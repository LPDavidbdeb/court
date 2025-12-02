import html
import re
from datetime import date
from django.contrib.contenttypes.models import ContentType
from collections import defaultdict
from document_manager.models import LibraryNode, Statement

class EvidenceFormatter:
    
    @staticmethod
    def _xml_escape(text):
        if not text: return ""
        return html.escape(str(text))

    @classmethod
    def format_narrative_context_xml(cls, narrative):
        """
        Génère le dossier XML strict pour une seule Trame Narrative.
        Utilisé par l'Auditeur IA.
        """
        xml_output = [f'<dossier_analyse id="TRAME-{narrative.pk}">']

        # 1. LES ALLÉGATIONS (La Thèse Adverse)
        xml_output.append('  <theses_adverses>')
        for stmt in narrative.targeted_statements.all():
            clean_text = cls._xml_escape(stmt.text)
            xml_output.append(f'    <allegation id="A-{stmt.pk}">{clean_text}</allegation>')
        xml_output.append('  </theses_adverses>')

        # 2. LES PREUVES (La Chronologie Factuelle)
        timeline = narrative.get_chronological_evidence()
        xml_output.append('  <elements_preuve>')
        
        for item in timeline:
            obj = item['object']
            date_str = item['date'].isoformat() if item['date'] else "ND"
            type_ref = item['type']
            
            # Gestion des différents types
            if type_ref == 'email':
                # Pour les emails, on veut l'extrait cité
                quote_text = cls._xml_escape(obj.quote_text)
                subject = cls._xml_escape(obj.email.subject)
                sender = cls._xml_escape(obj.email.sender)
                xml_output.append(f'    <preuve type="email" date="{date_str}" id="P-EMAIL-{obj.pk}">')
                xml_output.append(f'      <meta de="{sender}" sujet="{subject}" />')
                xml_output.append(f'      <contenu>{quote_text}</contenu>')
                xml_output.append('    </preuve>')

            elif type_ref == 'event':
                desc = cls._xml_escape(obj.explanation)
                xml_output.append(f'    <preuve type="evenement" date="{date_str}" id="P-EVENT-{obj.pk}">')
                xml_output.append(f'      <description>{desc}</description>')
                xml_output.append('    </preuve>')

            elif type_ref == 'photo':
                desc = cls._xml_escape(obj.description or obj.ai_analysis or "Photo sans description")
                title = cls._xml_escape(obj.title)
                xml_output.append(f'    <preuve type="photo" date="{date_str}" id="P-PHOTO-{obj.pk}">')
                xml_output.append(f'      <titre>{title}</titre>')
                xml_output.append(f'      <analyse_visuelle>{desc}</analyse_visuelle>')
                xml_output.append('    </preuve>')
            
            elif type_ref == 'chat':
                title = cls._xml_escape(obj.title)
                xml_output.append(f'    <preuve type="chat" date="{date_str}" id="P-CHAT-{obj.pk}">')
                xml_output.append(f'      <titre>{title}</titre>')
                for msg in obj.messages.all():
                    sender = cls._xml_escape(msg.sender.name)
                    content = cls._xml_escape(msg.text_content)
                    xml_output.append(f'      <message de="{sender}">{content}</message>')
                xml_output.append('    </preuve>')

        xml_output.append('  </elements_preuve>')
        xml_output.append('</dossier_analyse>')
        
        return "\n".join(xml_output)

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
        statement_ids = []

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
            
            statement_ids.extend(list(narrative.source_statements.values_list('id', flat=True)))

        # Process Statements
        if statement_ids:
            stmt_content_type = ContentType.objects.get_for_model(Statement)
            nodes = LibraryNode.objects.filter(
                content_type=stmt_content_type,
                object_id__in=statement_ids
            ).select_related('document')
            
            for node in nodes:
                global_data['unique_documents'].add(node.document)
                global_data['timeline'].append({
                    'date': cls.get_date(node.document),
                    'type': 'statement_entry',
                    'obj': node.content_object,
                    'parent_doc': node.document
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
            text = f"[ {date_str} ] PHOTO{label_str} : « {obj.title} »\n"
            
            if hasattr(obj, 'ai_analysis') and obj.ai_analysis:
                analysis_preview = (obj.ai_analysis[:400] + '...') if len(obj.ai_analysis) > 400 else obj.ai_analysis
                analysis_preview = analysis_preview.replace('\n', ' ').replace('\r', '')
                text += f"    -> CONTENU VISUEL/TEXTUEL : {analysis_preview}\n"
            
            elif obj.description:
                 text += f"    -> DESCRIPTION : {obj.description}\n"
                 
            return text
        
        elif item['type'] == 'statement_entry':
            parent_doc = item.get('parent_doc')
            doc_title = parent_doc.title if parent_doc else "Document inconnu"
            text = f"[ {date_str} ] DÉCLARATION{label_str} (Source: {doc_title}) : « {obj.text} »\n"
            return text

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

    @classmethod
    def format_full_chronology(cls, narratives_queryset):
        """
        Génère une chronologie textuelle complète à partir d'un queryset de TrameNarrative.
        """
        full_timeline = []
        for narrative in narratives_queryset:
            full_timeline.extend(narrative.get_chronological_evidence())
        
        # Sort all collected items by date
        sorted_timeline = sorted([item for item in full_timeline if item['date']], key=lambda x: x['date'])
        
        # Format into a single string
        output_lines = []
        for item in sorted_timeline:
            date_str = item['date'].strftime('%Y-%m-%d')
            obj = item['object']
            item_type = item['type']
            
            line = f"[{date_str}] "
            if item_type == 'email':
                line += f"EMAIL: De {obj.email.sender}, Sujet: {obj.email.subject}, Citation: '{obj.quote_text}'"
            elif item_type == 'pdf':
                line += f"PDF: '{obj.pdf_document.title}', Page {obj.page_number}, Citation: '{obj.quote_text}'"
            elif item_type == 'event':
                line += f"ÉVÉNEMENT: {obj.explanation}"
            elif item_type == 'photo':
                line += f"PHOTO: '{obj.title}' - {obj.description or obj.ai_analysis or ''}"
            elif item_type == 'chat':
                line += f"CHAT: '{obj.title}'"
            
            output_lines.append(line)
            
        return "\n".join(output_lines)
