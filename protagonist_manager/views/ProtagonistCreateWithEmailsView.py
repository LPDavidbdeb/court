from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View # Import View
from django.contrib import messages
from django.http import HttpResponseRedirect

from ..models import Protagonist, ProtagonistEmail
from ..forms.ProtagonistEmailFormSet import ProtagonistEmailForm

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
        messages.success(self.request, f"Email '{self.object.email_address}' added to {self.protagonist.get_full_name()}.")
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
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protagonist'] = self.protagonist
        return context

    def get_success_url(self):
        messages.success(self.request, f"Email '{self.object.email_address}' deleted from {self.protagonist.get_full_name()}.")
        return reverse_lazy('protagonist_manager:protagonist_detail', kwargs={'pk': self.protagonist.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
            return HttpResponseRedirect(success_url)
        except Exception as e:
            messages.error(self.request, f"Error deleting email '{self.object.email_address}': {e}")
            return HttpResponseRedirect(self.protagonist.get_absolute_url())

