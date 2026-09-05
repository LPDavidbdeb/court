from django.db import models
from pgvector.django import VectorField
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from core.mixins import ExhibitableMixin, ChampsEditables
from core.text_matching import fold_for_matching, locate
from datetime import datetime
import re

import fitz

class PDFDocumentType(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The name of the document type (e.g., 'Mémoire de Marie-Josée')."
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "PDF Document Type"
        verbose_name_plural = "PDF Document Types"
        ordering = ['name']

class PDFDocument(models.Model, ExhibitableMixin, ChampsEditables):
    title = models.CharField(
        max_length=255,
        help_text="The title of the PDF document."
    )
    author = models.ForeignKey(
        'protagonist_manager.Protagonist',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='authored_pdfs',
        help_text="The author of the document, if applicable."
    )
    file = models.FileField(
        upload_to='pdf_documents/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="The uploaded PDF file."
    )
    document_date = models.DateField(
        null=True,
        blank=True,
        help_text="The date of the document, if applicable."
    )
    document_type = models.ForeignKey(
        PDFDocumentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The type or category of this PDF document."
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time the document was uploaded."
    )
    ai_analysis = models.TextField(
        blank=True, null=True,
        help_text="Analyse forensique et résumé généré par l'IA pour économiser les tokens multimodaux."
    )
    embedding = VectorField(dimensions=768, null=True, blank=True)

    # --- Analyse rédigée (corpus legal/) ---
    #
    # À ne pas confondre avec `ai_analysis`, qui porte la transcription
    # générée : `analyse` est un texte écrit, importé d'un fichier du corpus et
    # relu ici. `analyse_maj` reste NULL tant que personne n'a rien écrit —
    # un `auto_now_add` aurait horodaté toutes les lignes existantes à la date
    # de la migration, une provenance fausse écrite avec l'autorité d'un champ
    # système.
    analyse = models.TextField(
        blank=True, default='',
        help_text="Analyse rédigée sur cette pièce, en HTML."
    )
    analyse_source = models.CharField(
        max_length=255, blank=True, default='',
        help_text="Nom du fichier du corpus dont l'analyse est issue. Rend "
                  "l'import rejouable et permet de comparer base et fichier."
    )
    analyse_maj = models.DateTimeField(
        null=True, blank=True,
        help_text="Dernière écriture de l'analyse. NULL = jamais renseignée."
    )

    # `note` n'est écrite que par l'utilisateur, depuis la page. Aucun
    # traitement automatique n'y touche : elle ne figure dans aucun
    # `update_fields` d'import. Voir `email_manager.Email.note`.
    note = models.TextField(
        blank=True, default='',
        help_text="Note de l'utilisateur sur cette pièce, en HTML. Jamais écrite par un import."
    )
    note_maj = models.DateTimeField(
        null=True, blank=True,
        help_text="Dernière écriture de la note. NULL = jamais renseignée."
    )

    # Ce que la page peut écrire en place : voir `ChampsEditables`.
    champs_editables = {'analyse': 'analyse_maj', 'note': 'note_maj'}

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pdf_manager:pdf_detail', kwargs={'pk': self.pk})

    def get_public_url(self):
        return reverse('core:pdf_document_public', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "PDF Document"
        verbose_name_plural = "PDF Documents"
        # Le pk départage les ex aequo : plusieurs pièces portent la même date
        # (trois au 1er janvier 2025), et sans second critère leur ordre était
        # laissé à la base. La liste s'en accommodait ; la navigation d'une
        # pièce à l'autre, elle, doit pouvoir nommer un voisin unique.
        ordering = ['-document_date', '-pk']

    # A transcription opens each page with a fenced line of this shape. Some
    # markers carry a note after the closing fence — '--- PAGE 5 --- (page 1 du
    # formulaire)', where one file holds two documents — so the line is matched
    # by how it starts, not by standing alone.
    PAGE_MARKER = re.compile(r'^[ \t]*-{2,}[ \t]*PAGE[ \t]*(\d+)[ \t]*-{2,}.*$',
                             re.IGNORECASE | re.MULTILINE)

    @property
    def transcription(self):
        """
        The transcribed text of this document, without its provenance header.

        ai_analysis holds the transcription itself, not a summary of it — the
        structured ones open with an HTML comment describing the transcription
        rather than the document, so it is dropped. The '--- PAGE n ---'
        markers are left in place: they carry the page number, and removing
        them would only shift every offset by the same amount.
        """
        return re.sub(r'^\s*<!--.*?-->', '', self.ai_analysis or "", count=1, flags=re.S)

    def transcription_pages(self):
        """
        The transcription split on its page markers, as [{'number', 'text'}].

        The text before the first marker — the note some transcriptions open
        with to say the file holds two documents — belongs to no page and is
        returned with a number of None, as is the whole transcription when it
        carries no markers at all. Text selected from a numbered block can fill
        the page field on its own; text selected from an unnumbered one leaves
        that field to be typed.
        """
        text = self.transcription
        if not text.strip():
            return []

        marks = list(self.PAGE_MARKER.finditer(text))
        if not marks:
            return [{'number': None, 'text': text.strip()}]

        pages = []
        preamble = text[:marks[0].start()].strip()
        if preamble:
            pages.append({'number': None, 'text': preamble})
        for i, mark in enumerate(marks):
            end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
            pages.append({'number': int(mark.group(1)),
                          'text': text[mark.end():end].strip()})
        return pages

    def has_text_layer(self, min_chars=200):
        """
        Whether the file draws real text rather than scanned pixels.

        This decides which reading surface the quote workbench offers. A
        document with a text layer is rendered by PDF.js, whose text becomes
        selectable DOM nodes; a scan has nothing to select, and the
        transcription stands in for it. The threshold tolerates the stray page
        number or scanner stamp that an image-only PDF sometimes carries, which
        is text but is not the document.

        A file that cannot be opened is reported as a scan: the transcription
        is then the only thing left to read it with, which is the right
        fallback for a PDF too damaged to parse.
        """
        try:
            with self.file.open('rb') as handle:
                data = handle.read()
        except Exception:
            return False

        try:
            with fitz.open(stream=data, filetype='pdf') as document:
                total = 0
                for page in document:
                    total += len(page.get_text('text').strip())
                    if total >= min_chars:
                        return True
        except Exception:
            return False
        return False

    # --- Exhibitable Interface ---
    def get_exhibit_date(self):
        if self.document_date:
            return datetime.combine(self.document_date, datetime.min.time())
        return self.uploaded_at

    def get_exhibit_title(self):
        return self.title

    def get_exhibit_type(self):
        return "Document PDF"

    def get_exhibit_parties(self):
        return f"Auteur: {self.author.get_full_name_with_role()}" if self.author else ""

    def get_exhibit_description(self):
        return self.ai_analysis or self.title

class Quote(models.Model, ChampsEditables):
    embedding = VectorField(dimensions=768, null=True, blank=True)
    pdf_document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE, related_name='quotes')
    quote_text = models.TextField()

    # Ce que la page peut écrire en place : voir `ChampsEditables`. Sans
    # horodatage — `updated_at` en tient lieu, et il n'est affiché nulle part.
    #
    # Seul `quote_text` est ouvert. `position_anchor` se corrige aussi de temps
    # à autre, mais il n'est jamais affiché : un champ qu'on ne voit pas ne peut
    # pas se modifier en place, il faudrait d'abord décider où le montrer.
    champs_editables = {'quote_text': None}
    page_number = models.PositiveIntegerField(
        help_text="The page number where the quote can be found."
    )
    quote_location_details = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional details to locate the quote, e.g., 'Paragraph 3' or 'Header'."
    )
    position_anchor = models.TextField(
        blank=True,
        default="",
        help_text=(
            "A verbatim fragment of the document, used only to place this quote in "
            "the text. Fill it in when quote_text is a reading of the document — a "
            "summary of table rows, say — rather than a passage copied out of it, "
            "and so cannot be found by searching for it. Never displayed."
        )
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('pdf_manager:quote_detail', kwargs={'pk': self.pk})

    @property
    def source_text(self):
        """
        The transcribed text of the document this quote was taken from.

        PDFDocument.transcription does the work, since the same text is now
        also read on screen when the document is a scan the quote workbench
        cannot render selectably.
        """
        return self.pdf_document.transcription if self.pdf_document else ""

    @property
    def position_in_source(self):
        """
        Sort key placing this quote where it actually sits in the document.

        Same reasoning as email_manager.Quote.position_in_source: created_at only
        describes the document while the reader never goes back up the text.

        The page is the dominant term and is always meaningful — page_number is
        populated on every quote. Position WITHIN a page used to be uncomputable,
        on the belief that ai_analysis was only a summary; it is in fact the
        transcription, so the offset of the quote in that text now ranks quotes
        sharing a page. The offset is measured document-wide rather than
        per-page, which orders a page's quotes identically and costs nothing to
        compute for the documents transcribed without page markers.

        A quote that reads the document rather than copying it — one that
        summarises a table's rows — is nowhere in the text to be found, however
        faithfully it renders what the table says. position_anchor exists for
        those: a verbatim fragment that says where the reading belongs, searched
        in place of quote_text whenever it is set. A wrong anchor simply fails
        to locate, exactly as an unfindable quote does.

        Returns (page, found, rank, pk). Quotes located in the transcription
        rank by offset; those that cannot be located trail them in creation
        order, which is the old behaviour kept where the new key has nothing to
        say. quote_location_details ('Paragraph 3', 'Header') is still not used:
        it is free text, filled on a small minority of quotes, and ordering on
        it would be guesswork dressed as precision.
        """
        page = self.page_number if self.page_number is not None else 10 ** 9
        offset = locate(fold_for_matching(self.source_text),
                        fold_for_matching(self.position_anchor or self.quote_text))
        if offset >= 0:
            return (page, 0, offset, self.pk)
        return (page, 1, self.created_at.timestamp() if self.created_at else 0.0, self.pk)

    @property
    def full_sentence(self):
        """
        Dynamically generates a full descriptive sentence for the quote,
        pulling metadata from the parent PDFDocument object.
        """
        if not self.pdf_document:
            return self.quote_text

        doc_title = self.pdf_document.title or "(Untitled Document)"
        return f'In the document "{doc_title}", on page {self.page_number}, it says: "{self.quote_text}"'

    def __str__(self):
        return f'Quote from "{self.pdf_document.title}" on page {self.page_number}'

    class Meta:
        verbose_name = "PDF Quote"
        verbose_name_plural = "PDF Quotes"
        ordering = ['-created_at']
