import html

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
