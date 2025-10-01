from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView
from django.http import JsonResponse
from .models import Email, Quote, EmailThread
from .forms import QuoteForm

class AddQuoteView(View):
    """
    Handles adding a quote from an email via a modal form.
    """
    def get(self, request, *args, **kwargs):
        email_id = kwargs.get('email_pk')
        email = get_object_or_404(Email, pk=email_id)
        form = QuoteForm()
        return render(request, 'email_manager/partials/add_quote_modal.html', {
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
            form.save_m2m()  # Necessary for ManyToMany fields
            return JsonResponse({'status': 'success', 'message': 'Quote saved successfully!'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors.as_json()}, status=400)

class EmailThreadListView(ListView):
    """
    Displays a list of all saved email threads.
    """
    model = EmailThread
    template_name = 'email_manager/email_list.html'
    context_object_name = 'threads'
    paginate_by = 10
