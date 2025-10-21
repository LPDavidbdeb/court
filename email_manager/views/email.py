import os
import json
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, View
from django.contrib import messages
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from ..models import Email, Quote
from ..forms import EmlUploadForm, QuoteForm
from ..utils import import_eml_file


class EmailDetailView(DetailView):
    """
    Displays the details of a single email message.
    """
    model = Email
    template_name = 'email_manager/email_detail.html'
    context_object_name = 'email'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quote_form'] = QuoteForm() # Add an empty form for new quotes
        return context


class DownloadEmlView(View):
    """Handles the secure download of a saved .eml file."""

    def get(self, request, *args, **kwargs):
        email_pk = kwargs.get('pk')
        email = get_object_or_404(Email, pk=email_pk)

        if not email.eml_file_path or not os.path.exists(email.eml_file_path):
            raise Http404("EML file not found.")

        response = FileResponse(open(email.eml_file_path, 'rb'), as_attachment=True)
        return response


class EmailPrintableView(DetailView):
    model = Email
    template_name = 'email_manager/email/printable_detail.html'
    context_object_name = 'email'


class EmlUploadView(FormView):
    template_name = 'email_manager/email/upload.html'
    form_class = EmlUploadForm

    def form_valid(self, form):
        eml_file = form.cleaned_data['eml_file']
        protagonist = form.cleaned_data.get('protagonist')
        try:
            email_obj = import_eml_file(eml_file, linked_protagonist=protagonist)
            messages.success(self.request, f"Successfully imported email: {email_obj.subject}")
            return redirect('email_manager:thread_detail', pk=email_obj.thread.pk)
        except Exception as e:
            messages.error(self.request, f"Failed to import EML file: {e}")
            return super().form_invalid(form)


# --- Quote Creation and AJAX Update Views ---
def create_email_quote(request, pk):
    email = get_object_or_404(Email, pk=pk)
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.email = email
            quote.save()
            messages.success(request, "Quote created successfully.")
            return redirect('email_manager:email_detail', pk=email.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    return redirect('email_manager:email_detail', pk=email.pk)

@require_POST
def ajax_update_email_quote(request, pk):
    try:
        quote = get_object_or_404(Quote, pk=pk)
        data = json.loads(request.body)
        new_text = data.get('quote_text', '')

        quote.quote_text = new_text
        quote.save(update_fields=['quote_text'])

        return JsonResponse({
            'success': True,
            'quote_text': quote.quote_text
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
