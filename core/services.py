# core/services.py
from datetime import datetime
from django.utils import timezone
from django.db.models import Q
import html

# Import all evidence models
from email_manager.models import Email, Quote as EmailQuote
from pdf_manager.models import PDFDocument, Quote as PDFQuote
from photos.models import PhotoDocument
from events.models import Event
from document_manager.models import Statement, Document
from googlechat_manager.models import ChatSequence

def get_global_evidence_timeline():
    """
    Fetches ALL evidence from the system, normalizes it to match the 
    'ProducedExhibit' specification, and sorts it by date.
    """
    timeline_items = []
    
    # Helper to safe format dates
    def fmt_date(dt):
        if not dt: return "Date Inconnue"
        return dt.strftime('%Y-%m-%d %H:%M')

    def fmt_date_short(dt):
        if not dt: return "Date Inconnue"
        return dt.strftime('%Y-%m-%d')

    # --- 1. EMAILS ---
    emails = Email.objects.select_related('sender_protagonist').prefetch_related('recipient_protagonists').all()
    for obj in emails:
        sender = obj.sender_protagonist.get_full_name_with_role() if obj.sender_protagonist else obj.sender
        recipients = ", ".join([p.get_full_name_with_role() for p in obj.recipient_protagonists.all()])
        parties_str = f"De: {sender}\nÀ: {recipients}"
        
        timeline_items.append({
            'sort_date': obj.date_sent or timezone.now(),
            'date_display': fmt_date(obj.date_sent),
            'exhibit_type': "Courriel",
            'description': obj.subject or '[Sans sujet]',
            'parties': parties_str,
            'url': obj.get_absolute_url() if hasattr(obj, 'get_absolute_url') else None,
            'obj': obj
        })

    # --- 2. EMAIL QUOTES ---
    email_quotes = EmailQuote.objects.select_related('email', 'email__sender_protagonist').prefetch_related('email__recipient_protagonists').all()
    for obj in email_quotes:
        quote_email = obj.email
        sender = quote_email.sender_protagonist.get_full_name_with_role() if quote_email.sender_protagonist else quote_email.sender
        recipients = ", ".join([p.get_full_name_with_role() for p in quote_email.recipient_protagonists.all()])
        parties_str = f"De: {sender}\nÀ: {recipients}"
        
        # Truncate logic from services.py
        short_q = (obj.quote_text[:200] + '..') if len(obj.quote_text) > 200 else obj.quote_text
        
        timeline_items.append({
            'sort_date': quote_email.date_sent or obj.created_at,
            'date_display': fmt_date(quote_email.date_sent),
            'exhibit_type': "Citation Courriel",
            'description': f"« {short_q} »",
            'parties': parties_str,
            'url': obj.get_absolute_url() if hasattr(obj, 'get_absolute_url') else None,
            'obj': obj
        })

    # --- 3. PDF DOCUMENTS ---
    pdfs = PDFDocument.objects.select_related('author').all()
    for obj in pdfs:
        parties_str = f"Auteur: {obj.author.get_full_name_with_role()}" if obj.author else ""
        
        timeline_items.append({
            'sort_date': obj.document_date or obj.uploaded_at,
            'date_display': fmt_date_short(obj.document_date),
            'exhibit_type': "Document PDF",
            'description': obj.title,
            'parties': parties_str,
            'url': obj.get_absolute_url() if hasattr(obj, 'get_absolute_url') else None,
            'obj': obj
        })

    # --- 4. PDF QUOTES ---
    pdf_quotes = PDFQuote.objects.select_related('pdf_document', 'pdf_document__author').all()
    for obj in pdf_quotes:
        quote_doc = obj.pdf_document
        parties_str = f"Auteur: {quote_doc.author.get_full_name_with_role()}" if quote_doc.author else ""
        desc = f"« {obj.quote_text} » (p. {obj.page_number})"
        
        timeline_items.append({
            'sort_date': quote_doc.document_date or obj.created_at,
            'date_display': fmt_date_short(quote_doc.document_date),
            'exhibit_type': "Citation PDF",
            'description': desc,
            'parties': parties_str,
            'url': obj.get_absolute_url() if hasattr(obj, 'get_absolute_url') else None,
            'obj': obj
        })

    # --- 5. EVENTS ---
    events = Event.objects.all()
    for obj in events:
        # Event parsing logic from services.py
        if ':' in (obj.explanation or ""):
            parts = obj.explanation.rsplit(':', 1)
            # Try to use the date part from string if valid, else fallback
            desc_text = parts[1].strip()
        else:
            desc_text = obj.explanation or ""

        timeline_items.append({
            'sort_date': obj.date or timezone.now(),
            'date_display': fmt_date_short(obj.date),
            'exhibit_type': "Événement",
            'description': desc_text,
            'parties': "", 
            'url': obj.get_absolute_url() if hasattr(obj, 'get_absolute_url') else None,
            'obj': obj
        })

    # --- 6. PHOTO DOCUMENTS ---
    photo_docs = PhotoDocument.objects.select_related('author').all()
    for obj in photo_docs:
        parties_str = f"Auteur: {obj.author.get_full_name_with_role()}" if obj.author else ""
        desc_text = obj.title
        if obj.description: desc_text += f"\n{obj.description}"

        timeline_items.append({
            'sort_date': obj.created_at,
            'date_display': fmt_date(obj.created_at),
            'exhibit_type': "Document Photo",
            'description': desc_text,
            'parties': parties_str,
            'url': obj.get_absolute_url() if hasattr(obj, 'get_absolute_url') else None,
            'obj': obj
        })

    # --- 7. STATEMENTS (Déclarations) ---
    statements = Statement.objects.all()
    for obj in statements:
        # Statements don't have inherent dates usually, use created_at
        timeline_items.append({
            'sort_date': obj.created_at,
            'date_display': fmt_date_short(obj.created_at),
            'exhibit_type': "Déclaration",
            'description': obj.text,
            'parties': "Utilisateur (Manuel)" if obj.is_user_created else "Importé",
            'url': None,
            'obj': obj
        })
        
    # --- 8. GENERAL DOCUMENTS ---
    documents = Document.objects.select_related('author').all()
    for obj in documents:
        parties_str = f"Auteur: {obj.author.get_full_name_with_role()}" if obj.author else ""
        
        timeline_items.append({
            'sort_date': obj.document_original_date or obj.created_at,
            'date_display': fmt_date_short(obj.document_original_date),
            'exhibit_type': "Document (Général)",
            'description': obj.title,
            'parties': parties_str,
            'url': obj.get_absolute_url() if hasattr(obj, 'get_absolute_url') else None,
            'obj': obj
        })

    # --- 9. GOOGLE CHAT SEQUENCES ---
    chat_sequences = ChatSequence.objects.all()
    for obj in chat_sequences:
        if not obj.start_date:
            obj.update_dates()
        
        date_val = obj.start_date or obj.created_at
        
        timeline_items.append({
            'sort_date': date_val,
            'date_display': fmt_date(date_val),
            'exhibit_type': "Extrait Google Chat",
            'description': obj.title,
            'parties': f"{obj.messages.count()} messages",
            'url': None, 
            'obj': obj
        })

    # --- FINAL SORTING ---
    # Ensure sort_date is aware for comparison
    def make_aware_if_naive(dt):
        if timezone.is_naive(dt):
            return timezone.make_aware(dt)
        return dt

    for item in timeline_items:
        if isinstance(item['sort_date'], datetime):
            item['sort_date'] = make_aware_if_naive(item['sort_date'])
        else:
            # Handle date objects (convert to datetime at midnight)
            item['sort_date'] = make_aware_if_naive(datetime.combine(item['sort_date'], datetime.min.time()))

    timeline_items.sort(key=lambda x: x['sort_date'])

    # --- NUMBERING (G-X) ---
    for i, item in enumerate(timeline_items, 1):
        item['label'] = f"G-{i}"

    return timeline_items