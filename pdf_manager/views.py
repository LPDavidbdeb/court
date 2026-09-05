import os
from collections import OrderedDict
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

from argument_manager.mixins import EvidenceDeleteMixin
from argument_manager.models import TrameNarrative
from core.text_matching import order_by_position
from .models import PDFDocument, PDFDocumentType, Quote
from .forms import PDFDocumentForm, QuoteForm
from protagonist_manager.models import Protagonist
from protagonist_manager.forms import ProtagonistForm

# ==============================================================================
# List and Create Views
# ==============================================================================

def pdf_document_list(request):
    """
    Displays a list of all uploaded PDF documents, grouped by type into tabs,
    with a final tab showing all documents.
    """
    doc_types = PDFDocumentType.objects.all()
    # Pas de order_by ici : Meta.ordering dit déjà '-document_date, -pk', et le
    # répéter sans le pk rendait à la base l'arbitrage des dates identiques —
    # un ordre que la navigation d'une pièce à l'autre ne pouvait plus suivre.
    all_documents = PDFDocument.objects.all()
    
    grouped_documents = OrderedDict()

    for doc_type in doc_types:
        grouped_documents[doc_type.name] = all_documents.filter(document_type=doc_type)

    grouped_documents['All'] = all_documents

    context = {
        'grouped_documents': grouped_documents,
    }
    return render(request, 'pdf_manager/pdf_list.html', context)

def upload_pdf_document(request):
    """
    Handles the upload of a new PDF document.
    """
    if request.method == 'POST':
        form = PDFDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"PDF document '{form.cleaned_data['title']}' uploaded successfully.")
            return redirect('pdf_manager:pdf_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PDFDocumentForm()
    
    protagonist_form = ProtagonistForm()
    return render(request, 'pdf_manager/upload_pdf.html', {'form': form, 'protagonist_form': protagonist_form})

# ==============================================================================
# Detail, Update, and Delete Views
# ==============================================================================

class PDFDocumentDetailView(DetailView):
    """
    Displays the details of a single PDF document.
    """
    model = PDFDocument
    template_name = 'pdf_manager/pdf_detail.html'
    context_object_name = 'document'

    def get_context_data(self, **kwargs):
        """
        Order the quotes as the document reads.

        The template used to iterate document.quotes.all, which falls through to
        Meta.ordering ['-created_at'] and showed the document's own passages in
        reverse order of extraction — the exact reverse of the exhibits, which
        case_manager/exhibit_service.py already sorts by position_in_source. The
        page a reader works from and the exhibit that reaches the court now put
        them in the same order.
        """
        context = super().get_context_data(**kwargs)
        quotes = order_by_position(
            self.object.quotes.prefetch_related('trames_narratives')
        )

        # Deleting a quote also deletes every narrative it leaves without
        # evidence, so the page marks those before the click rather than
        # reporting them after it.
        TrameNarrative.flag_orphans(quotes)

        context['ordered_quotes'] = quotes
        context.update(self.voisins())
        context['onglets'] = [
            {
                'id': 'analyse',
                'titre': 'Analyse',
                'objet': self.object,
                'gabarit': 'core/onglets/analyse.html',
            },
            {
                'id': 'note',
                'titre': 'Notes',
                'objet': self.object,
                'gabarit': 'core/onglets/note.html',
            },
        ]
        return context

    def voisins(self):
        """
        Les deux pièces qui encadrent celle-ci dans la liste.

        Même geste que sur la page d'un fil de courriels : « précédent »
        remonte la liste (pièce plus récente), « suivant » la descend (pièce
        plus ancienne). L'ordre parcouru est celui de Meta.ordering, donc
        celui-là même qu'affiche l'onglet « All » de la liste.

        On lit la suite des identifiants plutôt que d'aller chercher chaque
        voisin par comparaison de dates : une seule colonne pour une centaine
        de pièces, et surtout l'ordre affiché et l'ordre parcouru ne peuvent
        pas diverger — ex aequo et dates absentes compris, deux cas où une
        comparaison `document_date__gt` saute des pièces ou n'en trouve
        aucune.
        """
        ordre = list(PDFDocument.objects.values_list('pk', flat=True))
        rang = ordre.index(self.object.pk)

        pk_precedent = ordre[rang - 1] if rang > 0 else None
        pk_suivant = ordre[rang + 1] if rang + 1 < len(ordre) else None

        voisins = PDFDocument.objects.in_bulk(
            [pk for pk in (pk_precedent, pk_suivant) if pk is not None]
        )
        return {
            'document_precedent': voisins.get(pk_precedent),
            'document_suivant': voisins.get(pk_suivant),
        }


class PDFDocumentUpdateView(UpdateView):
    """
    Allows editing the details of a PDF document.
    """
    model = PDFDocument
    form_class = PDFDocumentForm
    template_name = 'pdf_manager/pdf_form.html'
    context_object_name = 'document'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protagonist_form'] = ProtagonistForm()
        return context

    def get_success_url(self):
        messages.success(self.request, "PDF document details updated successfully.")
        return reverse_lazy('pdf_manager:pdf_detail', kwargs={'pk': self.object.pk})

class PDFDocumentDeleteView(DeleteView):
    """
    Handles the deletion of a PDF document and its associated file.
    """
    model = PDFDocument
    template_name = 'pdf_manager/pdf_confirm_delete.html'
    context_object_name = 'document'
    success_url = reverse_lazy('pdf_manager:pdf_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.file and os.path.isfile(self.object.file.path):
            os.remove(self.object.file.path)
        messages.success(request, f"PDF document '{self.object.title}' deleted successfully.")
        return super().post(request, *args, **kwargs)

def create_pdf_quote(request, pk):
    document = get_object_or_404(PDFDocument, pk=pk)
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.pdf_document = document
            quote.save()
            messages.success(request, "Quote created successfully.")
            return redirect('pdf_manager:pdf_detail', pk=document.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    return redirect('pdf_manager:pdf_detail', pk=document.pk)

class QuoteDetailView(DetailView):
    """
    Displays the details of a single PDF quote.
    """
    model = Quote
    template_name = 'pdf_manager/quote_detail.html'
    context_object_name = 'quote'


class QuoteDeleteView(EvidenceDeleteMixin, DeleteView):
    """
    Deletes a single quote and returns to the document it was taken from.

    Same shape as email_manager.views.quote.QuoteDeleteView: POST only, with no
    confirmation page of its own. Deletion on GET would mean any link follow or
    prefetch of this URL destroys the quote, with no CSRF token in play; the
    caller submits a real form, so GET has nothing legitimate to do here.

    Deleting a quote drops it from every TrameNarrative that cites it, and any
    narrative it was the sole evidence of is deleted along with it: a narrative
    with nothing left to stand on is not an argument, only its own title. The
    narratives at stake are shown next to the button in pdf_detail.html, the
    doomed ones marked as such, so the consequence is visible before the click.
    """
    model = Quote
    http_method_names = ['post']
    deleted_message = "Quote deleted successfully."

    def get_success_url(self):
        # Called before the delete (BaseDeleteView.form_valid), so the parent
        # document is still reachable from the object.
        return reverse_lazy('pdf_manager:pdf_detail', kwargs={'pk': self.object.pdf_document_id})

# ==============================================================================
# AJAX Views
# ==============================================================================

def ajax_get_pdf_metadata(request, doc_pk):
    document = get_object_or_404(PDFDocument, pk=doc_pk)
    data = {
        'title': document.title,
        'author_name': document.author.get_full_name() if document.author else None,
        'document_date': document.document_date.strftime('%Y-%m-%d') if document.document_date else None,
    }
    return JsonResponse(data)

def author_search_view(request):
    term = request.GET.get('term', '')
    protagonists = Protagonist.objects.filter(
        Q(first_name__icontains=term) | Q(last_name__icontains=term)
    )[:10]  # Limit results
    results = [
        {
            'id': p.id,
            'text': p.get_full_name()
        }
        for p in protagonists
    ]
    return JsonResponse(results, safe=False)

def add_protagonist_view(request):
    if request.method == 'POST':
        form = ProtagonistForm(request.POST)
        if form.is_valid():
            protagonist = form.save()
            return JsonResponse({'success': True, 'id': protagonist.id, 'name': protagonist.get_full_name()})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request'})
