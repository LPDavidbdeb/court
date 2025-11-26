import PIL.Image
from datetime import date
from django.template.defaultfilters import date as date_filter
from django.conf import settings

class EvidenceFormatter:
    
    @staticmethod
    def get_date(obj):
        """Helper to extract a comparable date from any evidence type."""
        if hasattr(obj, 'date'): return obj.date
        elif hasattr(obj, 'date_sent'): return obj.date_sent.date() if obj.date_sent else date.min
        elif hasattr(obj, 'pdf_document'):
            if obj.pdf_document and obj.pdf_document.document_date:
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
    def format_pdf_quote(cls, quote):
        doc = quote.pdf_document
        if not doc: return "Document introuvable."
        doc_date = date_filter(doc.document_date, "d F Y") if doc.document_date else "Date inconnue"
        author_display = cls._get_protagonist_display(doc.author, "Auteur inconnu")
        return (
            f"DOCUMENT OFFICIEL : Le {doc_date}, {author_display} a écrit dans « {doc.title} » (Page {quote.page_number}) :\n"
            f"EXTRAIT : « {quote.quote_text} »"
        )

    @classmethod
    def format_email_quote(cls, quote):
        email = quote.email
        if not email: return "Courriel introuvable."
        email_date = date_filter(email.date_sent, "d F Y à H:i")
        sender_display = cls._get_protagonist_display(email.sender_protagonist, email.sender)
        recipient_display = email.recipients_to 
        return (
            f"COURRIEL : Le {email_date}, {sender_display} a écrit à {recipient_display} "
            f"dans un message intitulé « {email.subject} » :\n"
            f"EXTRAIT : « {quote.quote_text} »"
        )

    @staticmethod
    def format_event(event):
        if event.time:
            event_date = f"{date_filter(event.date, 'd F Y')} à {event.time}"
        else:
            event_date = date_filter(event.date, "d F Y")
        return f"ÉVÉNEMENT : Le {event_date} : {event.explanation}"

    @staticmethod
    def format_photo_document_text(photo_doc):
        doc_date = date_filter(photo_doc.created_at, "d F Y")
        return (
            f"PREUVE VISUELLE (Voir image ci-dessous) : « {photo_doc.title} » (Daté du {doc_date})\n"
            f"DESCRIPTION : {photo_doc.description}\n"
            f"INSTRUCTION : Analyse l'image suivante pour confirmer ces faits."
        )

    @classmethod
    def unpack_narrative_multimodal(cls, narrative):
        timeline = []
        
        for event in narrative.evenements.all():
            timeline.append({'date': cls.get_date(event), 'type': 'event', 'obj': event})
        for quote in narrative.citations_courriel.all().select_related('email', 'email__sender_protagonist'):
            timeline.append({'date': cls.get_date(quote.email), 'type': 'email', 'obj': quote})
        for quote in narrative.citations_pdf.all().select_related('pdf_document', 'pdf_document__author'):
            timeline.append({'date': cls.get_date(quote), 'type': 'pdf', 'obj': quote})
        for photo_doc in narrative.photo_documents.all():
            timeline.append({'date': cls.get_date(photo_doc), 'type': 'photo_doc', 'obj': photo_doc})

        timeline.sort(key=lambda x: x['date'])

        content_parts = []
        current_text_buffer = f"=== DOSSIER DE PREUVE : {narrative.titre} ===\n"
        current_text_buffer += f"CONTEXTE GÉNÉRAL : {narrative.resume}\n\n"
        current_text_buffer += "--- DÉBUT DE LA CHRONOLOGIE ---\n"

        for item in timeline:
            obj = item['obj']
            
            if item['type'] == 'photo_doc':
                if obj.ai_analysis:
                    description = (
                        f"--- PREUVE VISUELLE (ANALYSE CERTIFIÉE) ---\n"
                        f"TITRE : « {obj.title} » (Daté du {date_filter(obj.created_at, 'd F Y')})\n"
                        f"DESCRIPTION : {obj.description}\n"
                        f"CONTENU VISUEL (Analysé par IA) : {obj.ai_analysis}\n"
                        f"---------------------------------------------\n"
                    )
                    current_text_buffer += description
                else:
                    if current_text_buffer:
                        content_parts.append(current_text_buffer)
                        current_text_buffer = "" 
                    
                    content_parts.append(cls.format_photo_document_text(obj))
                    try:
                        # The model field is 'file', not 'image'
                        if hasattr(obj, 'file') and obj.file:
                            with obj.file.open('rb') as f:
                                img = PIL.Image.open(f)
                                img.load()
                                content_parts.append(img)
                    except Exception as e:
                        content_parts.append(f"[ERREUR DE LECTURE IMAGE : {str(e)}]")

            elif item['type'] == 'pdf':
                pdf_text = f"{cls.format_pdf_quote(obj)}\n"
                if obj.pdf_document and obj.pdf_document.ai_analysis:
                     pdf_text += f"CONTEXTE DOCUMENTAIRE (Résumé IA) : {obj.pdf_document.ai_analysis}\n"
                current_text_buffer += pdf_text + "\n"

            else:
                if item['type'] == 'event':
                    current_text_buffer += f"{cls.format_event(obj)}\n\n"
                elif item['type'] == 'email':
                    current_text_buffer += f"{cls.format_email_quote(obj)}\n\n"

        if current_text_buffer:
            current_text_buffer += "--- FIN DU DOSSIER ---\n"
            content_parts.append(current_text_buffer)

        return content_parts
