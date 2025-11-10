from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.db.models import Prefetch
from datetime import datetime, date
from django.utils import timezone

from ..models import Document, LibraryNode, Statement
from argument_manager.models import TrameNarrative
from email_manager.models import Quote as EmailQuote, Email
from pdf_manager.models import Quote as PDFQuote, PDFDocument
from events.models import Event
from photos.models import PhotoDocument, Photo


# --- Helper function for formatting (adapted from old views) ---

def _format_nodes_for_new_display(nodes):
    """
    Helper function to add numbering and indentation to each node for the new models.
    """
    formatted_list = []
    # Counters for legal-style numbering: depth 2 -> section, depth 3 -> subsection, etc.
    counters = {2: 0, 3: 0, 4: 0}

    for node in nodes:
        depth = node.depth
        
        if depth == 2:
            counters[2] += 1
            counters[3] = 0
            counters[4] = 0
            node.numbering = f"{counters[2]}."
        elif depth == 3:
            counters[3] += 1
            counters[4] = 0
            node.numbering = f"{chr(96 + counters[3])}."
        elif depth == 4:
            counters[4] += 1
            roman_map = {1: 'i', 2: 'ii', 3: 'iii', 4: 'iv', 5: 'v'}
            node.numbering = f"{roman_map.get(counters[4], counters[4])}."
        else:
            node.numbering = ""
        
        # Adjust indentation based on depth (starting from depth 1 as root)
        node.indent_pixels = (depth - 1) * 40
            
        formatted_list.append(node)
        
    return formatted_list

# --- View Functions ---

def new_document_list_view(request):
    """
    A new list view that uses the refactored 'Document' model.
    """
    documents = Document.objects.all().order_by('-created_at')
    return render(request, 'document_manager/new_document_list.html', {'documents': documents})

def new_document_detail_view(request, pk):
    """
    A new standard detail view that uses the refactored models.
    """
    document = get_object_or_404(Document, pk=pk)
    nodes = document.nodes.all().order_by('path')
    
    for node in nodes:
        node.indent_pixels = (node.depth - 1) * 40
        
    context = {
        'document': document,
        'nodes': nodes,
    }
    return render(request, 'document_manager/new_document_detail.html', context)

def new_clean_detail_view(request, pk):
    """
    A new 'clean' formatted view that uses the refactored models.
    """
    document = get_object_or_404(Document, pk=pk)
    # Exclude the root node for display purposes, as numbering starts from its children.
    descendants = document.nodes.filter(depth__gt=1).order_by('path')
    
    formatted_nodes = _format_nodes_for_new_display(descendants)
    
    context = {
        'document': document,
        'formatted_nodes': formatted_nodes,
    }
    return render(request, 'document_manager/new_clean_detail.html', context)

def new_interactive_detail_view(request, pk):
    """
    A new 'interactive' view that uses the refactored models.
    """
    document = get_object_or_404(Document, pk=pk)
    descendants = document.nodes.filter(depth__gt=1).order_by('path')
    
    formatted_nodes = _format_nodes_for_new_display(descendants)
    
    context = {
        'document': document,
        'formatted_nodes': formatted_nodes,
    }
    return render(request, 'document_manager/new_interactive_detail.html', context)


# --- New Perjury Element List View ---

class NewPerjuryElementListView(ListView):
    model = Statement
    template_name = 'document_manager/new_perjury_element_list.html'
    context_object_name = 'data_by_document'

    def _get_paragraph_numbering_map(self, document):
        """
        Replicates the numbering logic for the new models.
        """
        nodes = document.nodes.all().order_by('path')
        numbering_map = {}
        counters = {2: 0, 3: 0, 4: 0}

        for node in nodes:
            depth = node.depth
            numbering = ""
            
            if depth == 2:
                counters[2] += 1
                counters[3] = 0
                counters[4] = 0
                numbering = f"{counters[2]}."
            elif depth == 3:
                counters[3] += 1
                counters[4] = 0
                numbering = f"{chr(96 + counters[3])}."
            elif depth == 4:
                counters[4] += 1
                roman_map = {1: 'i', 2: 'ii', 3: 'iii', 4: 'iv', 5: 'v'}
                numbering = f"{roman_map.get(counters[4], counters[4])}."
            
            if numbering:
                numbering_map[node.pk] = numbering.rstrip('.')

        return numbering_map

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 1. Get all perjury statements
        prefetch_narratives = Prefetch(
            'narratives',
            queryset=TrameNarrative.objects.prefetch_related(
                'evenements', 'citations_courriel__email', 'citations_pdf__pdf_document', 'photo_documents__photos'
            )
        )
        all_perjury_statements = Statement.objects.filter(
            is_true=False, is_falsifiable=True
        ).prefetch_related(prefetch_narratives).order_by('id')

        # 2. Collect unique items for global numbering
        source_doc_set, all_trames_set, used_items_set = set(), set(), set()
        for statement in all_perjury_statements:
            for trame in statement.narratives.all():
                all_trames_set.add(trame)
                for eq in trame.citations_courriel.all():
                    source_doc_set.add(eq.email)
                    used_items_set.add(eq)
                for pq in trame.citations_pdf.all():
                    source_doc_set.add(pq.pdf_document)
                    used_items_set.add(pq)
                for event in trame.evenements.all():
                    source_doc_set.add(event)
                for photo_doc in trame.photo_documents.all():
                    source_doc_set.add(photo_doc)
                    used_items_set.update(photo_doc.photos.all())

        # 3. Create global numbering maps (P-X, N-X, P-X.Y)
        def get_date(obj):
            dt = None
            if isinstance(obj, Email): dt = obj.date_sent
            elif isinstance(obj, PDFDocument): dt = obj.uploaded_at
            elif isinstance(obj, PhotoDocument): dt = obj.created_at
            elif isinstance(obj, Event): dt = obj.date
            if not dt: return None
            if isinstance(dt, date) and not isinstance(dt, datetime):
                dt = datetime.combine(dt, datetime.min.time())
            return timezone.make_aware(dt) if timezone.is_naive(dt) else dt

        sorted_source_docs = sorted([d for d in source_doc_set if get_date(d)], key=get_date)
        exhibit_map = {doc: f"P-{i+1}" for i, doc in enumerate(sorted_source_docs)}
        
        item_map = {}
        for doc, p_id in exhibit_map.items():
            items_in_doc = []
            if isinstance(doc, Email): items_in_doc = sorted(list(doc.quotes.all()), key=lambda x: x.pk)
            elif isinstance(doc, PDFDocument): items_in_doc = sorted(list(doc.quotes.all()), key=lambda x: x.pk)
            elif isinstance(doc, PhotoDocument): items_in_doc = sorted(list(doc.photos.all()), key=lambda x: x.pk)
            item_counter = 1
            for item in items_in_doc:
                if item in used_items_set:
                    item_map[item] = f"{p_id}.{item_counter}"
                    item_counter += 1

        sorted_trames = sorted(list(all_trames_set), key=lambda t: t.pk)
        trame_map = {trame: f"N-{i+1}" for i, trame in enumerate(sorted_trames)}

        # 4. Build the hierarchical structure, grouped by parent document
        data_by_document = []
        main_documents = Document.objects.all().order_by('id')
        doc_counter = 0

        for doc in main_documents:
            # Find all LibraryNodes in this document that link to a perjury statement
            nodes_in_doc = LibraryNode.objects.filter(
                document=doc,
                statement__in=all_perjury_statements
            ).select_related('statement').prefetch_related(
                Prefetch('statement__narratives', queryset=TrameNarrative.objects.prefetch_related(
                    'evenements', 'citations_courriel', 'citations_pdf', 'photo_documents'
                ))
            ).order_by('path')

            if not nodes_in_doc:
                continue

            doc_counter += 1
            doc_id = f"C-{doc_counter}"
            paragraph_number_map = self._get_paragraph_numbering_map(doc)

            doc_data = {'document': doc, 'doc_id': doc_id, 'claims': []}
            for claim_node in nodes_in_doc:
                para_num = paragraph_number_map.get(claim_node.pk)
                claim_id = f"{doc_id}-{para_num}" if para_num else doc_id

                node_data = self._get_structured_data_for_node(
                    claim_node, trame_map, exhibit_map, item_map, sorted_source_docs, sorted_trames
                )
                node_data['claim_id'] = claim_id
                doc_data['claims'].append(node_data)
            
            data_by_document.append(doc_data)

        # 5. Prepare lists for the 'exhibits' section of the template
        exhibits_list = []
        for doc in sorted_source_docs:
            p_id = exhibit_map.get(doc)
            if not p_id: continue
            type_fr, title = '', ''
            if isinstance(doc, Email): type_fr, title = 'Courriel', doc.subject
            elif isinstance(doc, PDFDocument): type_fr, title = 'Document PDF', doc.title
            elif isinstance(doc, PhotoDocument): type_fr, title = 'Document Photo', doc.title
            elif isinstance(doc, Event): type_fr, title = 'Événement', f"Événement du {get_date(doc).strftime('%Y-%m-%d')}"
            exhibits_list.append({'main_id': p_id, 'type_fr': type_fr, 'title': title, 'date': get_date(doc)})

        narratives_list = [{'main_id': trame_map.get(t), 'title': t.titre, 'content': t.resume} for t in sorted_trames if trame_map.get(t)]

        context['data_by_document'] = data_by_document
        context['exhibits'] = exhibits_list
        context['narratives'] = narratives_list
        context['item_map'] = item_map
        context['trame_map'] = trame_map
        return context

    def _get_structured_data_for_node(self, node, trame_map, exhibit_map, item_map, sorted_source_docs, sorted_trames):
        node_data = {'node': node, 'trames': []}
        # Use the prefetched narratives from the statement
        trames_for_node = sorted(node.statement.narratives.all(), key=lambda t: sorted_trames.index(t) if t in sorted_trames else -1)

        for trame in trames_for_node:
            evidence_for_trame = []
            evidence_for_trame.extend(trame.citations_courriel.all())
            evidence_for_trame.extend(trame.citations_pdf.all())
            evidence_for_trame.extend(trame.evenements.all())
            evidence_for_trame.extend(trame.photo_documents.all())

            trame_data = {
                'trame': trame,
                'id': trame_map.get(trame),
                'evidence': self.process_evidence_for_node(
                    evidence_for_trame, exhibit_map, item_map, sorted_source_docs
                )
            }
            node_data['trames'].append(trame_data)
        return node_data

    def process_evidence_for_node(self, raw_evidence, exhibit_map, item_map, sorted_source_docs):
        processed = []
        def get_source_doc(obj):
            if isinstance(obj, EmailQuote): return obj.email
            if isinstance(obj, PDFQuote): return obj.pdf_document
            if isinstance(obj, (Event, PhotoDocument)): return obj
            return None
        def get_sort_key(obj):
            source = get_source_doc(obj)
            return sorted_source_docs.index(source) if source in sorted_source_docs else -1
        
        for obj in sorted(raw_evidence, key=get_sort_key):
            data = {'obj': obj}
            source_doc = get_source_doc(obj)
            data['p_id'] = exhibit_map.get(source_doc, '')

            if isinstance(obj, EmailQuote):
                data.update({
                    'type': 'EmailQuote',
                    'short_type': 'Email',
                    'item_id': item_map.get(obj),
                    'content': obj.quote_text,
                    'source_title': source_doc.subject,
                    'date': source_doc.date_sent,
                    'detail_url': source_doc.get_absolute_url()
                })
            elif isinstance(obj, PDFQuote):
                data.update({
                    'type': 'PDFQuote',
                    'short_type': 'PDF',
                    'item_id': item_map.get(obj),
                    'content': obj.quote_text,
                    'source_title': source_doc.title,
                    'date': source_doc.uploaded_at,
                    'detail_url': source_doc.get_absolute_url()
                })
            elif isinstance(obj, Event):
                data.update({'type': 'Event', 'short_type': 'Événement', 'item_id': None, 'content': obj.explanation, 'source_title': f"Événement du {obj.date.strftime('%Y-%m-%d')}", 'date': obj.date})
            elif isinstance(obj, PhotoDocument):
                data.update({'type': 'PhotoDocument', 'short_type': 'Photo', 'item_id': None, 'content': obj.description, 'source_title': obj.title, 'date': obj.created_at})
                data['photos'] = [{'obj': p, 'item_id': item_map.get(p)} for p in sorted(list(obj.photos.all()), key=lambda p: p.pk) if p in item_map]
            
            processed.append(data)
        return processed

    def get_queryset(self):
        return Statement.objects.none()
