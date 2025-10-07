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

import json
import bleach
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render
from django.db.models import Q, Prefetch
from email_manager.models import Email, EmailThread, Quote as EmailQuote
from events.models import Event

# THIS IS THE DIAGNOSTIC FIX: Add a dummy function to prevent server crash
def ajax_search_emails(request):
    """A dummy view to prevent server startup errors. This is not used."""
    return JsonResponse({'emails': []})

class TrameNarrativeListView(ListView):
    model = TrameNarrative
    template_name = 'argument_manager/tiamenarrative_list.html'
    context_object_name = 'narratives'

class TrameNarrativeDetailView(DetailView):
    model = TrameNarrative
    template_name = 'argument_manager/tiamenarrative_detail.html'
    context_object_name = 'narrative'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        narrative = self.get_object()
        allegations = narrative.allegations_ciblees.all()
        allegation_ids = [str(allegation.pk) for allegation in allegations]
        context['highlight_ids'] = ",".join(allegation_ids)
        allegations_with_docs = []
        for allegation in allegations:
            ancestors = allegation.get_ancestors()
            correct_document = next((ancestor for ancestor in ancestors if ancestor.depth == 2), None)
            if correct_document:
                allegations_with_docs.append((allegation, correct_document.pk))
            else:
                allegations_with_docs.append((allegation, None))
        context['allegations_with_docs'] = allegations_with_docs
        return context

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

    def form_valid(self, form):
        response = super().form_valid(form)
        selected_events_str = self.request.POST.get('selected_events', '')
        if selected_events_str:
            event_ids = selected_events_str.split(',')
            self.object.evenements.set(event_ids)
        else:
            self.object.evenements.clear()
        return response

class TrameNarrativeDeleteView(DeleteView):
    model = TrameNarrative
    template_name = 'argument_manager/tiamenarrative_confirm_delete.html'
    context_object_name = 'narrative'
    success_url = reverse_lazy('argument_manager:list')

@require_POST
def ajax_update_summary(request, narrative_pk):
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        data = json.loads(request.body)
        new_summary = data.get('resume')
        if new_summary is not None:
            narrative.resume = bleach.clean(new_summary)
            narrative.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'No summary provided.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

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

@require_POST
def ajax_update_narrative_events(request, narrative_pk):
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        data = json.loads(request.body)
        event_ids = data.get('event_ids', [])
        narrative.evenements.set(event_ids)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def ajax_get_email_quotes_list(request):
    quotes = EmailQuote.objects.order_by('-created_at')
    return render(request, 'argument_manager/_email_quote_selection_list.html', {'quotes': quotes})

@require_POST
def ajax_update_narrative_email_quotes(request, narrative_pk):
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        data = json.loads(request.body)
        quote_ids = data.get('quote_ids', [])
        narrative.citations_courriel.set(quote_ids)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def ajax_get_email_threads(request):
    threads = EmailThread.objects.prefetch_related(
        Prefetch('emails', queryset=Email.objects.order_by('date_sent'))
    )
    processed_threads = []
    for thread in threads:
        first_email = thread.emails.first()
        if not first_email:
            continue
        participants = set()
        for email in thread.emails.all():
            participants.add(email.sender)
        processed_threads.append({
            'pk': thread.pk,
            'subject': thread.subject,
            'first_email_date': first_email.date_sent,
            'participants': ", ".join(filter(None, participants)),
        })
    sorted_threads = sorted(processed_threads, key=lambda t: t['first_email_date'], reverse=True)
    return render(request, 'argument_manager/_thread_list.html', {'threads': sorted_threads})

def ajax_get_thread_emails(request, thread_pk):
    thread = get_object_or_404(EmailThread, pk=thread_pk)
    emails = thread.emails.order_by('date_sent')
    return render(request, 'argument_manager/_email_accordion.html', {'emails': emails})
