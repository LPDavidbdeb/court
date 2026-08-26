from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, DeleteView, UpdateView, DetailView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme

from argument_manager.mixins import EvidenceDeleteMixin
from argument_manager.models import TrameNarrative
from core.text_matching import order_by_position

from ..models import Email, Quote
from ..forms import QuoteForm


class QuoteDetailView(DetailView):
    """
    Displays the details of a single email quote.
    """
    model = Quote
    template_name = 'email_manager/quote_detail.html'
    context_object_name = 'quote'


class QuoteListView(ListView):
    """
    Displays a list of all Emails that have Quotes, ordered by the email's sent date.
    The quotes are grouped by their source email.
    """
    model = Email
    template_name = 'email_manager/quote/list.html'
    context_object_name = 'emails_with_quotes'
    # 25 emails rather than the 100 used by the photo and protagonist lists: a
    # row here carries the quote text itself, up to ~1300 characters, where
    # those lists carry a name and a date.
    paginate_by = 25

    def get_queryset(self):
        """
        Returns a queryset of emails that have at least one quote, ordered by date,
        with quotes prefetched for efficiency.

        'thread' is select_related because the template links every row to the
        source thread; without it the page costs one query per email.
        """
        return (
            Email.objects.filter(quotes__isnull=False)
            .distinct()
            .select_related('thread')
            .order_by('-date_sent')
            .prefetch_related('quotes__trames_narratives')
        )

    def get_context_data(self, **kwargs):
        """
        Attach each email's quotes in the order they appear in the email body.

        Quote.Meta.ordering is ['-created_at'], so the related manager hands the
        template quotes newest-extracted first — roughly backwards relative to
        the document, and inconsistent with the exhibits, which
        case_manager/exhibit_service.py already sorts by position_in_source.
        This page now uses the same key.

        position_in_source is a Python property, not a column, so it cannot go
        in order_by() and the sort has to happen here. That is affordable only
        because the page is paginated: this runs over one page of emails, not
        all 158. The quotes are already in the prefetch cache, and prefetching a
        reverse FK populates quote.email, so neither the sort nor the property's
        read of body_plain_text costs a query.
        """
        context = super().get_context_data(**kwargs)
        page_quotes = []
        for email in context['emails_with_quotes']:
            email.ordered_quotes = order_by_position(email.quotes.all())
            page_quotes.extend(email.ordered_quotes)

        # Deleting a quote deletes the narratives it alone supported, and the
        # Delete button is right here, so the page marks them. Flagged for the
        # whole page at once rather than per email: the cost is the same six
        # queries either way, and per email it would be six per row.
        TrameNarrative.flag_orphans(page_quotes)
        return context


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


class QuoteDeleteView(EvidenceDeleteMixin, DeleteView):
    """
    Handles the deletion of a single Quote object.

    EvidenceDeleteMixin carries the rest: any narrative this quote was the sole
    evidence of is deleted with it.
    """
    model = Quote
    success_url = reverse_lazy('email_manager:quote_list')
    deleted_message = "The quote has been deleted successfully."

    # POST only. Deletion used to happen on GET too, which meant any link
    # follow or prefetch of the delete URL destroyed the quote, with no CSRF
    # token in play. The callers already submit a real POST form, so there is
    # no confirmation page to render and GET has nothing legitimate to do here.
    http_method_names = ['post']

    def get_success_url(self):
        """
        Back where the delete was pressed, not always to the quote list.

        This view is reached from two pages — the list of all quotes and the
        detail of one email — and success_url only ever named the first, which
        threw anyone deleting from an email out of the email. A form may name
        its own page in `next`; anything pointing off this host is ignored
        rather than followed.
        """
        next_url = self.request.POST.get('next')
        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        ):
            return next_url
        return super().get_success_url()


class AddQuoteView(View):
    """
    Handles adding a quote from an email. This view can handle both standard
    form submissions and AJAX requests from a modal.
    """
    form_class = QuoteForm
    template_name = 'email_manager/quote/partials/add_quote_form.html'

    def get(self, request, *args, **kwargs):
        """
        For AJAX requests, returns the form HTML to be loaded into a modal.
        """
        email = get_object_or_404(Email, pk=kwargs.get('email_pk'))
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'email': email})

    def post(self, request, *args, **kwargs):
        """
        Handles both AJAX and standard form submissions for creating a quote.
        """
        email = get_object_or_404(Email, pk=kwargs.get('email_pk'))
        form = self.form_class(request.POST)

        if form.is_valid():
            quote = form.save(commit=False)
            quote.email = email
            quote.save()
            form.save_m2m()  # Save the many-to-many relationships

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Quote saved successfully!'})
            else:
                messages.success(request, 'Quote saved successfully!')
                return redirect('email_manager:email_detail', pk=email.pk)
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'errors': form.errors.as_json()}, status=400)
        else:
            # For standard submissions, re-render the page with the errors
            messages.error(request, 'Please correct the errors below.')
            # We need a full template for this, not just a partial
            # This part of the logic might need to be adjusted depending on where the standard form is.
            # For now, redirecting back to the email detail page.
            return redirect('email_manager:email_detail', pk=email.pk)
