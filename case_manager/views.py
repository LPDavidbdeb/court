import html
import re
from django.views.generic import ListView, DetailView, CreateView, View, FormView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from collections import defaultdict
import json
import google.generativeai as genai
import docx
import io
from django.utils.html import strip_tags
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

from .models import LegalCase, PerjuryContestation, AISuggestion, ExhibitRegistry
from .forms import LegalCaseForm, PerjuryContestationForm, PerjuryContestationNarrativeForm, PerjuryContestationStatementsForm
from .services import refresh_case_exhibits
from ai_services.utils import EvidenceFormatter
from document_manager.models import LibraryNode, DocumentSource, Statement

def _get_allegation_context(targeted_statements):
    """
    Helper function to build the enriched text for allegations,
    grouping them by document and including the solemn declaration.
    """
    lies_text = "--- DÉCLARATIONS SOUS SERMENT (VERSION SUSPECTE) ---\n"
    statement_ids = [s.id for s in targeted_statements]

    stmt_content_type = ContentType.objects.get_for_model(Statement)
    nodes = LibraryNode.objects.filter(
        content_type=stmt_content_type,
        object_id__in=statement_ids,
        document__source_type=DocumentSource.REPRODUCED
    ).select_related('document', 'document__author')

    # Group statements by document
    doc_to_stmts = defaultdict(list)
    for node in nodes:
        doc_to_stmts[node.document].append(node.content_object)

    # Format the output
    for doc, stmts in doc_to_stmts.items():
        if doc.solemn_declaration:
            lies_text += f"CONTEXTE DU DOCUMENT : « {doc.title} »\n"
            lies_text += f"DÉCLARATION SOLENNELLE : « {doc.solemn_declaration} »\n\n"
        
        for stmt in stmts:
            author_name = "Auteur Inconnu"
            author_role = ""
            if doc.author:
                author_name = doc.author.get_full_name()
                author_role = f" [{doc.author.role}]"

            doc_date = "Date Inconnue"
            if doc.document_original_date:
                doc_date = doc.document_original_date.strftime('%d %B %Y')
            
            lies_text += f"[ {author_name}{author_role}, dans le document {doc.title} en date du {doc_date} ecrit : « {stmt.text} » ]\n\n"
    
    return lies_text

def serialize_evidence(evidence_pool):
    serialized_data = []
    if evidence_pool.get('events'):
        event_menu = []
        for event in evidence_pool['events']:
            event_menu.append({
                'title': f'Event: {event.date} - {event.explanation[:50]}...',
                'value': f'<blockquote><p>{event.explanation}</p><cite>Event on {event.date}</cite></blockquote>'
            })
        if event_menu:
            serialized_data.append({'title': 'Events', 'menu': event_menu})
    if evidence_pool.get('emails'):
        email_menu = []
        for quote in evidence_pool['emails']:
            email_menu.append({
                'title': f'Email Quote: {quote.quote_text[:50]}...',
                'value': f'<blockquote><p>{quote.quote_text}</p><cite>Email from {quote.email.sender} on {quote.email.date_sent}</cite></blockquote>'
            })
        if email_menu:
            serialized_data.append({'title': 'Email Quotes', 'menu': email_menu})
    return json.dumps(serialized_data)

def preview_ai_context(request, contestation_pk):
    contestation = get_object_or_404(PerjuryContestation, pk=contestation_pk)
    
    refresh_case_exhibits(contestation.case.pk)
    exhibit_registry = contestation.case.exhibits.all()
    exhibit_map = {
        (ex.content_type_id, ex.object_id): ex.get_label()
        for ex in exhibit_registry
    }

    evidence_data = EvidenceFormatter.collect_global_evidence(
        contestation.supporting_narratives.all()
    )

    lies_text = _get_allegation_context(contestation.targeted_statements.all())
    
    prompt_sequence = [
        f"""
        === 1. CADRE DE LA MISSION : RAPPORT DE DÉNONCIATION ===
        RÔLE : Enquêteur spécialisé en fraude judiciaire.
        OBJECTIF : Démontrer l'intention de tromper le tribunal.
        
        {lies_text}

        === 2. THÈSES ET CONTEXTE (Arguments Narratifs) ===
        Voici les dimensions factuelles qui contredisent l'allégation :
        """
    ]

    for i, summary in enumerate(evidence_data['summaries'], 1):
        text_content = strip_tags(summary)
        text_content = html.unescape(text_content)
        text_content = text_content.strip()
        prompt_sequence.append(f"DIMENSION {i} : {text_content}\n")

    prompt_sequence.append("\n=== 3. CHRONOLOGIE UNIFIÉE DES FAITS (PREUVE DIRECTE) ===")
    
    for item in evidence_data['timeline']:
        label = EvidenceFormatter.get_label(item['obj'], exhibit_map)
        line = EvidenceFormatter.format_timeline_item(item, exhibit_label=label)
        prompt_sequence.append(line)

    prompt_sequence.append("\n=== 4. INDEX DES PIÈCES & CONTEXTE (DÉTAILS COMPLETS) ===")
    
    def natural_keys(text):
        return [ int(c) if c.isdigit() else c for c in re.split(r'(\d+)', text) ]

    sorted_docs = sorted(
        list(evidence_data['unique_documents']), 
        key=lambda d: natural_keys(EvidenceFormatter.get_label(d, exhibit_map) or "")
    )

    for doc in sorted_docs:
        label = EvidenceFormatter.get_label(doc, exhibit_map)
        context_block = EvidenceFormatter.format_document_reference(doc, exhibit_label=label)
        prompt_sequence.append(context_block + "\n")

    prompt_sequence.append("""
    --- FIN DU DOSSIER ---

    TÂCHE DE RÉDACTION (FORMAT JSON STRICT) :
    Rédige le rapport en 4 sections distinctes.

    CONSIGNES DE TON (CRITIQUE) :
    1. TON : Clinique, factuel, froid et chirurgical.
    2. MISE EN PAGE : Utilise impérativement des sauts de ligne avant chaque point d'une liste numérotée (1., 2., etc.). Aère le texte.
    
    STRUCTURE REQUISE (JSON keys) :
    - suggestion_sec1 (La Déclaration) : Cite la phrase exacte du serment qui est fausse.
    - suggestion_sec2 (La Preuve Contraire) : Résume les faits de la chronologie qui prouvent physiquement l'impossibilité de la déclaration.
    - suggestion_sec3 (Mens Rea / Connaissance) : Démontre que le sujet *savait* que c'était faux au moment de signer (ex: il a lui-même écrit l'email contradictoire P-X).
    - suggestion_sec4 (L'Intention) : Explique *pourquoi* ce mensonge a été fait (le gain judiciaire espéré).
    """)
    
    full_preview = "".join(prompt_sequence)
    return HttpResponse(full_preview, content_type="text/plain; charset=utf-8")

class LegalCaseListView(ListView):
    model = LegalCase
    template_name = 'case_manager/legalcase_list.html'
    context_object_name = 'cases'
    ordering = ['-created_at']

class LegalCaseDetailView(DetailView):
    model = LegalCase
    template_name = 'case_manager/legalcase_detail.html'
    context_object_name = 'case'
    def get(self, request, *args, **kwargs):
        refresh_case_exhibits(self.kwargs['pk'])
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contestations'] = self.object.contestations.all()
        return context

class LegalCaseCreateView(CreateView):
    model = LegalCase
    form_class = LegalCaseForm
    template_name = 'case_manager/legalcase_form.html'
    def get_success_url(self):
        return reverse_lazy('case_manager:case_detail', kwargs={'pk': self.object.pk})

class LegalCaseExportView(View):
    def get(self, request, *args, **kwargs):
        case = get_object_or_404(LegalCase, pk=self.kwargs['pk'])
        document = docx.Document()

        # ------------------------------------------------------------------
        # HELPER: Text Cleaning & Markdown Parsing
        # ------------------------------------------------------------------
        def clean_text(text):
            if not text: return ""
            text = text.replace('</p>', '\n').replace('<br>', '\n').replace('<br/>', '\n')
            text = strip_tags(text)
            text = html.unescape(text)
            return text.strip()

        def add_markdown_content(doc, raw_text):
            text = clean_text(raw_text)
            if not text: return

            # === FIX: AGGRESSIVE NEWLINE INJECTION ===
            
            # 1. Force newline before Bullet Points hidden in text
            text = re.sub(r'([\.\:\;])\s+([\*\-]\s)', r'\1\n\2', text)

            # 2. Force newline before Numbered Lists hidden in text
            text = re.sub(r'([\.\:\;])\s+(\d+\.\s)', r'\1\n\2', text)

            # 3. Fix the specific "Closing Quote + List" issue
            text = re.sub(r'(»)\s+([\*\-\d])', r'\1\n\2', text)

            # 4. Cleanup rare triple stars "***" into "* **" for consistency
            text = text.replace('***', '* **')

            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line: continue

                # Detect List Style
                para_style = None
                
                # Check for Bullet (* or -)
                if re.match(r'^[\*\-]\s+', line):
                    para_style = 'List Bullet'
                    line = re.sub(r'^[\*\-]\s+', '', line) # Remove marker
                
                # Check for Numbered (1., 2.)
                elif re.match(r'^\d+\.\s+', line):
                    para_style = 'List Number'
                    line = re.sub(r'^\d+\.\s+', '', line) # Remove marker

                p = doc.add_paragraph(style=para_style)
                
                # Parse Bold segments (**text**)
                parts = re.split(r'(\*\*.*?\*\*)', line)
                for part in parts:
                    if part.startswith('**') and part.endswith('**'):
                        clean_part = part[2:-2] # Strip **
                        if clean_part:
                            p.add_run(clean_part).bold = True
                    else:
                        p.add_run(part)

        # ------------------------------------------------------------------
        # DOCUMENT GENERATION (Margins & Structure)
        # ------------------------------------------------------------------
        section = document.sections[0]
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

        document.add_heading(f'Dénonciation: {case.title}', level=0)
        
        for contestation in case.contestations.all():
            document.add_heading(contestation.title, level=2)
            
            # Apply the enhanced parser to all sections
            document.add_heading('1. Déclaration', level=3)
            add_markdown_content(document, contestation.final_sec1_declaration)
            
            document.add_heading('2. Preuve', level=3)
            add_markdown_content(document, contestation.final_sec2_proof)
            
            document.add_heading('3. Mens Rea', level=3)
            add_markdown_content(document, contestation.final_sec3_mens_rea)
            
            document.add_heading('4. Intention', level=3)
            add_markdown_content(document, contestation.final_sec4_intent)
            
            document.add_page_break()

        # --- TABLE OF EXHIBITS ---
        document.add_heading('Index des Pièces (Exhibits)', level=1)
        table = document.add_table(rows=1, cols=3)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Cote'
        hdr_cells[1].text = 'Description'
        hdr_cells[2].text = 'Date'

        for exhibit in case.exhibits.order_by('exhibit_number'):
            row_cells = table.add_row().cells
            row_cells[0].text = exhibit.get_label()
            obj = exhibit.content_object
            row_cells[1].text = str(obj)

            date_str = ""
            if hasattr(obj, 'document_original_date') and obj.document_original_date:
                date_str = str(obj.document_original_date)
            elif hasattr(obj, 'date'):
                date_str = str(obj.date)
            elif hasattr(obj, 'date_sent'):
                date_str = str(obj.date_sent.date())
            row_cells[2].text = date_str

        # ==================================================================
        # ANNEXES
        # ==================================================================
        document.add_page_break()
        document.add_heading('ANNEXES - CONTENU DÉTAILLÉ', level=0)

        for exhibit in case.exhibits.order_by('exhibit_number'):
            obj = exhibit.content_object
            label = exhibit.get_label()
            model_name = exhibit.content_type.model

            document.add_heading(f'Pièce {label}', level=1)

            # ---------------------------------------------------------
            # 1. EMAILS
            # ---------------------------------------------------------
            if model_name == 'email':
                p = document.add_paragraph()
                p.add_run(f"Date : {obj.date_sent}\n").bold = True
                p.add_run(f"De : {obj.sender}\n").bold = True
                p.add_run(f"À : {obj.recipients_to}\n").bold = True
                p.add_run(f"Sujet : {obj.subject}").bold = True
                document.add_paragraph('--- Contenu ---').italic = True
                
                # Emails are usually plain text
                body_text = clean_text(obj.body_plain_text or "[Vide]")
                document.add_paragraph(body_text).alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

            # ---------------------------------------------------------
            # 2. EVENTS
            # ---------------------------------------------------------
            elif model_name == 'event':
                document.add_paragraph(f"Date : {obj.date}")
                p = document.add_paragraph()
                p.add_run("Description : ").bold = True
                
                # Apply Markdown parsing to Event explanation too
                add_markdown_content(document, obj.explanation)

                photos = obj.linked_photos.all()
                if photos.exists():
                    document.add_paragraph("Preuve visuelle :").italic = True
                    photo_table = document.add_table(rows=0, cols=2)
                    row_cells = None

                    for index, photo in enumerate(photos):
                        if index % 2 == 0:
                            row_cells = photo_table.add_row().cells
                        cell = row_cells[index % 2]
                        if photo.file:
                            try:
                                paragraph = cell.paragraphs[0]
                                run = paragraph.add_run()
                                run.add_picture(photo.file.open(), width=Inches(2.8))
                                caption = cell.add_paragraph(photo.file_name or "Image")
                                caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            except Exception as e:
                                cell.add_paragraph(f"[Erreur: {e}]")

            # ---------------------------------------------------------
            # 3. PHOTO DOCUMENTS
            # ---------------------------------------------------------
            elif model_name == 'photodocument':
                document.add_paragraph(f"Titre : {obj.title}")
                if obj.description:
                    add_markdown_content(document, obj.description)

                if hasattr(obj, 'ai_analysis') and obj.ai_analysis:
                    document.add_heading("Analyse IA :", level=4)
                    add_markdown_content(document, obj.ai_analysis)

                photos = obj.photos.all()
                if photos.exists():
                    photo_table = document.add_table(rows=0, cols=2)
                    row_cells = None
                    for index, photo in enumerate(photos):
                        if index % 2 == 0:
                            row_cells = photo_table.add_row().cells
                        cell = row_cells[index % 2]
                        if photo.file:
                            try:
                                paragraph = cell.paragraphs[0]
                                run = paragraph.add_run()
                                run.add_picture(photo.file.open(), width=Inches(2.8))
                                caption = cell.add_paragraph(f"Page {index + 1}")
                                caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            except Exception as e:
                                cell.add_paragraph(f"[Erreur: {e}]")

            # ---------------------------------------------------------
            # 4. PDF DOCUMENTS
            # ---------------------------------------------------------
            elif model_name == 'pdfdocument':
                document.add_paragraph(f"Document : {obj.title}")
                if hasattr(obj, 'ai_analysis') and obj.ai_analysis:
                    document.add_heading("Résumé / Analyse :", level=3)
                    add_markdown_content(document, obj.ai_analysis)
                document.add_paragraph("[Voir fichier PDF joint]").italic = True

            document.add_page_break()

        # Save
        f = io.BytesIO()
        document.save(f)
        f.seek(0)
        response = HttpResponse(f.getvalue(),
                                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="case_{case.pk}_export.docx"'
        return response

class PerjuryContestationCreateView(CreateView):
    model = PerjuryContestation
    form_class = PerjuryContestationForm
    template_name = 'case_manager/perjurycontestation_form.html'
    def form_valid(self, form):
        form.instance.case = get_object_or_404(LegalCase, pk=self.kwargs['case_pk'])
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('case_manager:contestation_detail', kwargs={'pk': self.object.pk})

class ManageContestationNarrativesView(UpdateView):
    model = PerjuryContestation
    form_class = PerjuryContestationNarrativeForm
    template_name = 'case_manager/manage_narratives.html'
    context_object_name = 'contestation'

    def get_success_url(self):
        messages.success(self.request, "Supporting narratives updated successfully.")
        return reverse('case_manager:contestation_detail', kwargs={'pk': self.object.pk})

class ManageContestationStatementsView(UpdateView):
    model = PerjuryContestation
    form_class = PerjuryContestationStatementsForm
    template_name = 'case_manager/manage_statements.html'
    context_object_name = 'contestation'

    def get_success_url(self):
        messages.success(self.request, "Targeted statements updated successfully.")
        return reverse('case_manager:contestation_detail', kwargs={'pk': self.object.pk})

class PerjuryContestationDetailView(UpdateView):
    model = PerjuryContestation
    template_name = 'case_manager/perjurycontestation_detail.html'
    context_object_name = 'contestation'
    fields = ['final_sec1_declaration', 'final_sec2_proof', 'final_sec3_mens_rea', 'final_sec4_intent']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evidence_pool = {'events': [], 'emails': [], 'pdfs': []}
        for narrative in self.object.supporting_narratives.all():
            evidence_pool['events'].extend(narrative.evenements.all())
            evidence_pool['emails'].extend(narrative.citations_courriel.all())
            evidence_pool['pdfs'].extend(narrative.citations_pdf.all())
        context['evidence_json'] = serialize_evidence(evidence_pool)
        context['ai_drafts'] = self.object.ai_suggestions.order_by('-created_at')
        return context

    def get_success_url(self):
        return reverse('case_manager:contestation_detail', kwargs={'pk': self.object.pk})

def generate_ai_suggestion(request, contestation_pk):
    contestation = get_object_or_404(PerjuryContestation, pk=contestation_pk)
    
    refresh_case_exhibits(contestation.case.pk)
    exhibit_registry = contestation.case.exhibits.all()
    exhibit_map = {
        (ex.content_type_id, ex.object_id): ex.get_label()
        for ex in exhibit_registry
    }

    evidence_data = EvidenceFormatter.collect_global_evidence(
        contestation.supporting_narratives.all()
    )

    lies_text = _get_allegation_context(contestation.targeted_statements.all())
    
    prompt_sequence = [
        f"""
        === 1. CADRE DE LA MISSION : RAPPORT DE DÉNONCIATION ===
        RÔLE : Enquêteur spécialisé en fraude judiciaire.
        OBJECTIF : Démontrer l'intention de tromper le tribunal.
        
        {lies_text}

        === 2. THÈSES ET CONTEXTE (Arguments Narratifs) ===
        Voici les dimensions factuelles qui contredisent l'allégation :
        """
    ]

    for i, summary in enumerate(evidence_data['summaries'], 1):
        text_content = strip_tags(summary)
        text_content = html.unescape(text_content)
        text_content = text_content.strip()
        prompt_sequence.append(f"DIMENSION {i} : {text_content}\n")

    prompt_sequence.append("\n=== 3. CHRONOLOGIE UNIFIÉE DES FAITS (PREUVE DIRECTE) ===")
    
    for item in evidence_data['timeline']:
        label = EvidenceFormatter.get_label(item['obj'], exhibit_map)
        line = EvidenceFormatter.format_timeline_item(item, exhibit_label=label)
        prompt_sequence.append(line)

    prompt_sequence.append("\n=== 4. INDEX DES PIÈCES & CONTEXTE (DÉTAILS COMPLETS) ===")
    
    def natural_keys(text):
        return [ int(c) if c.isdigit() else c for c in re.split(r'(\d+)', text) ]

    sorted_docs = sorted(
        list(evidence_data['unique_documents']), 
        key=lambda d: natural_keys(EvidenceFormatter.get_label(d, exhibit_map) or "")
    )

    for doc in sorted_docs:
        label = EvidenceFormatter.get_label(doc, exhibit_map)
        context_block = EvidenceFormatter.format_document_reference(doc, exhibit_label=label)
        prompt_sequence.append(context_block + "\n")

    prompt_sequence.append("""
    --- FIN DU DOSSIER ---

    TÂCHE DE RÉDACTION (FORMAT JSON STRICT) :
    Rédige le rapport en 4 sections distinctes.

    CONSIGNES DE TON (CRITIQUE) :
    1. TON : Clinique, factuel, froid et chirurgical.
    2. MISE EN PAGE : Utilise impérativement des sauts de ligne avant chaque point d'une liste numérotée (1., 2., etc.). Aère le texte.
    
    STRUCTURE REQUISE (JSON keys) :
    - suggestion_sec1 (La Déclaration) : Cite la phrase exacte du serment qui est fausse.
    - suggestion_sec2 (La Preuve Contraire) : Résume les faits de la chronologie qui prouvent physiquement l'impossibilité de la déclaration.
    - suggestion_sec3 (Mens Rea / Connaissance) : Démontre que le sujet *savait* que c'était faux au moment de signer (ex: il a lui-même écrit l'email contradictoire P-X).
    - suggestion_sec4 (L'Intention) : Explique *pourquoi* ce mensonge a été fait (le gain judiciaire espéré).
    """)
    
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro-latest')
        
        # 1. APPEL API (L'étape coûteuse)
        response = model.generate_content(prompt_sequence)
        raw_text = response.text

        # 2. SAUVEGARDE IMMÉDIATE (Le Staging)
        suggestion = AISuggestion.objects.create(
            contestation=contestation,
            raw_response=raw_text, # On sauve le brut !
            content={},            # Vide pour l'instant
            parsing_success=False
        )

        # 3. TRAITEMENT / PARSING (L'étape fragile)
        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        
        if json_match:
            try:
                cleaned_text = json_match.group(0)
                data_dict = json.loads(cleaned_text)
                
                # Mise à jour avec les données structurées
                suggestion.content = data_dict
                suggestion.parsing_success = True
                suggestion.save()
                
                messages.success(request, "Suggestion IA générée et structurée avec succès !")
                
            except json.JSONDecodeError as e:
                # Le JSON est malformé, mais on a gardé le texte brut !
                print(f"Erreur de décodage JSON sur la suggestion #{suggestion.pk}: {e}")
                messages.warning(request, "Réponse IA reçue mais formatage JSON échoué. Le brouillon brut a été sauvegardé.")
        else:
            messages.warning(request, "L'IA a répondu mais sans structure JSON détectable. Texte brut sauvegardé.")

    except Exception as e:
        print(f"AI Gen Error: {e}")
        messages.error(request, f"Erreur critique lors de l'appel API : {e}")

    return redirect('case_manager:contestation_detail', pk=contestation.pk)
