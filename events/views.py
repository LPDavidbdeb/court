import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View
)
from django.urls import reverse_lazy
from .models import Event

# ==============================================================================
# AJAX View for Inline Editing
# ==============================================================================
class ExplanationUpdateAPIView(View):
    """
    Handles the AJAX POST request to update the explanation for an event.
    """
    def post(self, request, *args, **kwargs):
        try:
            event = get_object_or_404(Event, pk=kwargs.get('pk'))
            data = json.loads(request.body)
            new_explanation = data.get('explanation')

            if new_explanation is None:
                return JsonResponse({'success': False, 'error': 'No explanation provided.'}, status=400)

            event.explanation = new_explanation.strip()
            event.save()

            return JsonResponse({'success': True, 'explanation': event.explanation})
        
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ==============================================================================
# Standard Class-Based Views
# ==============================================================================

class EventListView(ListView):
    model = Event
    template_name = 'SupportingEvidence/supportingevidence_list.html'
    context_object_name = 'event_list'

class EventDetailView(DetailView):
    model = Event
    template_name = 'SupportingEvidence/supportingevidence_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_event = self.get_object()

        # Get next event
        next_event = Event.objects.filter(pk__gt=current_event.pk).order_by('pk').first()
        context['next_event'] = next_event

        # Get previous event
        previous_event = Event.objects.filter(pk__lt=current_event.pk).order_by('-pk').first()
        context['previous_event'] = previous_event

        return context

class EventCreateView(CreateView):
    model = Event
    fields = [
        'parent',
        'allegation',
        'date',
        'explanation',
        'linked_photos',
        'linked_email',
        'email_quote',
    ]
    template_name = 'SupportingEvidence/supportingevidence_form.html'
    success_url = reverse_lazy('events:list')

class EventUpdateView(UpdateView):
    model = Event
    fields = [
        'parent',
        'allegation',
        'date',
        'explanation',
        'linked_photos',
        'linked_email',
        'email_quote',
    ]
    template_name = 'SupportingEvidence/supportingevidence_form.html'
    context_object_name = 'event'
    success_url = reverse_lazy('events:list')

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'SupportingEvidence/supportingevidence_confirm_delete.html'
    context_object_name = 'event'
    success_url = reverse_lazy('events:list')
