import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
# your_project_root/evidence/email_manager_1.py

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
from .models import SupportingEvidence

class SupportingEvidenceListView(ListView):
    """
    Displays a list of all SupportingEvidence instances.
    """
    model = SupportingEvidence
    template_name = 'supportingevidence/supportingevidence_list.html'
    context_object_name = 'evidences' # Name of the variable in the template

class SupportingEvidenceDetailView(DetailView):
    """
    Displays the details of a single SupportingEvidence instance.
    """
    model = SupportingEvidence
    template_name = 'supportingevidence/supportingevidence_detail.html'
    context_object_name = 'evidence' # Name of the variable in the template

class SupportingEvidenceCreateView(CreateView):
    """
    Handles the creation of a new SupportingEvidence instance.
    """
    model = SupportingEvidence
    # fields = '__all__' # Use '__all__' for all fields, or list them explicitly
    # Excluding 'linked_photos', 'linked_emails', 'linked_pdfs' from direct form as M2M are often handled separately
    # or by specific widgets. For basic forms, including them will make them appear as multi-select boxes.
    # Let's include them for now as Django-Bootstrap5 can render them as multi-selects.
    fields = [
        'start_date',
        'end_date',
        'description',
        'explanation',
        'linked_photos',
        #'linked_emails',
        #'linked_pdfs',
    ]
    template_name = 'supportingevidence/supportingevidence_form.html'
    success_url = reverse_lazy('evidence:list') # Redirect to the list view after successful creation

class SupportingEvidenceUpdateView(UpdateView):
    """
    Handles updating an existing SupportingEvidence instance.
    """
    model = SupportingEvidence
    # fields = '__all__' # Same field considerations as CreateView
    fields = [
        'start_date',
        'end_date',
        'description',
        'explanation',
        'linked_photos',
        # 'linked_emails',
        # 'linked_pdfs',
    ]
    template_name = 'supportingevidence/supportingevidence_form.html'
    context_object_name = 'evidence' # Variable name for the object in the template
    success_url = reverse_lazy('evidence:list') # Redirect to the list view after successful update

class SupportingEvidenceDeleteView(DeleteView):
    """
    Handles deleting an existing SupportingEvidence instance.
    """
    model = SupportingEvidence
    template_name = 'supportingevidence/supportingevidence_confirm_delete.html'
    context_object_name = 'evidence' # Variable name for the object in the template
    success_url = reverse_lazy('evidence:list') # Redirect to the list view after successful deletion

# NEW VIEW FOR AJAX UPDATE
@method_decorator(csrf_exempt, name='dispatch') # Temporarily csrf_exempt for easy testing.
                                                # For production, use csrf_protect or Django's default CSRF handling with Axios/Fetch etc.
                                                # For jQuery, ensure you send the CSRF token. I will show how to include it.
class ExplanationUpdateAPIView(DetailView):
    model = SupportingEvidence

    def post(self, request, *args, **kwargs):
        # The PK of the evidence object is in kwargs (from URL pattern)
        evidence_id = kwargs.get('pk')
        try:
            evidence = SupportingEvidence.objects.get(pk=evidence_id)
        except SupportingEvidence.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Evidence not found.'}, status=404)

        try:
            data = json.loads(request.body)
            new_explanation = data.get('value', '').strip() # Get the new value, default to empty string, strip whitespace
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)

        # Basic validation
        if not isinstance(new_explanation, str):
            return JsonResponse({'status': 'error', 'message': 'Invalid explanation format.'}, status=400)

        # Update and save
        evidence.explanation = new_explanation
        try:
            evidence.full_clean() # Run model's full validation (if you had custom clean methods)
            evidence.save()
            return JsonResponse({'status': 'success', 'message': 'Explanation updated.'})
        except Exception as e: # Catch any other validation or database errors
            return JsonResponse({'status': 'error', 'message': f'Failed to save: {str(e)}'}, status=500)
