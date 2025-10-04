import os
from django.views.generic import View
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Email

class DownloadEmlView(View):
    """Handles the secure download of a saved .eml file."""
    def get(self, request, *args, **kwargs):
        email_pk = kwargs.get('pk')
        email = get_object_or_404(Email, pk=email_pk)

        if not email.eml_file_path or not os.path.exists(email.eml_file_path):
            raise Http404("EML file not found.")

        response = FileResponse(open(email.eml_file_path, 'rb'), as_attachment=True)
        return response
