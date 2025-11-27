import PIL.Image
from datetime import date
from django.template.defaultfilters import date as date_filter
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from collections import defaultdict

class EvidenceFormatter:

    @staticmethod
    def get_label(obj, exhibit_map):
        """
        Helper to find the P-Number (e.g., 'P-12') for an object.
        """
        if not obj or not exhibit_map:
            return None
        ct = ContentType.objects.get_for_model(obj)
        key = (ct.id, obj.id)
        return exhibit_map.get(key)
    
    @staticmethod
    def get_date(obj):
        if hasattr(obj, 'document_original_date') and obj.document_original_date:
            return obj.document_original_date
        elif hasattr(obj, 'document_date') and obj.document_date:
            return obj.document_date
        elif hasattr(obj, 'date'): return obj.date
        elif hasattr(obj, 'date_sent'): return obj.date_sent.date() if obj.date_sent else date.min
        elif hasattr(obj, 'pdf_document'):
            if obj.pdf_document and hasattr(obj.pdf_document, 'document_original_date') and obj.pdf_document.document_original_date:
                return obj.pdf_document.document_original_date
            elif obj.pdf_document and hasattr(obj.pdf_document, 'document_date') and obj.pdf_document.document_date:
                return obj.pdf_document.document_date
            return date.min
        elif hasattr(obj, 'created_at'): return obj.created_at.date()
        return date.min

    @staticmethod
    def _get_protagonist_display(protagonist, fallback_name):
        if not protagonist:
            return fallback_name
        name = protagonist.get_full_name()
        if protagonist.role:
            return f"{name} [{protagonist.role}]"
        return name

    @classmethod
    def collect_global_evidence(cls, narratives):
        """
        Iterates over a list of narratives and pools all evidence into a single
        chronological structure, while also gathering unique summaries and documents.
        """
        global_data = {
            'summaries': [],
            'timeline': [],
            'unique_documents': set()
        }

        email_map = defaultdict(list)
        pdf_map = defaultdict(list)
        seen_event_ids = set()

        for narrative in narratives:
            if narrative.resume:
                global_data['summaries'].append(narrative.resume)

            for quote in narrative.citations_courriel.all().select_related('email', 'email__sender_protagonist').prefetch_related('email__recipient_protagonists'):
                email_map[quote.email].append(quote)

            for quote in narrative.citations_pdf.all().select_related('pdf_document', 'pdf_document__author'):
                pdf_map[quote.pdf_document].append(quote)

            for event in narrative.evenements.all():
                if event.id not in seen_event_ids:
                    seen_event_ids.add(event.id)
                    global_data['timeline'].append({
                        'date': cls.get_date(event),
                        'type': 'event_entry',
                        'obj': event
                    })

            for photo in narrative.photo_documents.all():
                global_data['unique_documents'].add(photo)
                global_data['timeline'].append({
                    'date': cls.get_date(photo),
                    'type': 'photo_entry',
                    'obj': photo
                })

        for email, quotes in email_map.items():
            global_data['unique_documents'].add(email)
            global_data['timeline'].append({
                'date': cls.get_date(email),
                'type': 'email_entry',
                'obj': email,
                'quotes': quotes
            })

        for pdf, quotes in pdf_map.items():
            global_data['unique_documents'].add(pdf)
            global_data['timeline'].append({
                'date': cls.get_date(pdf),
                'type': 'pdf_entry',
                'obj': pdf,
                'quotes': quotes
            })

        global_data['timeline'].sort(key=lambda x: x['date'])
        
        return global_data

    @classmethod
    def format_timeline_item(cls, item, exhibit_label=None):
        """
        Generates a concise timeline entry. 
        Focuses on the 'Action' or 'Quote', referencing the Exhibit ID.
        """
        obj = item['obj']
        item_date = cls.get_date(obj)
        
        if item_date.year < 1950:
            date_str = "DATE NON SPÉCIFIÉE"
        else:
            date_str = item_date.strftime("%d %B %Y")

        label_str = f" (Pièce {exhibit_label})" if exhibit_label else ""

        if item['type'] == 'email_entry':
            sender = cls._get_protagonist_display(obj.sender_protagonist, obj.sender)
            
            if obj.recipient_protagonists.exists():
                recipients = [cls._get_protagonist_display(p, "") for p in obj.recipient_protagonists.all()]
                recipient_display = ", ".join(recipients)
            else:
                recipient_display = obj.recipients_to or "Destinataire inconnu"

            text = f"[ {date_str} ] COURRIEL{label_str} : De {sender} à {recipient_display} — Sujet : « {obj.subject} »\n"
            if item.get('quotes'):
                for q in item['quotes']:
                    text += f"    -> CITATION CLÉ : « {q.quote_text} »\n"
            return text

        elif item['type'] == 'pdf_entry':
            text = f"[ {date_str} ] DOCUMENT{label_str} : « {obj.title} »\n"
            if item.get('quotes'):
                for q in item['quotes']:
                    text += f"    -> EXTRAIT (Page {q.page_number}) : « {q.quote_text} »\n"
            return text

        elif item['type'] == 'event_entry':
            return f"[ {date_str} ] ÉVÉNEMENT : {obj.explanation}\n"

        elif item['type'] == 'photo_entry':
            return f"[ {date_str} ] PHOTO{label_str} : « {obj.title} »\n"

        return ""

    @classmethod
    def format_document_reference(cls, obj, exhibit_label=None):
        """
        Generates the detailed context for the 'Reference' section.
        This contains the full body text, AI analysis, etc.
        """
        header = f"--- PIÈCE {exhibit_label if exhibit_label else 'Non classée'} ---"
        
        if hasattr(obj, 'subject') and hasattr(obj, 'body_plain_text'):
            return (
                f"{header}\n"
                f"TYPE : Courriel complet\n"
                f"DE : {obj.sender}\n"
                f"À : {obj.recipients_to}\n"
                f"DATE : {obj.date_sent}\n"
                f"CONTENU :\n{obj.body_plain_text}\n"
            )
        
        elif hasattr(obj, 'title'):
            doc_type = "Document PDF" if hasattr(obj, 'page_count') else "Photo"
            analysis = getattr(obj, 'ai_analysis', None) or getattr(obj, 'description', '')
            
            return (
                f"{header}\n"
                f"TYPE : {doc_type} (« {obj.title} »)\n"
                f"DESCRIPTION / ANALYSE IA :\n{analysis}\n"
            )
            
        return ""
