import PIL.Image
from datetime import date
from django.template.defaultfilters import date as date_filter
from django.conf import settings

class EvidenceFormatter:
    
    @staticmethod
    def get_date(obj):
        if hasattr(obj, 'document_original_date'):
            return obj.document_original_date or date.min
        elif hasattr(obj, 'document_date'):
            return obj.document_date or date.min
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
    def format_email_group(cls, email, quotes):
        if not email: return "Courriel introuvable."
        
        email_date = date_filter(email.date_sent, "d F Y à H:i")
        sender_display = cls._get_protagonist_display(email.sender_protagonist, email.sender)
        
        if email.recipient_protagonists.exists():
            recipients = [cls._get_protagonist_display(p, "") for p in email.recipient_protagonists.all()]
            recipient_display = ", ".join(recipients)
        else:
            recipient_display = email.recipients_to or "Destinataire inconnu"

        full_body = email.body_plain_text[:3000] + "..." if email.body_plain_text and len(email.body_plain_text) > 3000 else email.body_plain_text

        text = (
            f"--- PREUVE : COURRIEL COMPLET ---\n"
            f"DATE : {email_date}\n"
            f"DE : {sender_display}\n"
            f"À : {recipient_display}\n"
            f"SUJET : « {email.subject} »\n"
            f"CONTENU :\n{full_body}\n"
            f"---------------------------------\n"
        )

        if len(quotes) == 1:
            text += f"CITATION PERTINENTE (De {sender_display} à {recipient_display}, le {email_date}) : « {quotes[0].quote_text} »\n"
        else:
            text += "CITATIONS PERTINENTES DANS CE MESSAGE :\n"
            for i, q in enumerate(quotes, 1):
                text += f"{i}. [De {sender_display} à {recipient_display}, le {email_date}] : « {q.quote_text} »\n"
        
        return text

    @classmethod
    def format_pdf_group(cls, doc, quotes):
        if not doc: return "Document introuvable."
        
        doc_date_obj = None
        if hasattr(doc, 'document_original_date') and doc.document_original_date:
            doc_date_obj = doc.document_original_date
        elif hasattr(doc, 'document_date') and doc.document_date:
            doc_date_obj = doc.document_date
            
        doc_date = date_filter(doc_date_obj, "d F Y") if doc_date_obj else "Date inconnue"
        author_display = cls._get_protagonist_display(doc.author, "Auteur inconnu")

        text = (
            f"--- PREUVE DOCUMENTAIRE (PDF) ---\n"
            f"DOCUMENT : « {doc.title} »\n"
            f"DATE DU DOCUMENT : {doc_date}\n"
            f"AUTEUR : {author_display}\n"
        )
        if doc.ai_analysis:
            text += f"CONTEXTE (RÉSUMÉ IA) : {doc.ai_analysis}\n"
        text += "---------------------------------\n"

        if len(quotes) == 1:
            text += f"EXTRAIT (Page {quotes[0].page_number} - {doc.title}, du {doc_date}) : « {quotes[0].quote_text} »\n"
        else:
            text += "EXTRAITS IDENTIFIÉS :\n"
            for q in quotes:
                text += f"- [Page {q.page_number} de {doc.title}, daté du {doc_date}] : « {q.quote_text} »\n"

        return text

    @staticmethod
    def format_event(event):
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
        timeline_items = []

        email_map = {}
        for quote in narrative.citations_courriel.all().select_related('email', 'email__sender_protagonist'):
            if quote.email not in email_map:
                email_map[quote.email] = []
            email_map[quote.email].append(quote)
        
        for email, quotes in email_map.items():
            timeline_items.append({
                'date': cls.get_date(email),
                'type': 'email_group',
                'obj': email,
                'quotes': quotes
            })

        pdf_map = {}
        for quote in narrative.citations_pdf.all().select_related('pdf_document', 'pdf_document__author'):
            if quote.pdf_document not in pdf_map:
                pdf_map[quote.pdf_document] = []
            pdf_map[quote.pdf_document].append(quote)

        for pdf, quotes in pdf_map.items():
             timeline_items.append({
                'date': cls.get_date(pdf),
                'type': 'pdf_group',
                'obj': pdf,
                'quotes': quotes
            })

        for event in narrative.evenements.all():
            timeline_items.append({'date': cls.get_date(event), 'type': 'event', 'obj': event})

        for photo_doc in narrative.photo_documents.all():
             timeline_items.append({'date': cls.get_date(photo_doc), 'type': 'photo_doc', 'obj': photo_doc})

        timeline_items.sort(key=lambda x: x['date'])

        content_parts = []
        current_text_buffer = f"=== DOSSIER DE PREUVE : {narrative.titre} ===\n"
        current_text_buffer += f"CONTEXTE GÉNÉRAL : {narrative.resume}\n\n"
        current_text_buffer += "--- DÉBUT DE LA CHRONOLOGIE ---\n"

        for item in timeline_items:
            
            if item['type'] == 'email_group':
                current_text_buffer += cls.format_email_group(item['obj'], item['quotes']) + "\n"
            
            elif item['type'] == 'pdf_group':
                current_text_buffer += cls.format_pdf_group(item['obj'], item['quotes']) + "\n"
            
            elif item['type'] == 'event':
                current_text_buffer += cls.format_event(item['obj']) + "\n\n"
            
            elif item['type'] == 'photo_doc':
                if current_text_buffer:
                    content_parts.append(current_text_buffer)
                    current_text_buffer = "" 
                
                obj = item['obj']
                if hasattr(obj, 'ai_analysis') and obj.ai_analysis:
                    text_evidence = (
                        f"--- PREUVE VISUELLE (ANALYSE CERTIFIÉE) ---\n"
                        f"TITRE : {obj.title}\n"
                        f"CONTENU VISUEL (Analysé par IA) : {obj.ai_analysis}\n"
                        f"---------------------------------------------\n"
                    )
                    current_text_buffer = text_evidence
                else:
                    content_parts.append(cls.format_photo_document_text(obj))
                    try:
                        if hasattr(obj, 'file') and obj.file:
                            with obj.file.open('rb') as f:
                                img = PIL.Image.open(f)
                                img.load()
                                content_parts.append(img)
                    except Exception as e:
                        content_parts.append(f"[ERREUR IMAGE : {str(e)}]")

        if current_text_buffer:
            current_text_buffer += "--- FIN DU DOSSIER ---\n"
            content_parts.append(current_text_buffer)

        return content_parts
