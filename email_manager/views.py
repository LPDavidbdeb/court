# Merged imports from both versions
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, FormView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse, FileResponse, Http404

# Models from both versions
from .models import Email, EmailThread, Quote
# Forms from both versions
from .forms import EmlUploadForm, EmailSearchForm, QuoteForm
# Utils from the main branch
from .utils import import_eml_file, search_gmail


# ==============================================================================
# NEW: EML File Download View
# ==============================================================================
class DownloadEmlView(View):
    """Handles the secure download of a saved .eml file."""
    def get(self, request, *args, **kwargs):
        email_pk = kwargs.get('pk')
        email = get_object_or_404(Email, pk=email_pk)

        if not email.eml_file_path or not os.path.exists(email.eml_file_path):
            raise Http404("EML file not found.")

        # Use FileResponse to stream the file, which is memory-efficient
        # as_attachment=True triggers the browser's download dialog
        response = FileResponse(open(email.eml_file_path, 'rb'), as_attachment=True)
        return response

# ==============================================================================
# Printable Detail View (from main branch)
# ==============================================================================
class EmailPrintableView(DetailView):
    model = Email
    template_name = 'email_manager/email_printable_detail.html'
    context_object_name = 'email'

# ==============================================================================
# Main Views
# ==============================================================================

# Use the more modern Thread-based list view
class EmailThreadListView(ListView):
    model = EmailThread
    template_name = 'email_manager/email_list.html'
    context_object_name = 'threads'
    paginate_by = 10

# Modify the DetailView to be Thread-based to support the quoting feature
class EmailDetailView(DetailView):
    model = EmailThread
    template_name = 'email_manager/email_detail.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thread = self.get_object()
        context['emails_in_thread'] = thread.emails.all().order_by('date_sent')
        # Add the QuoteForm to the context to ensure the modal renders correctly
        context['form'] = QuoteForm()
        return context

# Kept from main branch
class EmlUploadView(FormView):
    template_name = 'email_manager/eml_upload_form.html'
    form_class = EmlUploadForm
    success_url = reverse_lazy('email_manager:email_list')

    def form_valid(self, form):
        eml_file = self.request.FILES['eml_file']
        try:
            email_obj = import_eml_file(eml_file)
            messages.success(self.request, f"Successfully imported email: {email_obj.subject}")
        except Exception as e:
            messages.error(self.request, f"Failed to import EML file: {e}")
        return super().form_valid(form)

# Kept from main branch
class EmailSearchView(FormView):
    template_name = 'email_manager/email_search.html'
    form_class = EmailSearchForm

    def form_valid(self, form):
        query = form.cleaned_data['query']
        max_results = form.cleaned_data['max_results']
        try:
            results = search_gmail(query, max_results)
            messages.success(self.request, f"Successfully fetched {len(results)} threads from Gmail.")
            return redirect('email_manager:email_list')
        except Exception as e:
            messages.error(self.request, f"Failed to search Gmail: {e}")
            return redirect('email_manager:email_search')

# Added the new AJAX view for the quote modal
class AddQuoteView(View):
    def post(self, request, *args, **kwargs):
        email_id = kwargs.get('email_pk')
        email = get_object_or_404(Email, pk=email_id)
        form = QuoteForm(request.POST)

        if form.is_valid():
            quote = form.save(commit=False)
            quote.email = email
            quote.save()
            form.save_m2m()
            return JsonResponse({'status': 'success', 'message': 'Quote saved successfully!'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors.as_json()}, status=400)
