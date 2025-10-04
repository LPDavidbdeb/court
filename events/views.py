from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
from .models import Event

# NEW IMPORTS for the AJAX view
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'  # Corrected template path
    context_object_name = 'events'

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

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

# ADDED: View to handle the AJAX request for inline editing
@require_POST
def ajax_update_explanation(request, pk):
    """
    Handles AJAX requests to update the explanation of an Event.
    """
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
