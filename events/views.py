from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
from .models import Event

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    # ADDED: Custom context for next/previous navigation
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_event = self.get_object()

        # Find the next event (ordering by date and then by pk as a tie-breaker)
        next_event = Event.objects.filter(date__gt=current_event.date).order_by('date', 'pk').first()
        if not next_event:
            # If no event on a later date, check for a later event on the same date
            next_event = Event.objects.filter(date=current_event.date, pk__gt=current_event.pk).order_by('pk').first()

        # Find the previous event
        prev_event = Event.objects.filter(date__lt=current_event.date).order_by('-date', '-pk').first()
        if not prev_event:
            # If no event on an earlier date, check for an earlier event on the same date
            prev_event = Event.objects.filter(date=current_event.date, pk__lt=current_event.pk).order_by('-pk').first()

        context['next_event'] = next_event
        context['prev_event'] = prev_event
        return context

class EventCreateView(CreateView):
    model = Event
    template_name = 'events/event_form.html'
    fields = ['date', 'explanation', 'allegation', 'linked_email', 'linked_photos', 'parent']
    success_url = reverse_lazy('events:list')

class EventUpdateView(UpdateView):
    model = Event
    template_name = 'events/event_form.html'
    fields = ['date', 'explanation', 'allegation', 'linked_email', 'linked_photos', 'parent']
    success_url = reverse_lazy('events:list')

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    context_object_name = 'event'
    success_url = reverse_lazy('events:list')

@require_POST
def ajax_update_explanation(request, pk):
    try:
        event = get_object_or_404(Event, pk=pk)
        data = json.loads(request.body)
        new_explanation = data.get('explanation', '')

        event.explanation = new_explanation
        event.save(update_fields=['explanation'])

        return JsonResponse({
            'success': True,
            'explanation': event.explanation
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
