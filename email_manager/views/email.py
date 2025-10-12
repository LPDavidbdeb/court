import os
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, View
from django.contrib import messages
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect

from ..models import Email
from ..forms import EmlUploadForm
from ..utils import import_eml_file


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
