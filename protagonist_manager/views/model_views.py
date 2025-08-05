from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy  # For class-based views or redirects after success
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages  # For displaying messages to the user

from ..models import Protagonist, ProtagonistEmail
from ..forms.protagonist_form import ProtagonistForm, ProtagonistEmailForm


# --- List View ---
class ProtagonistListView(ListView):
    """
    Displays a list of all protagonists.
    """
    model = Protagonist
    template_name = 'protagonist_manager/protagonist_list.html'
    context_object_name = 'protagonists'  # The variable name to use in the template
    paginate_by = 100  # Optional: Add pagination


# --- Detail View ---
class ProtagonistDetailView(DetailView):
    """
    Displays the details of a single protagonist.
    """
    model = Protagonist
    template_name = 'protagonist_manager/protagonist_detail.html'
    context_object_name = 'protagonist'  # The variable name to use in the template


# --- Create View ---
class ProtagonistCreateView(CreateView):
    """
    Handles creation of a new protagonist.
    """
    model = Protagonist
    form_class = ProtagonistForm
    template_name = 'protagonist_manager/protagonist_form.html'
    success_url = reverse_lazy('protagonist_manager:protagonist_list')  # Redirect to list after creation

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Protagonist '{self.object.get_full_name()}' created successfully!")
        return response


# --- Update View ---
class ProtagonistUpdateView(UpdateView):
    """
    Handles updating an existing protagonist.
    """
    model = Protagonist
    form_class = ProtagonistForm
    template_name = 'protagonist_manager/protagonist_form.html'
    context_object_name = 'protagonist'  # For pre-populating the form

    def get_success_url(self):
        # Redirect to the detail page of the updated protagonist
        messages.success(self.request, f"Protagonist '{self.object.get_full_name()}' updated successfully!")
        return reverse_lazy('protagonist_manager:protagonist_detail', kwargs={'pk': self.object.pk})


# --- Delete View ---
class ProtagonistDeleteView(DeleteView):
    """
    Handles deletion of a protagonist.
    """
    model = Protagonist
    template_name = 'protagonist_manager/protagonist_confirm_delete.html'  # A confirmation template
    success_url = reverse_lazy('protagonist_manager:protagonist_list')  # Redirect to list after deletion
    context_object_name = 'protagonist'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Protagonist '{self.object.get_full_name()}' deleted successfully!")
        return response

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, f"Protagonist '{self.object.get_full_name()}' deleted successfully.")
            return HttpResponseRedirect(success_url)
        except Exception as e:
            messages.error(self.request, f"Error deleting protagonist '{self.object.get_full_name()}': {e}")
            return HttpResponseRedirect(self.object.get_absolute_url())  # Redirect back to detail on error


# --- Protagonist Email Management Views ---

class ProtagonistEmailCreateView(CreateView):
    """
    Handles adding a new email address to a specific protagonist.
    """
    model = ProtagonistEmail
    form_class = ProtagonistEmailForm
    template_name = 'protagonist_manager/protagonist_email_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.protagonist = get_object_or_404(Protagonist, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protagonist'] = self.protagonist
        return context

    def form_valid(self, form):
        form.instance.protagonist = self.protagonist
        response = super().form_valid(form)
        messages.success(self.request,
                         f"Email '{self.object.email_address}' added to {self.protagonist.get_full_name()}.")
        return response

    def get_success_url(self):
        return reverse_lazy('protagonist_manager:protagonist_detail', kwargs={'pk': self.protagonist.pk})


class ProtagonistEmailDeleteView(DeleteView):
    """
    Handles deleting a specific email address from a protagonist.
    """
    model = ProtagonistEmail
    template_name = 'protagonist_manager/protagonist_email_confirm_delete.html'
    context_object_name = 'protagonist_email'

    def dispatch(self, request, *args, **kwargs):
        self.protagonist = get_object_or_404(Protagonist, pk=self.kwargs['protagonist_pk'])
        self.object = self.get_object()  # Ensure the email belongs to the correct protagonist if needed
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protagonist'] = self.protagonist
        return context

    def get_success_url(self):
        messages.success(self.request,
                         f"Email '{self.object.email_address}' deleted from {self.protagonist.get_full_name()}.")
        return reverse_lazy('protagonist_manager:protagonist_detail', kwargs={'pk': self.protagonist.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
            return HttpResponseRedirect(success_url)
        except Exception as e:
            messages.error(self.request, f"Error deleting email '{self.object.email_address}': {e}")
            return HttpResponseRedirect(
                self.protagonist.get_absolute_url())  # Redirect back to protagonist detail on error

