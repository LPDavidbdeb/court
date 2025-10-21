from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy, reverse
from .models import TrameNarrative
from .forms import TrameNarrativeForm
from document_manager.models import DocumentNode

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


@require_POST
def ajax_remove_allegation(request, narrative_pk):
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        data = json.loads(request.body)
        allegation_id = data.get('allegation_id')

        if not allegation_id:
            return JsonResponse({'success': False, 'error': 'Allegation ID is required.'}, status=400)

        allegation = get_object_or_404(DocumentNode, pk=allegation_id)
        narrative.allegations_ciblees.remove(allegation)

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_POST
def ajax_remove_evidence_association(request, narrative_pk):
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        data = json.loads(request.body)
        evidence_type = data.get('evidence_type')
        evidence_id = data.get('evidence_id')

        if not evidence_type or not evidence_id:
            return JsonResponse({'success': False, 'error': 'Evidence type and ID are required.'}, status=400)

        if evidence_type == 'Event':
            event_to_remove = get_object_or_404(Event, pk=evidence_id)
            narrative.evenements.remove(event_to_remove)
        elif evidence_type == 'PhotoDocument':
            photo_doc_to_remove = get_object_or_404(PhotoDocument, pk=evidence_id)
            narrative.photo_documents.remove(photo_doc_to_remove)
        elif evidence_type == 'PDFQuote':
            quote_to_remove = get_object_or_404(PDFQuote, pk=evidence_id)
            narrative.citations_pdf.remove(quote_to_remove)
        elif evidence_type == 'EmailQuote':
            quote_to_remove = get_object_or_404(EmailQuote, pk=evidence_id)
            narrative.citations_courriel.remove(quote_to_remove)
        else:
            return JsonResponse({'success': False, 'error': f'Invalid evidence type received: {evidence_type}'}, status=400)

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_POST
def ajax_remove_quote(request, narrative_pk):
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        data = json.loads(request.body)
        quote_id = data.get('quote_id')
        quote_type = data.get('quote_type')

        if not quote_id or not quote_type:
            return JsonResponse({'success': False, 'error': 'Quote ID and type are required.'}, status=400)

        if quote_type == 'PDFQuote':
            quote_to_remove = get_object_or_404(PDFQuote, pk=quote_id)
            narrative.citations_pdf.remove(quote_to_remove)
        elif quote_type == 'EmailQuote':
            quote_to_remove = get_object_or_404(EmailQuote, pk=quote_id)
            narrative.citations_courriel.remove(quote_to_remove)
        else:
            return JsonResponse({'success': False, 'error': f'Invalid quote type received: {quote_type}'}, status=400)

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def pdf_quote_list_for_tinymce(request):
    """
    Returns a list of PDF quotes in a format suitable for TinyMCE's link plugin.
    """
    quotes = PDFQuote.objects.select_related('pdf_document').order_by('pdf_document__title', 'page_number')
    
    # Format the quotes for TinyMCE
    formatted_quotes = []
    for quote in quotes:
        if quote.pdf_document:
            # Construct a descriptive title for the dropdown
            title = f"{quote.pdf_document.title} (p. {quote.page_number}) - {quote.quote_text[:50]}..."
            # The value to be inserted into the editor
            value = f'''<blockquote data-quote-id="{quote.id}" data-source="pdf"> <p>{quote.quote_text}</p> <cite>Source: {quote.pdf_document.title}, page {quote.page_number}</cite> </blockquote>'''
            formatted_quotes.append({'title': title, 'value': value})
            
    return JsonResponse(formatted_quotes, safe=False)

# THIS IS THE DIAGNOSTIC FIX: Add a dummy function to prevent server startup errors.
def ajax_search_emails(request):
    """
    A dummy view to prevent server startup errors. This is not used.
    This function is a placeholder and does not perform any actual email search.
    It always returns an empty list of emails.
    """
    return JsonResponse({'emails': []})

class TrameNarrativeListView(ListView):
    model = TrameNarrative
    template_name = 'argument_manager/tiamenarrative_list.html'
    context_object_name = 'narratives'

class TrameNarrativeDetailView(DetailView):
    model = TrameNarrative
    context_object_name = 'narrative'

    def get_template_names(self):
        """
        Returns the appropriate template based on the 'view' query parameter.
        """
        view_type = self.request.GET.get('view', 'columns')
        if view_type == 'accordion':
            return ['argument_manager/tiamenarrative_detail_accordion.html']
        return ['argument_manager/tiamenarrative_detail.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        narrative = self.get_object()
        allegations = narrative.allegations_ciblees.all()
        allegation_ids = [str(allegation.pk) for allegation in allegations]
        context['highlight_ids'] = ",".join(allegation_ids)
        allegations_with_docs = []
        for allegation in allegations:
            ancestors = allegation.get_ancestors()
            correct_document = next((ancestor for ancestor in ancestors if ancestor.depth == 2), None)
            if correct_document:
                allegations_with_docs.append((allegation, correct_document.pk))
            else:
                allegations_with_docs.append((allegation, None))
        context['allegations_with_docs'] = allegations_with_docs
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
            event_ids = selected_events_str.split(',')
            self.object.evenements.set(event_ids)
        return response

class TrameNarrativeUpdateView(UpdateView):
    model = TrameNarrative
    form_class = TrameNarrativeForm
    template_name = 'argument_manager/tiamenarrative_form.html'

    def get_success_url(self):
        return reverse_lazy('argument_manager:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        narrative = self.object

        # Pass associated querysets directly
        context['associated_events'] = narrative.evenements.all()
        context['associated_email_quotes'] = narrative.citations_courriel.select_related('email').all()
        context['associated_pdf_quotes'] = narrative.citations_pdf.select_related('pdf_document').all()
        context['associated_photo_documents'] = narrative.photo_documents.all()

        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Handle Events
        selected_events_str = self.request.POST.get('selected_events', '')
        event_ids = selected_events_str.split(',') if selected_events_str else []
        self.object.evenements.set(event_ids)

        # Handle Email Quotes
        selected_email_quotes_str = self.request.POST.get('selected_email_quotes', '')
        email_quote_ids = selected_email_quotes_str.split(',') if selected_email_quotes_str else []
        self.object.citations_courriel.set(email_quote_ids)

        # Handle PDF Quotes
        selected_pdf_quotes_str = self.request.POST.get('selected_pdf_quotes', '')
        pdf_quote_ids = selected_pdf_quotes_str.split(',') if selected_pdf_quotes_str else []
        self.object.citations_pdf.set(pdf_quote_ids)

        # Handle Photo Documents
        selected_photo_docs_str = self.request.POST.get('selected_photo_documents', '')
        photo_doc_ids = selected_photo_docs_str.split(',') if selected_photo_docs_str else []
        self.object.photo_documents.set(photo_doc_ids)
            
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

@require_POST
def ajax_add_email_quote(request, narrative_pk):
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        data = json.loads(request.body)
        email_id = data.get('email_id')
        quote_text = data.get('quote_text')
        if not email_id or not quote_text:
            return JsonResponse({'success': False, 'error': 'Email ID and quote text are required.'}, status=400)
        email_obj = get_object_or_404(Email, pk=email_id)
        new_quote = EmailQuote.objects.create(
            email=email_obj,
            quote_text=quote_text
        )
        narrative.citations_courriel.add(new_quote)
        return JsonResponse({
            'success': True,
            'quote': {
                'id': new_quote.id,
                'text': new_quote.quote_text,
                'full_sentence': new_quote.full_sentence
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def ajax_get_events_list(request):
    events = Event.objects.prefetch_related('linked_photos').order_by('-date')
    return render(request, 'argument_manager/_event_selection_list.html', {'events': events})

@require_POST
def ajax_update_narrative_events(request, narrative_pk):
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        data = json.loads(request.body)
        event_ids = data.get('event_ids', [])
        narrative.evenements.set(event_ids)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def ajax_get_email_quotes_list(request):
    quotes = EmailQuote.objects.select_related('email__thread').order_by('-email__date_sent')
    
    grouped_quotes = OrderedDict()
    for quote in quotes:
        thread = quote.email.thread
        if thread not in grouped_quotes:
            grouped_quotes[thread] = []
        grouped_quotes[thread].append(quote)

    return render(request, 'argument_manager/_email_quote_selection_list.html', {'grouped_quotes': grouped_quotes.items()})

@require_POST
def ajax_update_narrative_email_quotes(request, narrative_pk):
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        data = json.loads(request.body)
        quote_ids = data.get('quote_ids', [])
        narrative.citations_courriel.set(quote_ids)
        
        updated_quotes = narrative.citations_courriel.select_related('email').all()
        quotes_data = [
            {
                'pk': q.pk, 
                'text': q.quote_text, 
                'parent_url': q.email.get_absolute_url()
            } 
            for q in updated_quotes
        ]
        
        return JsonResponse({'success': True, 'quotes': quotes_data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def ajax_get_email_threads(request):
    threads = EmailThread.objects.prefetch_related(
        Prefetch('emails', queryset=Email.objects.order_by('date_sent'))
    )
    processed_threads = []
    for thread in threads:
        first_email = thread.emails.first()
        if not first_email:
            continue
        participants = set()
        for email in thread.emails.all():
            participants.add(email.sender)
        processed_threads.append({
            'pk': thread.pk,
            'subject': thread.subject,
            'first_email_date': first_email.date_sent,
            'participants': ", ".join(filter(None, participants)),
        })
    sorted_threads = sorted(processed_threads, key=lambda t: t['first_email_date'], reverse=True)
    return render(request, 'argument_manager/_thread_list.html', {'threads': sorted_threads})

def ajax_get_thread_emails(request, thread_pk):
    thread = get_object_or_404(EmailThread, pk=thread_pk)
    emails = thread.emails.order_by('date_sent')
    return render(request, 'argument_manager/_email_accordion.html', {'emails': emails})

def ajax_get_pdf_quotes_list(request):
    quotes = PDFQuote.objects.select_related('pdf_document').order_by('-pdf_document__document_date', 'page_number')
    
    grouped_quotes = OrderedDict()
    for quote in quotes:
        if quote.pdf_document:
            if quote.pdf_document not in grouped_quotes:
                grouped_quotes[quote.pdf_document] = []
            grouped_quotes[quote.pdf_document].append(quote)
            
    return render(request, 'argument_manager/_pdf_quote_selection_list.html', {'grouped_quotes': grouped_quotes.items()})

@require_POST
def ajax_update_narrative_pdf_quotes(request, narrative_pk):
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        data = json.loads(request.body)
        quote_ids = data.get('quote_ids', [])
        narrative.citations_pdf.set(quote_ids)
        
        updated_quotes = narrative.citations_pdf.select_related('pdf_document').all()
        quotes_data = [
            {
                'pk': q.pk, 
                'text': q.quote_text, 
                'page': q.page_number, 
                'parent_url': q.pdf_document.get_absolute_url()
            } 
            for q in updated_quotes
        ]
        
        return JsonResponse({'success': True, 'quotes': quotes_data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def ajax_get_source_pdfs(request):
    # Use select_related to efficiently fetch the document_type and order by its name
    documents = PDFDocument.objects.select_related('document_type').order_by('document_type__name', 'title')
    
    # Group documents by document_type using itertools.groupby
    grouped_documents = []
    for key, group in groupby(documents, key=lambda doc: doc.document_type):
        # The key will be the PDFDocumentType object or None for uncategorized documents
        group_name = key.name if key else "Uncategorized"
        grouped_documents.append({'type_name': group_name, 'documents': list(group)})
        
    context = {'grouped_documents': grouped_documents}
    
    return render(request, 'argument_manager/_pdf_source_list.html', context)

@require_POST
def ajax_add_pdf_quote(request, narrative_pk):
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        data = json.loads(request.body)
        doc_id = data.get('doc_id')
        quote_text = data.get('quote_text')
        page_number = data.get('page_number')

        if not all([doc_id, quote_text, page_number]):
            return JsonResponse({'success': False, 'error': 'Document, quote text, and page number are required.'}, status=400)

        pdf_doc = get_object_or_404(PDFDocument, pk=doc_id)
        
        new_quote = PDFQuote.objects.create(
            pdf_document=pdf_doc,
            quote_text=quote_text,
            page_number=page_number
        )
        
        narrative.citations_pdf.add(new_quote)
        
        return JsonResponse({
            'success': True,
            'quote': {
                'pk': new_quote.pk,
                'text': new_quote.quote_text,
                'page': new_quote.page_number,
                'parent_url': pdf_doc.get_absolute_url()
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def ajax_get_pdf_viewer(request, doc_pk):
    document = get_object_or_404(PDFDocument, pk=doc_pk)
    # Add a timestamp for cache-busting. The parameter must come BEFORE the hash.
    timestamp = int(time.time())
    pdf_url_with_params = f"{document.file.url}?v={timestamp}#view=Fit&layout=SinglePage"
    context = {
        'pdf_url_with_params': pdf_url_with_params
    }
    return render(request, 'argument_manager/_pdf_viewer_partial.html', context)

def ajax_get_photo_documents_list(request):
    photo_documents = PhotoDocument.objects.all().order_by('-created_at')
    return render(request, 'argument_manager/_photo_document_selection_list.html', {'photo_documents': photo_documents})

def affidavit_generator_view(request, pk):
    """
    Generates the context for a detailed, evidence-backed affidavit based on a TrameNarrative.
    """
    narrative = get_object_or_404(
        TrameNarrative.objects.prefetch_related(
            'allegations_ciblees',
            'evenements__linked_photos',
            'photo_documents__photos',
            'citations_courriel__email',
            'citations_pdf__pdf_document'
        ),
        pk=pk
    )

    # 1. Structure the claims being contradicted
    claims = [
        {
            'id': f'C-{allegation.pk}',
            'text': allegation.text,
            'obj': allegation
        }
        for allegation in narrative.allegations_ciblees.all()
    ]

    # 2. Gather and group all evidence sources
    all_evidence_source = []
    
    for item in narrative.evenements.all():
        all_evidence_source.append({'type': 'Event', 'date': item.date, 'obj': item})
    for item in narrative.photo_documents.all():
        all_evidence_source.append({'type': 'PhotoDocument', 'date': item.created_at.date(), 'obj': item})

    # Group PDF quotes by their parent document
    pdf_quotes = narrative.citations_pdf.select_related('pdf_document').order_by('pdf_document_id', 'page_number')
    for pdf_document, quotes in groupby(pdf_quotes, key=lambda q: q.pdf_document):
        if not pdf_document:
            continue
        quotes_list = list(quotes)
        if not quotes_list:
            continue
        pdf_date = getattr(pdf_document, 'document_date', None) or pdf_document.uploaded_at.date()
        all_evidence_source.append({
            'type': 'PDFDocument', 
            'date': pdf_date, 
            'obj': pdf_document,
            'quotes': quotes_list
        })

    # Group Email quotes by their parent email
    email_quotes = narrative.citations_courriel.select_related('email').order_by('email_id', 'id')
    for email, quotes in groupby(email_quotes, key=lambda q: q.email):
        if not email:
            continue
        quotes_list = list(quotes)
        if not quotes_list:
            continue
        all_evidence_source.append({
            'type': 'Email',
            'date': email.date_sent.date(),
            'obj': email,
            'quotes': quotes_list
        })

    # Sort all evidence chronologically
    all_evidence_source.sort(key=lambda x: x['date'] if x['date'] is not None else date.max)

    # 3. Process the sorted evidence to create final exhibits with hierarchical numbering
    exhibits = []
    exhibit_counter = 1
    for evidence in all_evidence_source:
        item_type = evidence['type']
        obj = evidence['obj']
        exhibit_id_base = f'P-{exhibit_counter}'
        exhibit_data = {}

        if item_type == 'Event':
            photos = obj.linked_photos.all()
            exhibit_data = {
                'type': 'Event',
                'type_fr': 'Événement',
                'title': obj.explanation,
                'date': obj.date,
                'main_id': exhibit_id_base,
                'evidence_obj': obj,
                'items': []
            }
            if photos:
                for i, photo in enumerate(photos):
                    exhibit_data['items'].append({
                        'id': f"{exhibit_id_base}-{i+1}",
                        'obj': photo,
                        'description': f"Photo {i+1} of event on {obj.date.strftime('%Y-%m-%d')}"
                    })

        elif item_type == 'PhotoDocument':
            photos = obj.photos.all()
            exhibit_data = {
                'type': 'PhotoDocument',
                'type_fr': 'Document photographique',
                'title': obj.title,
                'description': obj.description,
                'date': obj.created_at,
                'main_id': exhibit_id_base,
                'evidence_obj': obj,
                'items': []
            }
            if photos:
                for i, photo in enumerate(photos):
                    exhibit_data['items'].append({
                        'id': f"{exhibit_id_base}-{i+1}",
                        'obj': photo,
                        'description': f"Page {i+1} of document '{obj.title}'"
                    })

        elif item_type == 'PDFDocument':
            quotes = evidence['quotes']
            exhibit_data = {
                'type': 'PDFDocument',
                'type_fr': 'Document PDF',
                'title': obj.title,
                'date': evidence['date'],
                'main_id': exhibit_id_base,
                'evidence_obj': obj,
                'items': []
            }
            if quotes:
                for i, quote in enumerate(quotes):
                    exhibit_data['items'].append({
                        'id': f"{exhibit_id_base}-{i+1}",
                        'obj': quote,
                        'description': quote.quote_text
                    })

        elif item_type == 'Email':
            quotes = evidence['quotes']
            exhibit_data = {
                'type': 'Email',
                'type_fr': 'Courriel',
                'title': f"Courriel du {obj.date_sent.strftime('%Y-%m-%d')} - {obj.subject}",
                'date': evidence['date'],
                'main_id': exhibit_id_base,
                'evidence_obj': obj,
                'items': []
            }
            if quotes:
                for i, quote in enumerate(quotes):
                    exhibit_data['items'].append({
                        'id': f"{exhibit_id_base}-{i+1}",
                        'obj': quote,
                        'description': quote.quote_text
                    })
        
        if exhibit_data:
            exhibits.append(exhibit_data)
            exhibit_counter += 1

    # 4. Create the summary string for the affidavit text
    summary_parts = []
    for exhibit in exhibits:
        if len(exhibit['items']) > 1:
            id_range = f"{exhibit['items'][0]['id']} à {exhibit['items'][-1]['id']}"
            summary_parts.append(f"pièces {id_range}")
        elif exhibit['items']:
            summary_parts.append(f"pièce {exhibit['items'][0]['id']}")
        else: # For exhibits with no items, like an event with no photos
            summary_parts.append(f"pièce {exhibit['main_id']}")

    
    summary_str = f"Voir {', '.join(summary_parts)}."

    context = {
        'narrative': narrative,
        'claims': claims,
        'exhibits': exhibits,
        'summary_str': summary_str
    }

    return render(request, 'argument_manager/affidavit_generator.html', context)


@require_POST
def ajax_associate_photo_documents(request, narrative_pk):
    """
    Associates a list of PhotoDocuments with a TrameNarrative based on
    the provided IDs.
    """
    try:
        narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
        data = json.loads(request.body)
        doc_ids = data.get('photo_document_ids', [])
        
        # The IDs from JS will be strings, so convert them to int
        doc_ids = [int(id) for id in doc_ids]

        narrative.photo_documents.set(doc_ids)
        
        # Return the updated list of documents for display
        updated_docs = narrative.photo_documents.all().order_by('-created_at')
        docs_data = [
            {'id': doc.id, 'title': doc.title}
            for doc in updated_docs
        ]
        
        return JsonResponse({'success': True, 'photo_documents': docs_data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def ajax_get_photo_documents(request, narrative_pk):
    """
    Returns a JSON list of all PhotoDocuments, indicating which are
    associated with the current narrative.
    """
    narrative = get_object_or_404(TrameNarrative, pk=narrative_pk)
    all_docs = PhotoDocument.objects.all().order_by('-created_at')
    associated_doc_ids = set(narrative.photo_documents.values_list('id', flat=True))

    data = []
    for doc in all_docs:
        data.append({
            'id': doc.id,
            'title': doc.title,
            'is_associated': doc.id in associated_doc_ids
        })
    
    return JsonResponse(data, safe=False)
