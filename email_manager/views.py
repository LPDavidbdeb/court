from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Email
from .forms import EmlUploadForm, EmailSearchForm
from .utils import import_eml_file, search_gmail


# ==============================================================================
# NEW: Printable Detail View
# ==============================================================================
class EmailPrintableView(DetailView):
    """
    A view to display a clean, printable version of a single email.
    """
    model = Email
    template_name = 'email_manager/email_printable_detail.html'
    context_object_name = 'email'

# ==============================================================================
# Standard Views
# ==============================================================================

class EmailListView(ListView):
    model = Email
    template_name = 'email_manager/email_list.html'
    context_object_name = 'emails'
    paginate_by = 50

class EmailDetailView(DetailView):
    model = Email
    template_name = 'email_manager/email_detail.html'
    context_object_name = 'email'

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

class EmailSearchView(FormView):
    template_name = 'email_manager/email_search.html'
    form_class = EmailSearchForm

    def form_valid(self, form):
        query = form.cleaned_data['query']
        max_results = form.cleaned_data['max_results']
        try:
            results = search_gmail(query, max_results)
            # For simplicity, we'll just show a success message.
            # A more advanced implementation would display the results.
            messages.success(self.request, f"Successfully fetched {len(results)} threads from Gmail.")
            return redirect('email_manager:email_list')
        except Exception as e:
            messages.error(self.request, f"Failed to search Gmail: {e}")
            return redirect('email_manager:email_search')
