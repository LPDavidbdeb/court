from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
import json
from .models import LegalCase, PerjuryContestation, AISuggestion
from .forms import LegalCaseForm, PerjuryContestationForm

def serialize_evidence(evidence_pool):
    """
    Serializes a pool of evidence objects into a JSON structure
    suitable for the TinyMCE custom inserter plugin.
    """
    serialized_data = []
    
    # Example for events
    if evidence_pool.get('events'):
        event_menu = []
        for event in evidence_pool['events']:
            event_menu.append({
                'title': f'Event: {event.date} - {event.explanation[:50]}...',
                'value': f'<blockquote><p>{event.explanation}</p><cite>Event on {event.date}</cite></blockquote>'
            })
        if event_menu:
            serialized_data.append({'title': 'Events', 'menu': event_menu})

    # Example for email quotes
    if evidence_pool.get('emails'):
        email_menu = []
        for quote in evidence_pool['emails']:
            email_menu.append({
                'title': f'Email Quote: {quote.quote_text[:50]}...',
                'value': f'<blockquote><p>{quote.quote_text}</p><cite>Email from {quote.email.sender} on {quote.email.date_sent}</cite></blockquote>'
            })
        if email_menu:
            serialized_data.append({'title': 'Email Quotes', 'menu': email_menu})

    # Add other evidence types (PDFs, etc.) here following the same pattern...

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

class PerjuryContestationDetailView(DetailView):
    model = PerjuryContestation
    template_name = 'case_manager/perjurycontestation_detail.html'
    context_object_name = 'contestation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Load Evidence for the Sidebar/Plugin
        evidence_pool = {
            'events': [],
            'emails': [],
            'pdfs': [],
        }
        for narrative in self.object.supporting_narratives.all():
            evidence_pool['events'].extend(narrative.evenements.all())
            evidence_pool['emails'].extend(narrative.citations_courriel.all())
            evidence_pool['pdfs'].extend(narrative.citations_pdf.all())
            
        context['evidence_json'] = serialize_evidence(evidence_pool)
        
        # 2. Load AI Suggestions
        context['ai_drafts'] = self.object.ai_suggestions.order_by('-created_at')
        
        return context

def generate_ai_suggestion(request, contestation_pk):
    """
    Placeholder view to generate a new AI suggestion for a contestation.
    """
    contestation = get_object_or_404(PerjuryContestation, pk=contestation_pk)
    
    # In a real scenario, you would:
    # 1. Gather all context (targeted statements, evidence text).
    # 2. Send it to the Gemini API.
    # 3. Get the 4-part response.
    
    # For now, we create a dummy suggestion.
    dummy_text = f"This is a dummy AI suggestion generated at {timezone.now().strftime('%H:%M:%S')}."
    AISuggestion.objects.create(
        contestation=contestation,
        suggestion_sec1=f"Dummy Declaration: {dummy_text}",
        suggestion_sec2=f"Dummy Proof: {dummy_text}",
        suggestion_sec3=f"Dummy Mens Rea: {dummy_text}",
        suggestion_sec4=f"Dummy Intent: {dummy_text}",
    )
    
    return redirect('case_manager:contestation_detail', pk=contestation.pk)
