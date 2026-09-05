from django.db import models
from core.mixins import ChampsEditables
from document_manager.models import Statement, LibraryNode, Document, DocumentSource
from events.models import Event
from email_manager.models import Quote as EmailQuote
from pdf_manager.models import Quote as PDFQuote
from photos.models import PhotoDocument
from googlechat_manager.models import ChatSequence
from datetime import datetime, date
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class TrameNarrative(models.Model, ChampsEditables):
    """
    Construit un dossier d'argumentation qui lie un ensemble de preuves 
    à un ensemble d'allégations cibles, dans le but de les supporter ou 
    de les contredire. This is the 'Evidence Collector'.
    """
    
    class TypeArgument(models.TextChoices):
        CONTRADICTION = 'CONTRADICTION', 'Vise à contredire les allégations'
        SUPPORT = 'SUPPORT', 'Vise à supporter les allégations'

    titre = models.CharField(
        max_length=255, 
        help_text="Un titre descriptif pour ce dossier d'argumentation (ex: 'Preuve de l'implication parentale')."
    )
    resume = models.TextField(
        help_text="Le résumé expliquant comment les preuves assemblées forment un argument cohérent contre (ou pour) les allégations ciblées."
    )
    type_argument = models.CharField(
        max_length=20,
        choices=TypeArgument.choices
    )

    targeted_statements = models.ManyToManyField(
        Statement,
        related_name='narratives_targeting_this_statement',
        blank=True,
        help_text="The specific statements targeted by this narrative."
    )

    # --- L'ensemble des preuves documentaires ---
    source_statements = models.ManyToManyField(
        Statement,
        related_name='narratives_using_this_statement_as_evidence',
        blank=True,
        help_text="Statements from other documents used as evidence."
    )
    evenements = models.ManyToManyField(
        Event,
        blank=True,
        related_name='trames_narratives'
    )
    citations_courriel = models.ManyToManyField(
        EmailQuote,
        blank=True,
        related_name='trames_narratives'
    )
    citations_pdf = models.ManyToManyField(
        PDFQuote,
        blank=True,
        related_name='trames_narratives'
    )
    photo_documents = models.ManyToManyField(
        PhotoDocument,
        blank=True,
        related_name='trames_narratives'
    )
    citations_chat = models.ManyToManyField(
        ChatSequence,
        blank=True,
        related_name='trames_narratives',
        help_text="Sequences of chat messages used as evidence."
    )

    # === NOUVEAUX CHAMPS POUR L'AUDITEUR IA ===
    ai_analysis_json = models.JSONField(
        default=dict,
        blank=True,
        help_text="Analyse objective générée par l'IA confrontant preuves vs allégations."
    )
    analysis_date = models.DateTimeField(null=True, blank=True)

    # The relations a narrative is actually built out of. targeted_statements is
    # deliberately absent: those are the allegations the narrative attacks, not
    # what holds it up. Kept here rather than in case_manager.signals so the two
    # readings of "evidence" cannot drift apart.
    EVIDENCE_FIELDS = (
        'evenements',
        'citations_courriel',
        'citations_pdf',
        'photo_documents',
        'source_statements',
        'citations_chat',
    )

    def __str__(self):
        return self.titre

    @classmethod
    def evidence_totals(cls, pks):
        """
        How many pieces of evidence each of these narratives holds, all relations summed.

        One query per relation instead of six joined Counts in a single query:
        joining all six at once multiplies the rows of every relation by those of
        the others, and a narrative citing a dozen items in several of them is
        enough for that product to get out of hand. Six small queries always
        cost six small queries.
        """
        totals = {pk: 0 for pk in pks}
        if not totals:
            return totals
        for field in cls.EVIDENCE_FIELDS:
            rows = cls.objects.filter(pk__in=totals).annotate(
                n=models.Count(field)
            ).values_list('pk', 'n')
            for pk, n in rows:
                totals[pk] += n
        return totals

    @classmethod
    def flag_orphans(cls, evidence_items):
        """
        Mark, on each item, the narratives that deleting it would destroy.

        Sets `orpheline_si_supprimee` on every narrative reached through the
        items' `trames_narratives`, and collects the doomed ones per item as
        `trames_orphelines`, so a page can show the consequence of a delete
        button before it is pressed.

        A narrative listed under an item and holding exactly one piece of
        evidence holds that item: the totals settle every case, and no query is
        needed per item. Prefetch `trames_narratives` on the items, or this
        reads them one at a time.
        """
        items = list(evidence_items)
        totals = cls.evidence_totals(
            {trame.pk for item in items for trame in item.trames_narratives.all()}
        )
        for item in items:
            trames = item.trames_narratives.all()
            for trame in trames:
                trame.orpheline_si_supprimee = totals.get(trame.pk, 0) == 1
            item.trames_orphelines = [t for t in trames if t.orpheline_si_supprimee]
        return items

    def is_supported_only_by(self, evidence):
        """
        True when `evidence` is the last thing holding this narrative up.

        Every evidence relation is searched, and the one that stores objects of
        this kind is searched with `evidence` taken out of it — what is being
        asked is what would be left once it is gone, not what is there now. A
        narrative that keeps anything at all, of any kind, is not orphaned.
        """
        for field in self.EVIDENCE_FIELDS:
            manager = getattr(self, field)
            queryset = manager.all()
            if manager.model is type(evidence):
                queryset = queryset.exclude(pk=evidence.pk)
            if queryset.exists():
                return False
        return True

    def get_chronological_evidence(self):
        timeline = []

        def to_datetime(d):
            if d is None: return None
            if isinstance(d, datetime): return timezone.make_aware(d) if timezone.is_naive(d) else d
            if isinstance(d, date): return timezone.make_aware(datetime.combine(d, datetime.min.time()))
            return None

        # Helper pour récupérer nom ET rôle
        def get_author_info(protagonist, default_name="Auteur inconnu"):
            if protagonist:
                return {
                    'name': protagonist.get_full_name(),
                    'role': protagonist.role
                }
            return {'name': default_name, 'role': ''}

        # 1. PDF Quotes
        for quote in self.citations_pdf.select_related('pdf_document', 'pdf_document__author'):
            auth_info = get_author_info(quote.pdf_document.author if quote.pdf_document else None, "Document officiel")
            doc_date = to_datetime(quote.pdf_document.document_date if quote.pdf_document else None)
            timeline.append({
                'type': 'pdf',
                'date': doc_date,
                'object': quote,
                'content': quote.quote_text,
                'author_name': auth_info['name'],
                'author_role': auth_info['role'],
                'source_title': quote.pdf_document.title if quote.pdf_document else "Document",
                'sort_key': quote.created_at.timestamp() if quote.created_at else 0
            })

        # 2. Emails
        for quote in self.citations_courriel.select_related('email', 'email__sender_protagonist'):
            email_date = to_datetime(quote.email.date_sent if quote.email else None)
            
            name = "Inconnu"
            role = ""
            if quote.email:
                if quote.email.sender_protagonist:
                    name = quote.email.sender_protagonist.get_full_name()
                    role = quote.email.sender_protagonist.role
                else:
                    name = quote.email.sender
                    role = "Expéditeur"

            timeline.append({
                'type': 'email',
                'date': email_date,
                'object': quote,
                'content': quote.quote_text,
                'author_name': name,
                'author_role': role,
                'source_title': f"Objet : {quote.email.subject}",
                'sort_key': email_date.timestamp() if email_date else 0
            })

        # 3. Statements
        statements = self.source_statements.all()
        if statements.exists():
            statement_ct = ContentType.objects.get_for_model(statements.first())
            nodes = LibraryNode.objects.filter(
                content_type=statement_ct,
                object_id__in=statements.values_list('pk', flat=True),
                document__source_type=DocumentSource.REPRODUCED
            ).select_related('document', 'document__author').order_by('path')

            node_map = {node.object_id: node for node in nodes}

            for statement in statements:
                node = node_map.get(statement.pk)
                
                doc_date = None
                name = "Analyse"
                role = ""
                title = "Constat"
                sort_path = ""

                if node:
                    doc = node.document
                    doc_date = doc.document_original_date
                    if doc.author:
                        name = doc.author.get_full_name()
                        role = doc.author.role
                    
                    title = doc.title
                    sort_path = node.path

                timeline.append({
                    'type': 'statement',
                    'date': to_datetime(doc_date),
                    'object': statement,
                    'content': statement.text,
                    'author_name': name,
                    'author_role': role,
                    'source_title': title,
                    'sort_key': sort_path
                })

        # Other evidence types
        for event in self.evenements.all():
            timeline.append({
                'type': 'event',
                'date': to_datetime(event.date),
                'object': event,
                'content': event.explanation,
                'author_name': "Observateur",
                'author_role': "Témoin",
                'source_title': 'Événement',
                'sort_key': ''
            })
            
        for photo in self.photo_documents.all():
             timeline.append({
                'type': 'photo',
                'date': to_datetime(photo.created_at),
                'object': photo,
                'content': photo.title,
                'author_name': "Photographe",
                'author_role': "Preuve Visuelle",
                'source_title': 'Document Photo',
                'sort_key': ''
            })
        
        for seq in self.citations_chat.all():
            timeline.append({
                'type': 'chat',
                'date': to_datetime(seq.start_date),
                'object': seq,
                'content': seq.title,
                'author_name': "Participants",
                'author_role': "Conversation",
                'source_title': 'Conversation',
                'sort_key': ''
            })

        # TRI FINAL :
        # 1. Par Date (Full Timestamp)
        # 2. Par Clé secondaire (Path ou Timestamp)
        # Note: On ne trie plus par 'author_name' en second pour respecter l'ordre chronologique strict (ex: réponses par email le même jour)
        return sorted(
            [item for item in timeline if item['date']], 
            key=lambda x: (x['date'], x.get('sort_key', ''))
        )

    def get_source_documents(self):
        """
        Collecte et retourne une liste unique de tous les documents sources
        (PDFs, Emails, Documents de Statements) référencés dans cette trame.
        """
        source_docs = {}

        # 1. PDF Documents from PDF Quotes
        for quote in self.citations_pdf.select_related('pdf_document'):
            doc = quote.pdf_document
            if doc:
                source_docs[f"pdf-{doc.pk}"] = {
                    'type': 'PDF',
                    'title': doc.title,
                    'url': doc.get_public_url()
                }

        # 2. Emails from Email Quotes
        for quote in self.citations_courriel.select_related('email'):
            email = quote.email
            if email:
                source_docs[f"email-{email.pk}"] = {
                    'type': 'Courriel',
                    'title': email.subject,
                    'url': email.get_public_url()
                }

        # 3. Documents from Statements
        statements = self.source_statements.all()
        if statements.exists():
            statement_ct = ContentType.objects.get_for_model(statements.first())
            nodes = LibraryNode.objects.filter(
                content_type=statement_ct,
                object_id__in=statements.values_list('pk', flat=True),
                document__source_type=DocumentSource.REPRODUCED
            ).select_related('document')

            for node in nodes:
                doc = node.document
                if doc:
                    source_docs[f"document-{doc.pk}"] = {
                        'type': 'Document',
                        'title': doc.title,
                        'url': doc.get_public_url()
                    }
        
        return list(source_docs.values())

    def get_structured_analysis(self):
        if self.ai_analysis_json and 'constats_objectifs' in self.ai_analysis_json:
            return self.ai_analysis_json
        
        return {
            "analyse_id": f"MANUAL-{self.pk}",
            "constats_objectifs": [{
                "fait_identifie": "Résumé narratif (Manuel)",
                "description_factuelle": self.resume,
                "contradiction_directe": "Non spécifié (Mode manuel)"
            }]
        }

    # Ce que la page peut écrire en place : voir `ChampsEditables`. Le résumé
    # n'a pas d'horodatage — il n'en a jamais eu, et rien ne l'affiche.
    champs_editables = {'resume': None}

    class Meta:
        verbose_name = "Trame Narrative"
        verbose_name_plural = "Trames Narratives"

class PerjuryArgument(models.Model):
    trame = models.OneToOneField(
        TrameNarrative, 
        on_delete=models.CASCADE, 
        related_name='perjury_argument',
        null=True
    )
    text_declaration = models.TextField(verbose_name="1. Déclaration faite sous serment", help_text="Contextualise the lie.", blank=True)
    text_proof = models.TextField(verbose_name="2. Preuve de la fausseté", help_text="Demonstrate why it is false.", blank=True)
    text_mens_rea = models.TextField(verbose_name="3. Connaissance de la fausseté (Mens Rea)", help_text="Demonstrate that they KNEW it was false.", blank=True)
    text_legal_consequence = models.TextField(verbose_name="4. Intention de tromper le tribunal", help_text="What did they hope to gain?", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Argument: {self.trame.titre}"

# ---------------------------------------------------------------------------
# Axes, faits, appuis
#
# Un AXE regroupe des FAITS ; chaque fait est soutenu par des APPUIS, et chaque
# appui joue un RÔLE déterminé dans ce soutien. L'axe vise une ou plusieurs
# allégations d'un acte reproduit.
#
# Trois choses distinguent cette structure de TrameNarrative, qui rassemblait
# des preuves autour d'un argument sans les qualifier :
#
#   1. La pièce soutient un FAIT, pas un axe. Une même pièce peut servir deux
#      faits pour des raisons différentes.
#   2. Le RÔLE détermine comment la pièce peut être invoquée. Un horaire de
#      2026 versé pour éclairer la forme d'une saison ne prouve pas le
#      calendrier de 2013 : le déclarer ILLUSTRATION empêche l'assemblage de
#      lui faire porter un fait qu'il ne porte pas.
#   3. Un axe est délibérément PARTIEL. Plusieurs axes convergent sur la même
#      allégation ; aucun ne prétend l'épuiser.
# ---------------------------------------------------------------------------

class RoleAppui(models.TextChoices):
    ATTESTATION = 'ATTESTATION', "Atteste directement un fait daté"
    CADRE = 'CADRE', "Établit la structure ou le contexte"
    INFERENCE = 'INFERENCE', "N'établit pas le fait, le présuppose"
    VERIFICATION = 'VERIFICATION', "Confirmation postérieure par un tiers"
    ILLUSTRATION = 'ILLUSTRATION', "À titre informatif — ne porte aucun fait"


class Axe(models.Model):
    """Un regroupement de faits opposé à une ou plusieurs allégations."""
    nom = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    # Facultatives : amorcent l'axe par une union temporelle. L'appartenance
    # d'une pièce n'en dépend pas — un horaire non daté ou une vérification
    # postérieure de plusieurs années y ont leur place.
    fenetre_debut = models.DateField(null=True, blank=True)
    fenetre_fin = models.DateField(null=True, blank=True)

    cibles = models.ManyToManyField(
        'document_manager.Statement', blank=True, related_name='axes_contestataires',
        help_text="Les allégations que cet axe conteste, dans un acte REPRODUCED."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Axe"
        verbose_name_plural = "Axes"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class NatureFait(models.TextChoices):
    """
    Tous les faits d'un axe ne se comportent pas de la même façon.

    La RÉSERVE mérite l'attention : c'est le seul type qui LIMITE au lieu
    d'affirmer, et donc le seul dont le retrait améliore la lecture tout en
    affaiblissant l'acte. Deux paragraphes du dépôt en portent une — §27
    (« Cette continuité biographique n'est pas invoquée comme preuve d'une
    inscription… ») et §28 (« Il n'est pas invoqué pour prétendre que les dates
    précises… »). Sans marquage, une relecture qui resserre la prose les coupe.
    """
    PROPOSITION = 'PROPOSITION', "Ce que l'axe affirme"
    DOCUMENTAIRE = 'DOCUMENTAIRE', "Ce qu'une pièce dit"
    STRUCTUREL = 'STRUCTUREL', "La structure d'une institution ou d'un cadre"
    RESERVE = 'RESERVE', "Ce qui n'est PAS allégué — neutralise une objection"
    INFERENCE = 'INFERENCE', "Tiré d'une conduite, non d'une affirmation"
    CONSEQUENCE = 'CONSEQUENCE', "Découle des faits précédents"


class Fait(models.Model):
    """
    Un énoncé factuel, soutenu par ses propres appuis.

    UN FAIT EST UN PARAGRAPHE DE L'EXPOSÉ. `statement` le rattache au
    paragraphe réellement plaidé dans un document PRODUCED ; `enonce` n'est que
    le brouillon qui précède ce rattachement. Quand les deux existent, l'écart
    entre eux EST le différentiel : ce que l'axe voudrait plaider contre ce qui
    l'est.

    `axes` est plusieurs-à-plusieurs et non une clé étrangère : un paragraphe
    de l'exposé n'existe qu'une fois et porte un seul numéro, alors que deux
    axes peuvent s'y appuyer. « La demanderesse suivait des cours de danse en
    soirée » sert l'axe de la danse et celui de la présence quotidienne.
    """
    axes = models.ManyToManyField(Axe, related_name='faits')
    ordre = models.PositiveIntegerField(default=1)
    enonce = models.TextField(
        help_text="Le fait tel qu'on souhaite le plaider. Brouillon tant que "
                  "`statement` est vide."
    )

    statement = models.ForeignKey(
        'document_manager.Statement', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='faits',
        help_text="Le paragraphe PRODUCED qui plaide ce fait. NULL = le fait "
                  "n'est pas encore au dossier."
    )

    nature = models.CharField(
        max_length=14, choices=NatureFait.choices,
        default=NatureFait.DOCUMENTAIRE
    )
    raison = models.TextField(
        blank=True,
        help_text="POURQUOI ce fait est formulé ainsi. Ne se plaide pas — c'est "
                  "ce qui empêche une relecture de couper une clause porteuse "
                  "en la prenant pour du remplissage."
    )

    class Meta:
        verbose_name = "Fait"
        verbose_name_plural = "Faits"
        ordering = ['ordre']

    def __str__(self):
        noms = ", ".join(a.nom[:28] for a in self.axes.all()) or "sans axe"
        return f"{noms} — {self.ordre}. {self.enonce[:60]}"

    @property
    def est_plaide(self):
        return self.statement_id is not None

    def numero_plaide(self):
        """Le numéro du paragraphe au dossier, ou None s'il n'est pas plaidé."""
        if not self.statement_id:
            return None
        from document_manager.models import LibraryNode
        ct = ContentType.objects.get_for_model(Statement)
        node = LibraryNode.objects.filter(
            content_type=ct, object_id=self.statement_id).first()
        return node.item if node else None


class RattachementAxe(models.Model):
    """
    « Cette pièce concerne cet axe. » — le niveau de TRIAGE.

    À NE PAS CONFONDRE AVEC `AppuiFait`. Les deux relient une pièce à un axe,
    mais ils affirment des choses différentes :

      RattachementAxe   un jugement de PERTINENCE. On le pose en parcourant le
                        registre, avant de savoir quel fait la pièce servira.
                        C'est une case qu'on coche.
      AppuiFait         une fonction PROBATOIRE. Elle nomme le FAIT soutenu et
                        le RÔLE joué. C'est ce qui se plaide.

    Ce n'est donc pas un doublon : le premier dit « j'ai regardé cette pièce et
    elle appartient à ce dossier-ci », le second dit « elle établit ceci, à ce
    titre ». Sans le premier, le triage de 334 pièces est impossible — il
    faudrait connaître le fait avant d'avoir lu la pièce.

    IMPLICATION À SENS UNIQUE. Un `AppuiFait` implique le rattachement à tous
    les axes de son fait ; la réciproque est fausse. Les vues affichent donc
    l'UNION des deux, et ne permettent jamais de « décocher » un axe adossé à
    un appui précis — ce serait supprimer un lien probatoire par une case.
    """
    axe = models.ForeignKey(Axe, on_delete=models.CASCADE,
                            related_name='rattachements')

    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    note = models.TextField(
        blank=True,
        help_text="Pourquoi cette pièce concerne cet axe, si ce n'est pas évident."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Rattachement à un axe"
        verbose_name_plural = "Rattachements à un axe"
        indexes = [models.Index(fields=['content_type', 'object_id'])]
        constraints = [
            models.UniqueConstraint(
                fields=['axe', 'content_type', 'object_id'],
                name='rattachement_axe_unique',
            ),
        ]

    def __str__(self):
        return f"{self.axe.nom} ← {self.content_type.model}-{self.object_id}"


class AppuiFait(models.Model):
    """Une pièce, le fait qu'elle soutient, et le rôle qu'elle y joue."""
    fait = models.ForeignKey(Fait, on_delete=models.CASCADE, related_name='appuis')
    ordre = models.PositiveIntegerField(default=1)

    # PROTECT : la disparition d'un ContentType ne doit pas emporter un appui.
    content_type = models.ForeignKey(
        ContentType, on_delete=models.PROTECT,
        help_text="Modèle de la pièce : Email, Event, PDFDocument, PhotoDocument…"
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    role = models.CharField(max_length=14, choices=RoleAppui.choices,
                            default=RoleAppui.ATTESTATION)
    note = models.TextField(blank=True,
                            help_text="Pourquoi cette pièce soutient ce fait, et à quel titre.")

    class Meta:
        verbose_name = "Appui"
        verbose_name_plural = "Appuis"
        ordering = ['fait', 'ordre']
        indexes = [models.Index(fields=['content_type', 'object_id'],
                                name='appui_cle_generique_idx')]
        constraints = [
            models.UniqueConstraint(
                fields=['fait', 'content_type', 'object_id'],
                name='appui_unique_par_fait',
            ),
        ]

    def __str__(self):
        return f"{self.role} — {self.content_object}"
