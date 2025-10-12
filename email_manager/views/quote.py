from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DeleteView, UpdateView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages

from ..models import Email, Quote
from ..forms import QuoteForm


class QuoteListView(ListView):
    """
    Displays a list of all Emails that have Quotes, ordered by the email's sent date.
    The quotes are grouped by their source email.
    """
    model = Email
    template_name = 'email_manager/quote/list.html'
    context_object_name = 'emails_with_quotes'

    def get_queryset(self):
        """
        Returns a queryset of emails that have at least one quote, ordered by date,
        with quotes prefetched for efficiency.
        """
        return Email.objects.filter(quotes__isnull=False).distinct().order_by('-date_sent').prefetch_related('quotes__trames_narratives')


class QuoteUpdateView(UpdateView):
    """
    Handles updating the narrative associations for a single Quote.
    """
    model = Quote
    form_class = QuoteForm
    template_name = 'email_manager/quote/update.html'
    success_url = reverse_lazy('email_manager:quote_list')

    def get_initial(self):
        """Pre-select the narratives currently associated with the quote."""
        initial = super().get_initial()
        # The reverse relationship from Quote to TrameNarrative is 'trames_narratives'
        initial['trames_narratives'] = self.object.trames_narratives.all()
        return initial

    def get_form(self, form_class=None):
        """Make the quote_text field readonly to focus on narrative association."""
        form = super().get_form(form_class)
        form.fields['quote_text'].widget.attrs['readonly'] = True
        return form

    def form_valid(self, form):
        """Manually save the ManyToMany relationship."""
        self.object = form.save()
        # Get the selected narratives from the form and set them
        self.object.trames_narratives.set(form.cleaned_data['trames_narratives'])
        messages.success(self.request, "The quote's narrative associations have been updated successfully.")
        return super().form_valid(form)


class QuoteDeleteView(DeleteView):
    """
    Handles the deletion of a single Quote object.
    """
    model = Quote
    success_url = reverse_lazy('email_manager:quote_list')

    def form_valid(self, form):
        messages.success(self.request, "The quote has been deleted successfully.")
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        """Override get to redirect to post for immediate deletion."""
        return self.post(request, *args, **kwargs)


class AddQuoteView(View):
    """
    Handles adding a quote from an email via a modal form.
    """

    def get(self, request, *args, **kwargs):
        email_id = kwargs.get('email_pk')
        email = get_object_or_404(Email, pk=email_id)
        form = QuoteForm()
        return render(request, 'email_manager/quote/partials/add_quote_modal.html', {
            'email': email,
            'form': form
        })

    def post(self, request, *args, **kwargs):
        email_id = kwargs.get('email_pk')
        email = get_object_or_404(Email, pk=email_id)
        form = QuoteForm(request.POST)

        if form.is_valid():
            quote = form.save(commit=False)
            quote.email = email
            quote.save()
            # Manually save the ManyToMany relationship for the new quote
            quote.trames_narratives.set(form.cleaned_data['trames_narratives'])
            return JsonResponse({'status': 'success', 'message': 'Quote saved successfully!'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors.as_json()}, status=400)
