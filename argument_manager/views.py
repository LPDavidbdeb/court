from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy, reverse
from .models import TrameNarrative, PerjuryArgument
from .forms import TrameNarrativeForm, PerjuryArgumentForm
from document_manager.models import LibraryNode, Statement, Document 
from django.contrib.contenttypes.models import ContentType

import json
import time
from itertools import groupby
from collections import OrderedDict
from datetime import date
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render
from django.db.models import Q, Prefetch
from email_manager.models import Email, EmailThread, Quote as EmailQuote
from events.models import Event
from pdf_manager.models import PDFDocument, Quote as PDFQuote
from photos.models import PhotoDocument


class PerjuryBacklogView(ListView):
    model = Statement
    template_name = 'argument_manager/perjury_backlog.html'
    context_object_name = 'statements'

    def get_queryset(self):
        """
        This view lists all statements that are marked as false and falsifiable,
        which represents the "Backlog of Perjury" to be refuted.
        """
        return Statement.objects.filter(is_true=False, is_falsifiable=True).order_by('id')


class PerjuryArgumentCreateView(CreateView):
    model = PerjuryArgument
    form_class = PerjuryArgumentForm
    template_name = 'argument_manager/perjuryargument_form.html'

    def get_initial(self):
        initial = super().get_initial()
        statement_ids = self.request.GET.getlist('statement_ids')
        if statement_ids:
            initial['targeted_statements'] = statement_ids
        return initial

    def get_success_url(self):
        return reverse('argument_manager:detail', kwargs={'pk': self.object.trame_narrative.pk})


@require_POST
def ajax_remove_allegation(request, narrative_pk):
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        data = json.loads(request.body)
        allegation_id = data.get('allegation_id')
        if not allegation_id:
            return JsonResponse({'success': False, 'error': 'Allegation ID is required.'}, status=400)
        allegation = get_object_or_404(Statement, pk=allegation_id)
        narrative.targeted_statements.remove(allegation)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_POST
def ajax_remove_evidence(request, narrative_pk):
    EVIDENCE_MODELS = {
        'PDFQuote': (PDFQuote, 'citations_pdf'),
        'EmailQuote': (EmailQuote, 'citations_courriel'),
        'Event': (Event, 'evenements'),
        'PhotoDocument': (PhotoDocument, 'photo_documents'),
        'Statement': (Statement, 'source_statements'),
    }
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        data = json.loads(request.body)
        evidence_type = data.get('evidence_type')
        evidence_id = data.get('evidence_id')
        if not evidence_type or not evidence_id:
            return JsonResponse({'success': False, 'error': 'Evidence type and ID are required.'}, status=400)
        model_class, relationship_name = EVIDENCE_MODELS.get(evidence_type)
        if not model_class:
            return JsonResponse({'success': False, 'error': f'Invalid evidence type: {evidence_type}'}, status=400)
        evidence_to_remove = get_object_or_404(model_class, pk=evidence_id)
        relationship_manager = getattr(narrative, relationship_name)
        relationship_manager.remove(evidence_to_remove)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def pdf_quote_list_for_tinymce(request):
    quotes = PDFQuote.objects.select_related('pdf_document').order_by('pdf_document__title', 'page_number')
    formatted_quotes = []
    for quote in quotes:
        if quote.pdf_document:
            title = f"{quote.pdf_document.title} (p. {quote.page_number}) - {quote.quote_text[:50]}..."
            value = f'''<blockquote data-quote-id="{quote.id}" data-source="pdf"> <p>{quote.quote_text}</p> <cite>Source: {quote.pdf_document.title}, page {quote.page_number}</cite> </blockquote>'''
            formatted_quotes.append({'title': title, 'value': value})
    return JsonResponse(formatted_quotes, safe=False)


def ajax_search_emails(request):
    return JsonResponse({'emails': []})


class TrameNarrativeListView(ListView):
    model = TrameNarrative
    template_name = 'argument_manager/tiamenarrative_list.html'
    context_object_name = 'narratives'


class TrameNarrativeDetailView(DetailView):
    model = TrameNarrative
    context_object_name = 'narrative'

    def get_template_names(self):
        # This logic can be simplified if you decide on a single view,
        # but for now, it's kept as is.
        view_type = self.request.GET.get('view', 'columns') 
        if view_type == 'columns':
            return ['argument_manager/tiamenarrative_detail.html']
        # The accordion view is now the main view for displaying perjury arguments
        return ['argument_manager/tiamenarrative_detail_accordion.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        narrative = self.get_object()

        # The existing context data for other parts of the page
        narrative_data = {
            'events': [{'title': f'{e.date.strftime("%Y-%m-%d")}: {e.explanation[:50]}...', 'text': e.explanation, 'url': reverse('events:detail', args=[e.pk])} for e in narrative.evenements.all()],
            'emailQuotes': [{'title': f'{q.quote_text[:50]}...', 'text': q.quote_text, 'url': reverse('email_manager:thread_detail', args=[q.email.thread.pk])} for q in narrative.citations_courriel.select_related('email__thread').all()],
            'pdfQuotes': [{'title': f'{q.quote_text[:50]}...', 'text': q.quote_text, 'url': reverse('pdf_manager:pdf_detail', args=[q.pdf_document.pk])} for q in narrative.citations_pdf.select_related('pdf_document').all()]
        }
        context['narrative_data_json'] = json.dumps(narrative_data)
        
        # We no longer need to pass allegations separately, as they are part of the arguments
        # However, if you have other uses for this, you can keep it.
        allegations = narrative.targeted_statements.all()
        allegation_ids = [str(allegation.pk) for allegation in allegations]
        context['highlight_ids'] = ",".join(allegation_ids)
        
        # The main addition: prefetch the arguments and their related statements
        context['arguments'] = narrative.arguments.prefetch_related('targeted_statements')
        
        return context


class TrameNarrativeCreateView(CreateView):
    model = TrameNarrative
    form_class = TrameNarrativeForm
    template_name = 'argument_manager/tiamenarrative_form.html'
    success_url = reverse_lazy('argument_manager:list')
    def form_valid(self, form):
        response = super().form_valid(form)
        selected_events_str = self.request.POST.get('selected_events', '')
        if selected_events_str:
            self.object.evenements.set(selected_events_str.split(','))
        return response


class TrameNarrativeUpdateView(UpdateView):
    model = TrameNarrative
    form_class = TrameNarrativeForm
    template_name = 'argument_manager/tiamenarrative_form.html'
    def get_success_url(self):
        return reverse_lazy('argument_manager:detail', kwargs={'pk': self.object.pk})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        narrative = self.get_object()
        context['associated_events'] = narrative.evenements.all()
        context['associated_email_quotes'] = narrative.citations_courriel.select_related('email').all()
        context['associated_pdf_quotes'] = narrative.citations_pdf.select_related('pdf_document').all()
        context['associated_photo_documents'] = narrative.photo_documents.all()
        context['associated_statements'] = narrative.source_statements.all()
        return context
    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.evenements.set(self.request.POST.get('selected_events', '').split(',') if self.request.POST.get('selected_events') else [])
        self.object.citations_courriel.set(self.request.POST.get('selected_email_quotes', '').split(',') if self.request.POST.get('selected_email_quotes') else [])
        self.object.citations_pdf.set(self.request.POST.get('selected_pdf_quotes', '').split(',') if self.request.POST.get('selected_pdf_quotes') else [])
        self.object.photo_documents.set(self.request.POST.get('selected_photo_documents', '').split(',') if self.request.POST.get('selected_photo_documents') else [])
        self.object.source_statements.set(self.request.POST.get('selected_statements', '').split(',') if self.request.POST.get('selected_statements') else [])
        return response


class TrameNarrativeDeleteView(DeleteView):
    model = TrameNarrative
    template_name = 'argument_manager/tiamenarrative_confirm_delete.html'
    context_object_name = 'narrative'
    success_url = reverse_lazy('argument_manager:list')


@require_POST
def ajax_update_summary(request, narrative_pk):
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        data = json.loads(request.body)
        new_summary = data.get('resume')
        if new_summary is not None:
            narrative.resume = new_summary
            narrative.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'No summary provided.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def affidavit_generator_view(request, pk):
    narrative = get_object_or_404(TrameNarrative.objects.prefetch_related('arguments__targeted_statements'), pk=pk)
    context = {
        'narrative': narrative,
        'arguments': narrative.arguments.all(),
    }
    return render(request, 'argument_manager/affidavit_generator.html', context)


def ajax_get_statements_list(request):
    statement_content_type = ContentType.objects.get_for_model(Statement)
    nodes_linking_to_statements = LibraryNode.objects.filter(content_type=statement_content_type).select_related('document').prefetch_related('content_object')
    grouped_statements = {}
    for node in nodes_linking_to_statements:
        if node.content_object:
            doc = node.document
            if doc not in grouped_statements:
                grouped_statements[doc] = set()
            grouped_statements[doc].add(node.content_object)
    final_grouped_statements = {doc: list(stmts) for doc, stmts in grouped_statements.items()}
    return render(request, 'argument_manager/_statement_selection_list.html', {'grouped_statements': final_grouped_statements.items()})


@require_POST
def ajax_update_narrative_statements(request, narrative_pk):
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        data = json.loads(request.body)
        narrative.source_statements.set(data.get('statement_ids', []))
        updated_statements = narrative.source_statements.all()
        return JsonResponse({'success': True, 'statements': [{'pk': s.pk, 'text': s.text} for s in updated_statements]})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_POST
def ajax_add_email_quote(request, narrative_pk):
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        data = json.loads(request.body)
        email = get_object_or_404(Email, pk=data.get('email_id'))
        new_quote = EmailQuote.objects.create(email=email, quote_text=data.get('quote_text'))
        narrative.citations_courriel.add(new_quote)
        return JsonResponse({'success': True, 'quote': {'id': new_quote.id, 'text': new_quote.quote_text, 'full_sentence': new_quote.full_sentence}})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def ajax_get_email_threads(request):
    threads = EmailThread.objects.prefetch_related(Prefetch('emails', queryset=Email.objects.order_by('date_sent')))
    processed_threads = [{'pk': t.pk, 'subject': t.subject, 'first_email_date': t.emails.first().date_sent if t.emails.first() else None, 'participants': ", ".join(filter(None, {e.sender for e in t.emails.all()}))} for t in threads]
    return render(request, 'argument_manager/_thread_list.html', {'threads': sorted([t for t in processed_threads if t['first_email_date']], key=lambda t: t['first_email_date'], reverse=True)})


def ajax_get_thread_emails(request, thread_pk):
    thread = get_object_or_404(EmailThread, pk=thread_pk)
    return render(request, 'argument_manager/_email_accordion.html', {'emails': thread.emails.order_by('date_sent')})


def ajax_get_events_list(request):
    return render(request, 'argument_manager/_event_selection_list.html', {'events': Event.objects.prefetch_related('linked_photos').order_by('-date')})


@require_POST
def ajax_update_narrative_events(request, narrative_pk):
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        narrative.evenements.set(json.loads(request.body).get('event_ids', []))
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def ajax_get_email_quotes_list(request):
    quotes = EmailQuote.objects.select_related('email__thread').order_by('-email__date_sent')
    grouped_quotes = OrderedDict((thread, list(quotes_in_thread)) for thread, quotes_in_thread in groupby(quotes, key=lambda q: q.email.thread))
    return render(request, 'argument_manager/_email_quote_selection_list.html', {'grouped_quotes': grouped_quotes.items()})


@require_POST
def ajax_update_narrative_email_quotes(request, narrative_pk):
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        narrative.citations_courriel.set(json.loads(request.body).get('quote_ids', []))
        return JsonResponse({'success': True, 'quotes': [{'pk': q.pk, 'text': q.quote_text, 'parent_url': q.email.get_absolute_url()} for q in narrative.citations_courriel.select_related('email').all()]})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def ajax_get_pdf_quotes_list(request):
    quotes = PDFQuote.objects.select_related('pdf_document').order_by('-pdf_document__document_date', 'page_number')
    grouped_quotes = OrderedDict((doc, list(quotes_in_doc)) for doc, quotes_in_doc in groupby(quotes, key=lambda q: q.pdf_document) if doc)
    return render(request, 'argument_manager/_pdf_quote_selection_list.html', {'grouped_quotes': grouped_quotes.items()})


@require_POST
def ajax_update_narrative_pdf_quotes(request, narrative_pk):
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        narrative.citations_pdf.set(json.loads(request.body).get('quote_ids', []))
        return JsonResponse({'success': True, 'quotes': [{'pk': q.pk, 'text': q.quote_text, 'page': q.page_number, 'parent_url': q.pdf_document.get_absolute_url()} for q in narrative.citations_pdf.select_related('pdf_document').all()]})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def ajax_get_source_pdfs(request):
    documents = PDFDocument.objects.select_related('document_type').order_by('document_type__name', 'title')
    grouped_documents = [{'type_name': key.name if key else "Uncategorized", 'documents': list(group)} for key, group in groupby(documents, key=lambda doc: doc.document_type)]
    return render(request, 'argument_manager/_pdf_source_list.html', {'grouped_documents': grouped_documents})


@require_POST
def ajax_add_pdf_quote(request, narrative_pk):
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        data = json.loads(request.body)
        pdf_doc = get_object_or_404(PDFDocument, pk=data.get('doc_id'))
        new_quote = PDFQuote.objects.create(pdf_document=pdf_doc, quote_text=data.get('quote_text'), page_number=data.get('page_number'))
        narrative.citations_pdf.add(new_quote)
        return JsonResponse({'success': True, 'quote': {'pk': new_quote.pk, 'text': new_quote.quote_text, 'page': new_quote.page_number, 'parent_url': pdf_doc.get_absolute_url()}})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def ajax_get_pdf_viewer(request, doc_pk):
    document = get_object_or_404(PDFDocument, pk=doc_pk)
    return render(request, 'argument_manager/_pdf_viewer_partial.html', {'pdf_url_with_params': f"{document.file.url}?v={int(time.time())}#view=Fit&layout=SinglePage"})


def ajax_get_photo_documents(request, narrative_pk):
    narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
    all_docs = PhotoDocument.objects.all().order_by('-created_at')
    associated_doc_ids = set(narrative.photo_documents.values_list('id', flat=True))
    return JsonResponse([{'id': doc.id, 'title': doc.title, 'is_associated': doc.id in associated_doc_ids} for doc in all_docs], safe=False)


@require_POST
def ajax_associate_photo_documents(request, narrative_pk):
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        narrative.photo_documents.set([int(id) for id in json.loads(request.body).get('photo_document_ids', [])])
        return JsonResponse({'success': True, 'photo_documents': [{'id': doc.id, 'title': doc.title} for doc in narrative.photo_documents.all().order_by('-created_at')]})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
