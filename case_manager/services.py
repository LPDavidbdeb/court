# case_manager/services.py

from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.db.models import Min
from django.utils import timezone
from collections import defaultdict
from datetime import datetime

from .models import LegalCase, ExhibitRegistry, ProducedExhibit
from document_manager.models import LibraryNode, Statement, Document
from email_manager.models import Email, Quote as EmailQuote
from events.models import Event
from photos.models import PhotoDocument
from pdf_manager.models import PDFDocument, Quote as PDFQuote

def refresh_case_exhibits(case_id):
    """
    Placeholder: Ensures the ExhibitRegistry is up-to-date for the given case.
    """
    print(f"INFO: Running placeholder for refresh_case_exhibits for case {case_id}")
    pass

def get_datetime_for_sorting(exhibit, exhibit_objects):
    """
    Helper to extract a comparable datetime from pre-fetched evidence objects.
    """
    obj = exhibit_objects.get((exhibit.content_type_id, exhibit.object_id))
    if not obj:
        return timezone.now()

    dt = None
    model_name = exhibit.content_type.model
    
    if model_name == 'email' and obj.date_sent:
        dt = obj.date_sent
    elif model_name == 'event' and obj.date:
        dt = datetime.combine(obj.date, datetime.min.time())
    elif model_name == 'librarynode' and hasattr(obj, 'document') and obj.document.document_original_date:
        dt = datetime.combine(obj.document.document_original_date, datetime.min.time())
    elif model_name == 'photodocument':
        dt = obj.created_at
    elif model_name == 'pdfdocument' and obj.document_date:
        dt = datetime.combine(obj.document_date, datetime.min.time())
    elif model_name == 'quote' and hasattr(obj, 'pdf_document') and obj.pdf_document and obj.pdf_document.document_date:
        dt = datetime.combine(obj.pdf_document.document_date, datetime.min.time())

    if not dt and hasattr(obj, 'created_at') and obj.created_at:
        dt = obj.created_at

    if dt and timezone.is_naive(dt):
        return timezone.make_aware(dt, timezone.get_current_timezone())
    
    return dt or timezone.now()

def rebuild_produced_exhibits(case_id):
    """
    Wipes and repopulates the ProducedExhibit table for a case atomically
    and with optimized database queries.
    """
    try:
        with transaction.atomic():
            case = LegalCase.objects.get(pk=case_id)
            ProducedExhibit.objects.filter(case=case).delete()
            
            # --- Pre-fetch all quotes for the case ---
            email_quotes_map = defaultdict(list)
            all_email_quotes = EmailQuote.objects.filter(
                trames_narratives__supported_contestations__case=case
            ).select_related('email', 'email__sender_protagonist').prefetch_related('email__recipient_protagonists').distinct()
            for quote in all_email_quotes:
                if quote.email_id:
                    email_quotes_map[quote.email_id].append(quote)

            pdf_quotes_map = defaultdict(list)
            all_pdf_quotes = PDFQuote.objects.filter(
                trames_narratives__supported_contestations__case=case
            ).select_related('pdf_document', 'pdf_document__author').distinct()
            for quote in all_pdf_quotes:
                if quote.pdf_document_id:
                    pdf_quotes_map[quote.pdf_document_id].append(quote)

            refresh_case_exhibits(case_id) 
            all_exhibits = list(case.exhibits.all().select_related('content_type'))
            
            exhibits_by_type = defaultdict(list)
            for ex in all_exhibits:
                exhibits_by_type[ex.content_type_id].append(ex.object_id)

            content_types = ContentType.objects.in_bulk(exhibits_by_type.keys())

            exhibit_objects = {}
            for ct_id, obj_ids in exhibits_by_type.items():
                ct = content_types.get(ct_id)
                if not ct: continue
                
                model_class = ct.model_class()
                queryset = model_class.objects.filter(pk__in=obj_ids)
                
                if model_class == LibraryNode:
                    queryset = queryset.select_related('document', 'document__author', 'content_type').prefetch_related('content_object')
                elif model_class == Email:
                    queryset = queryset.select_related('sender_protagonist').prefetch_related('recipient_protagonists')
                elif model_class == PhotoDocument:
                    queryset = queryset.select_related('author')
                elif model_class == PDFDocument:
                    queryset = queryset.select_related('author')
                elif model_class == PDFQuote:
                    queryset = queryset.select_related('pdf_document', 'pdf_document__author')

                for obj in queryset:
                    exhibit_objects[(ct_id, obj.id)] = obj
            
            exhibits_with_sort_date = []
            for ex in all_exhibits:
                sort_date = get_datetime_for_sorting(ex, exhibit_objects)
                exhibits_with_sort_date.append({'exhibit': ex, 'sort_date': sort_date})
            exhibits_with_sort_date.sort(key=lambda x: x['sort_date'])

            new_rows = []
            global_counter = 1
            
            # NEW: Set to track LibraryNode exhibits that have been grouped and processed
            processed_library_node_exhibits = set()

            for item in exhibits_with_sort_date:
                exhibit = item['exhibit']
                
                # NEW: Skip if this LibraryNode was already handled in a group
                if exhibit.id in processed_library_node_exhibits:
                    continue

                sort_date = item['sort_date']
                obj = exhibit_objects.get((exhibit.content_type_id, exhibit.object_id))
                if not obj: continue

                model_name = exhibit.content_type.model
                main_label = f"P-{global_counter}"
                
                exhibit_type_str, date_text, desc_text, parties_str = "", "", "", ""
                
                # --- Main Exhibit Processing ---
                if model_name == 'librarynode':
                    # This is the first time we see a statement from this document.
                    # Create a master entry for the parent Document.
                    parent_doc = obj.document
                    exhibit_type_str = "Document (Général)"
                    date_text = parent_doc.document_original_date.strftime('%Y-%m-%d') if parent_doc.document_original_date else "Date Inconnue"
                    desc_text = parent_doc.title
                    if parent_doc.author:
                        parties_str = f"Auteur: {parent_doc.author.get_full_name_with_role()}"
                    
                    # Add the main row for the parent document
                    new_rows.append(ProducedExhibit(
                        case=case, sort_order=len(new_rows) + 1, label=main_label,
                        exhibit_type=exhibit_type_str, date_display=date_text, 
                        description=desc_text, parties=parties_str, content_object=parent_doc
                    ))

                    # --- Find all other statements from this same document ---
                    statement_nodes_for_this_doc = []
                    for other_exhibit_item in exhibits_with_sort_date:
                        other_exhibit = other_exhibit_item['exhibit']
                        if other_exhibit.content_type.model == 'librarynode':
                            other_node = exhibit_objects.get((other_exhibit.content_type_id, other_exhibit.object_id))
                            if other_node and other_node.document_id == parent_doc.id:
                                statement_nodes_for_this_doc.append(other_node)
                                processed_library_node_exhibits.add(other_exhibit.id)
                    
                    # --- Create sub-exhibits for each statement ---
                    for idx, node_obj in enumerate(statement_nodes_for_this_doc, 1):
                        if node_obj.content_object and isinstance(node_obj.content_object, Statement):
                            statement_text = node_obj.content_object.text
                            new_rows.append(ProducedExhibit(
                                case=case, sort_order=len(new_rows) + 1, label=f"{main_label}-{idx}",
                                exhibit_type="Déclaration", date_display="",
                                description=statement_text, parties="", content_object=node_obj.content_object
                            ))

                elif model_name == 'email':
                    exhibit_type_str = "Courriel"
                    date_text = obj.date_sent.strftime('%Y-%m-%d %H:%M') if obj.date_sent else "Date Inconnue"
                    desc_text = obj.subject or '[Sans sujet]'
                    sender = obj.sender_protagonist.get_full_name_with_role() if obj.sender_protagonist else obj.sender
                    recipients = ", ".join([p.get_full_name_with_role() for p in obj.recipient_protagonists.all()])
                    parties_str = f"De: {sender}\nÀ: {recipients}"
                    new_rows.append(ProducedExhibit(case=case, sort_order=len(new_rows) + 1, label=main_label, exhibit_type=exhibit_type_str, date_display=date_text, description=desc_text, parties=parties_str, content_object=obj))

                elif model_name == 'pdfdocument':
                    exhibit_type_str = "Document PDF"
                    date_text = obj.document_date.strftime('%Y-%m-%d') if obj.document_date else "Date Inconnue"
                    desc_text = obj.title
                    if obj.author:
                        parties_str = f"Auteur: {obj.author.get_full_name_with_role()}"
                    new_rows.append(ProducedExhibit(case=case, sort_order=len(new_rows) + 1, label=main_label, exhibit_type=exhibit_type_str, date_display=date_text, description=desc_text, parties=parties_str, content_object=obj))

                else: # Fallback for other types like Event, PhotoDocument, etc.
                    if model_name == 'event':
                        exhibit_type_str = "Événement"
                        if ':' in (obj.explanation or ""):
                            parts = obj.explanation.rsplit(':', 1)
                            date_text, desc_text = parts[0].strip(), parts[1].strip()
                        else:
                            date_text = obj.date.strftime('%Y-%m-%d') if obj.date else "Date Inconnue"
                            desc_text = obj.explanation or ""
                    elif model_name == 'photodocument':
                        exhibit_type_str = "Document Photo"
                        date_text = sort_date.strftime('%Y-%m-%d %H:%M') if sort_date else "Date Inconnue"
                        desc_text = obj.title
                        if obj.description: desc_text += f"\n{obj.description}"
                        if obj.author: parties_str = f"Auteur: {obj.author.get_full_name_with_role()}"
                    else:
                        exhibit_type_str = "Autre"
                        date_text = sort_date.strftime('%Y-%m-%d')
                        desc_text = str(obj)
                    new_rows.append(ProducedExhibit(case=case, sort_order=len(new_rows) + 1, label=main_label, exhibit_type=exhibit_type_str, date_display=date_text, description=desc_text, parties=parties_str, content_object=obj))

                # --- SUB-EXHIBIT LOOPS for quotes ---
                if model_name == 'email':
                    quotes = sorted(email_quotes_map.get(obj.id, []), key=lambda q: q.created_at)
                    for idx, quote_obj in enumerate(quotes, 1):
                        quote_email = quote_obj.email
                        quote_date_text = quote_email.date_sent.strftime('%Y-%m-%d %H:%M') if quote_email.date_sent else ""
                        sender = quote_email.sender_protagonist.get_full_name_with_role() if quote_email.sender_protagonist else quote_email.sender
                        recipients = ", ".join([p.get_full_name_with_role() for p in quote_email.recipient_protagonists.all()])
                        quote_parties_str = f"De: {sender}\nÀ: {recipients}"
                        short_q = (quote_obj.quote_text[:200] + '..') if len(quote_obj.quote_text) > 200 else quote_obj.quote_text
                        new_rows.append(ProducedExhibit(case=case, sort_order=len(new_rows) + 1, label=f"{main_label}-{idx}", exhibit_type="Citation Courriel", date_display=quote_date_text, description=f"« {short_q} »", parties=quote_parties_str, content_object=quote_obj))
                
                if model_name == 'pdfdocument':
                    quotes = sorted(pdf_quotes_map.get(obj.id, []), key=lambda q: q.created_at)
                    for idx, quote_obj in enumerate(quotes, 1):
                        quote_doc = quote_obj.pdf_document
                        quote_date_text = quote_doc.document_date.strftime('%Y-%m-%d') if quote_doc.document_date else ""
                        quote_parties_str = f"Auteur: {quote_doc.author.get_full_name_with_role()}" if quote_doc.author else ""
                        desc = f"« {quote_obj.quote_text} » (p. {quote_obj.page_number})"
                        new_rows.append(ProducedExhibit(case=case, sort_order=len(new_rows) + 1, label=f"{main_label}-{idx}", exhibit_type="Citation PDF", date_display=quote_date_text, description=desc, parties=quote_parties_str, content_object=quote_obj))

                global_counter += 1

            ProducedExhibit.objects.bulk_create(new_rows)
            return len(new_rows)

    except Exception as e:
        raise e
