from django.views.generic import ListView, DetailView, CreateView, View
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
import json
import google.generativeai as genai
import docx
import io

from .models import LegalCase, PerjuryContestation, AISuggestion
from .forms import LegalCaseForm, PerjuryContestationForm
from .services import refresh_case_exhibits
from ai_services.utils import EvidenceFormatter
from document_manager.models import LibraryNode, DocumentSource, Statement

def _get_allegation_context(targeted_statements):
    """
    Helper function to build the enriched text for allegations,
    including their original source document context.
    """
    lies_text = "--- DÉCLARATIONS SOUS SERMENT (VERSION SUSPECTE) ---\n"
    statement_ids = [s.id for s in targeted_statements]

    stmt_content_type = ContentType.objects.get_for_model(Statement)
    nodes = LibraryNode.objects.filter(
        content_type=stmt_content_type,
        object_id__in=statement_ids,
        document__source_type=DocumentSource.REPRODUCED
    ).select_related('document', 'document__author')

    stmt_to_doc_map = {node.object_id: node.document for node in nodes}

    for stmt in targeted_statements:
        doc = stmt_to_doc_map.get(stmt.id)
        author_name = "Auteur Inconnu"
        author_role = ""
        if doc and doc.author:
            author_name = doc.author.get_full_name()
            author_role = f" [{doc.author.role}]"

        doc_date = "Date Inconnue"
        if doc and doc.document_original_date:
            doc_date = doc.document_original_date.strftime('%d %B %Y')
        
        lies_text += f"[De {author_name}{author_role}, le {doc_date}]: « {stmt.text} »\n\n"
    
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
    lies_text = _get_allegation_context(contestation.targeted_statements.all())

    full_preview = f"""
        === 1. CADRE DE LA MISSION : RAPPORT DE DÉNONCIATION ===
        
        RÔLE : Enquêteur spécialisé en fraude judiciaire (Profil: Police / Investigation).
        
        OBJECTIF : 
        Démontrer l'intention de tromper le tribunal en confrontant la déclaration sous serment à la preuve brute (pièces justificatives).
        
        MÉTHODOLOGIE AXIOMATIQUE :
        - Ne cherche pas de nuances psychologiques. Cherche des impossibilités matérielles.
        - Logique binaire : Si la Preuve A dit BLANC et la Déclaration B dit NOIR, alors B est faux.
        - Si l'auteur a généré la Preuve A (ex: son propre courriel), alors l'ignorance (erreur) est impossible. C'est donc un mensonge volontaire.
        
        {lies_text}
        
        === DÉBUT DU DOSSIER DE PREUVES (TEXTES COMPLETS & IMAGES) ===
        """
    for narrative in contestation.supporting_narratives.all():
        sequence = EvidenceFormatter.unpack_narrative_multimodal(narrative)
        for item in sequence:
            if isinstance(item, str):
                full_preview += item + "\n"
            else:
                image_type = type(item).__name__
                full_preview += f"\n[ *** IMAGE MULTIMODALE INSÉRÉE ICI ({image_type}) *** ]\n\n"
    full_preview += """
    --- FIN DU DOSSIER ---
    
    TÂCHE DE RÉDACTION (FORMAT JSON STRICT) :
    Rédige un rapport factuel en 4 points :
    
    - suggestion_sec1 (Les Faits Allégués) : 
      Résumé neutre : "Le [Date], X a déclaré sous serment que..."
      
    - suggestion_sec2 (La Preuve Contraire) : 
      Démonstration technique : "Cette affirmation est contredite par la pièce P-Y (Courriel du [Date]). Dans ce document, on lit explicitement : '[Citation]'."
      (Cite les passages clés du courriel complet pour prouver le contexte).
      
    - suggestion_sec3 (L'Élément Intentionnel / Mens Rea) : 
      Raisonnement déductif : "L'intention est démontrée par le fait que l'auteur possédait la preuve contraire (ex: en étant l'expéditeur du courriel). Il ne pouvait ignorer la réalité."
      
    - suggestion_sec4 (Le Mobile / Intention Stratégique) : 
      Constat de bénéfice : "Cette fausse représentation a eu pour effet de [Masquer un actif / Obtenir un délai / Créer un préjudice]."
    """
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
        document.add_heading(f'Case: {case.title}', level=1)
        for contestation in case.contestations.all():
            document.add_heading(contestation.title, level=2)
            document.add_heading('1. Déclaration', level=3)
            document.add_paragraph(contestation.final_sec1_declaration)
            document.add_heading('2. Preuve', level=3)
            document.add_paragraph(contestation.final_sec2_proof)
            document.add_heading('3. Mens Rea', level=3)
            document.add_paragraph(contestation.final_sec3_mens_rea)
            document.add_heading('4. Intention', level=3)
            document.add_paragraph(contestation.final_sec4_intent)
            document.add_page_break()
        document.add_heading('Table of Exhibits', level=1)
        table = document.add_table(rows=1, cols=3)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Exhibit ID'
        hdr_cells[1].text = 'Description'
        hdr_cells[2].text = 'Date'
        for exhibit in case.exhibits.order_by('exhibit_number'):
            row_cells = table.add_row().cells
            row_cells[0].text = exhibit.get_label()
            obj = exhibit.content_object
            row_cells[1].text = str(obj)
            if hasattr(obj, 'document_original_date') and obj.document_original_date:
                row_cells[2].text = str(obj.document_original_date)
            elif hasattr(obj, 'date'):
                row_cells[2].text = str(obj.date)
            elif hasattr(obj, 'date_sent'):
                row_cells[2].text = str(obj.date_sent.date())
            elif hasattr(obj, 'created_at'):
                row_cells[2].text = str(obj.created_at.date())
            else:
                row_cells[2].text = ""
        f = io.BytesIO()
        document.save(f)
        f.seek(0)
        response = HttpResponse(f.getvalue(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
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
    lies_text = _get_allegation_context(contestation.targeted_statements.all())
    
    prompt_sequence = [
        f"""
        === 1. CADRE DE LA MISSION : RAPPORT DE DÉNONCIATION ===
        RÔLE : Enquêteur spécialisé en fraude judiciaire (Profil: Police / Investigation).
        OBJECTIF : 
        Démontrer l'intention de tromper le tribunal en confrontant la déclaration sous serment (Ci-dessus) à la preuve brute (Ci-dessous).
        MÉTHODOLOGIE AXIOMATIQUE :
        - Ne cherche pas de nuances psychologiques. Cherche des impossibilités matérielles.
        - Si la Preuve A (Datée) contredit la Déclaration B (Datée), note-le.
        - Si l'auteur a généré la Preuve A (ex: son propre courriel), l'ignorance est impossible.
        {lies_text}
        === DÉBUT DU DOSSIER DE PREUVES (TEXTES COMPLETS & IMAGES) ===
        """
    ]
    for narrative in contestation.supporting_narratives.all():
        narrative_content = EvidenceFormatter.unpack_narrative_multimodal(narrative)
        prompt_sequence.extend(narrative_content)
    prompt_sequence.append("""
    --- FIN DU DOSSIER ---
    TÂCHE DE RÉDACTION (FORMAT JSON STRICT) :
    Rédige un rapport factuel en 4 points :
    - suggestion_sec1 (Les Faits Allégués) : 
      Résumé neutre : "Le [Date], X a déclaré sous serment que..."
    - suggestion_sec2 (La Preuve Contraire) : 
      Démonstration technique : "Cette affirmation est contredite par la pièce P-Y (Courriel du [Date]). Dans ce document, on lit explicitement : '[Citation]'."
    - suggestion_sec3 (L'Élément Intentionnel / Mens Rea) : 
      Raisonnement déductif : "L'intention est démontrée par le fait que l'auteur possédait la preuve contraire."
    - suggestion_sec4 (Le Mobile / Intention Stratégique) : 
      Constat de bénéfice : "Cette fausse représentation a eu pour effet de [Masquer un actif / Obtenir un délai / Créer un préjudice]."
    """)
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro-latest')
        response = model.generate_content(prompt_sequence)
        cleaned_text = response.text.replace('```json', '').replace('```', '').strip()
        data_dict = json.loads(cleaned_text)
        AISuggestion.objects.create(
            contestation=contestation,
            content=data_dict
        )
        messages.success(request, "Suggestion AI générée avec succès !")
    except json.JSONDecodeError:
        print(f"Invalid JSON received: {response.text}")
        messages.error(request, "L'IA a répondu, mais le format n'était pas du JSON valide.")
    except Exception as e:
        print(f"AI Gen Error: {e}")
        messages.error(request, f"Erreur : {e}")
    return redirect('case_manager:contestation_detail', pk=contestation.pk)
