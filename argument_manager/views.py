from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
from .models import TrameNarrative
from .forms import TrameNarrativeForm

# --- NEW IMPORTS FOR AJAX VIEWS ---
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from email_manager.models import Email, Quote as EmailQuote
from events.models import Event
# --- END NEW IMPORTS ---

class TrameNarrativeListView(ListView):
    model = TrameNarrative
    template_name = 'argument_manager/tiamenarrative_list.html'
    context_object_name = 'narratives'

class TrameNarrativeDetailView(DetailView):
    model = TrameNarrative
    template_name = 'argument_manager/tiamenarrative_detail.html'
    context_object_name = 'narrative'

class TrameNarrativeCreateView(CreateView):
    model = TrameNarrative
    form_class = TrameNarrativeForm
    template_name = 'argument_manager/tiamenarrative_form.html'
    success_url = reverse_lazy('argument_manager:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        selected_events_str = self.request.POST.get('selected_events', '')
        if selected_events_str:
            event_ids = selected_events_str.split(',')
            self.object.evenements.set(event_ids)
        return response

class TrameNarrativeUpdateView(UpdateView):
    model = TrameNarrative
    form_class = TrameNarrativeForm
    template_name = 'argument_manager/tiamenarrative_form.html'
    success_url = reverse_lazy('argument_manager:list')

    # ADDED: Custom logic for handling M2M relationships on update
    def form_valid(self, form):
        response = super().form_valid(form)
        selected_events_str = self.request.POST.get('selected_events', '')
        if selected_events_str:
            event_ids = selected_events_str.split(',')
            self.object.evenements.set(event_ids)
        else:
            # If the hidden input is empty, clear the relationship
            self.object.evenements.clear()
        return response

class TrameNarrativeDeleteView(DeleteView):
    model = TrameNarrative
    template_name = 'argument_manager/tiamenarrative_confirm_delete.html'
    context_object_name = 'narrative'
    success_url = reverse_lazy('argument_manager:list')

# --- DYNAMIC WORKBENCH VIEWS ---

def ajax_search_emails(request):
    term = request.GET.get('term', '')
    if len(term) < 3:
        return JsonResponse({'emails': []})
    emails = Email.objects.filter(
        Q(subject__icontains=term) |
        Q(sender__icontains=term) |
        Q(body_plain_text__icontains=term)
    ).order_by('-date_sent')[:20]
    results = [
        {
            'id': email.id,
            'subject': email.subject,
            'sender': email.sender,
            'date': email.date_sent.strftime('%Y-%m-%d'),
            'body': email.body_plain_text or ""
        }
        for email in emails
    ]
    return JsonResponse({'emails': results})

@require_POST
def ajax_add_email_quote(request, narrative_pk):
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        data = json.loads(request.body)
        email_id = data.get('email_id')
        quote_text = data.get('quote_text')
        if not email_id or not quote_text:
            return JsonResponse({'success': False, 'error': 'Email ID and quote text are required.'}, status=400)
        email_obj = get_object_or_404(Email, pk=email_id)
        new_quote = EmailQuote.objects.create(
            email=email_obj,
            quote_text=quote_text
        )
        narrative.citations_courriel.add(new_quote)
        return JsonResponse({
            'success': True,
            'quote': {
                'id': new_quote.id,
                'text': new_quote.quote_text,
                'full_sentence': new_quote.full_sentence
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def ajax_get_events_list(request):
    events = Event.objects.prefetch_related('linked_photos').order_by('-date')
    return render(request, 'argument_manager/_event_selection_list.html', {'events': events})
