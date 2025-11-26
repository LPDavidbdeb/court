from django.views.generic import ListView, DetailView, CreateView, View
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.conf import settings
import json
import google.generativeai as genai
import docx
import io

from .models import LegalCase, PerjuryContestation, AISuggestion
from .forms import LegalCaseForm, PerjuryContestationForm
from .services import refresh_case_exhibits
from ai_services.utils import EvidenceFormatter

def serialize_evidence(evidence_pool):
    """
    Serializes a pool of evidence objects into a JSON structure
    suitable for the TinyMCE custom inserter plugin.
    """
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

# --- LegalCase Views ---

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

        # Add Contestations
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

        # Add Exhibit Table
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
            
            if hasattr(obj, 'date'):
                row_cells[2].text = str(obj.date)
            elif hasattr(obj, 'date_sent'):
                row_cells[2].text = str(obj.date_sent.date())
            elif hasattr(obj, 'document_date') and obj.document_date:
                row_cells[2].text = str(obj.document_date)
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

# --- PerjuryContestation Views ---

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
    
    # 1. Prepare the Lies
    lies_text = "--- ALLÉGATIONS MENSONGÈRES À CONTESTER ---\n"
    for stmt in contestation.targeted_statements.all():
        lies_text += f"- « {stmt.text} »\n"

    # 2. Build the Prompt Sequence
    prompt_sequence = [
        f"""
        RÔLE : Expert juridique en litige familial.
        OBJECTIF : Rédiger une contestation de parjure formelle.
        
        INSTRUCTIONS D'ANALYSE :
        1. Tu vas recevoir une chronologie mixte de textes et d'images.
        2. Note spécifiquement les ROLES des personnes impliquées (ex: si une avocate ou un juge contredit la mère).
        3. Si une image est fournie, décris ce qu'elle prouve.
        
        {lies_text}
        
        --- DÉBUT DES PREUVES ---
        """
    ]

    # 3. Inject the Multimodal Narrative
    for narrative in contestation.supporting_narratives.all():
        narrative_content = EvidenceFormatter.unpack_narrative_multimodal(narrative)
        prompt_sequence.extend(narrative_content)

    # 4. Add Final Instructions
    prompt_sequence.append("""
    --- FIN DES PREUVES ---
    
    TÂCHE : 
    Rédige la réponse au format JSON strict avec 4 clés :
    - suggestion_sec1 (Déclaration) : Le contexte du mensonge.
    - suggestion_sec2 (Preuve) : L'argumentation factuelle. CITE les dates, les rôles (ex: "L'avocate a confirmé...") et le contenu des images.
    - suggestion_sec3 (Mens Rea) : Pourquoi, vu son rôle ou sa présence (prouvée par l'image/email), la personne NE POUVAIT PAS ignorer la vérité.
    - suggestion_sec4 (Intention) : Quel avantage stratégique elle visait.
    """)

    # 5. Call Gemini
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        response = model.generate_content(prompt_sequence)
        
        cleaned_text = response.text.replace('```json', '').replace('```', '').strip()
        data = json.loads(cleaned_text)
        
        AISuggestion.objects.create(
            contestation=contestation,
            suggestion_sec1=data.get('suggestion_sec1', ''),
            suggestion_sec2=data.get('suggestion_sec2', ''),
            suggestion_sec3=data.get('suggestion_sec3', ''),
            suggestion_sec4=data.get('suggestion_sec4', ''),
        )
        
    except Exception as e:
        print(f"AI Gen Error: {e}")

    return redirect('case_manager:contestation_detail', pk=contestation.pk)
