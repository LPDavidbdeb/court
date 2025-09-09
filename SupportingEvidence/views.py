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
from .models import SupportingEvidence

# ==============================================================================
# CORRECTED: AJAX View for Inline Editing
# ==============================================================================
class ExplanationUpdateAPIView(View):
    """
    Handles the AJAX POST request to update the explanation for a piece of evidence.
    """
    def post(self, request, *args, **kwargs):
        try:
            evidence = get_object_or_404(SupportingEvidence, pk=kwargs.get('pk'))
            data = json.loads(request.body)
            new_explanation = data.get('explanation')

            if new_explanation is None:
                return JsonResponse({'success': False, 'error': 'No explanation provided.'}, status=400)

            evidence.explanation = new_explanation.strip()
            evidence.save()

            return JsonResponse({'success': True, 'explanation': evidence.explanation})
        
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ==============================================================================
# Standard Class-Based Views
# ==============================================================================

class SupportingEvidenceListView(ListView):
    model = SupportingEvidence
    template_name = 'SupportingEvidence/supportingevidence_list.html'
    context_object_name = 'supportingevidence_list'

class SupportingEvidenceDetailView(DetailView):
    model = SupportingEvidence
    template_name = 'SupportingEvidence/supportingevidence_detail.html'
    context_object_name = 'evidence'

class SupportingEvidenceCreateView(CreateView):
    model = SupportingEvidence
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
    success_url = reverse_lazy('SupportingEvidence:list')

class SupportingEvidenceUpdateView(UpdateView):
    model = SupportingEvidence
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
    context_object_name = 'evidence'
    success_url = reverse_lazy('SupportingEvidence:list')

class SupportingEvidenceDeleteView(DeleteView):
    model = SupportingEvidence
    template_name = 'SupportingEvidence/supportingevidence_confirm_delete.html'
    context_object_name = 'evidence'
    success_url = reverse_lazy('SupportingEvidence:list')
