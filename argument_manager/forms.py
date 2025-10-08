from django import forms
from tinymce.widgets import TinyMCE
from .models import TrameNarrative
from document_manager.models import DocumentNode
from events.models import Event
from email_manager.models import Quote as EmailQuote
from pdf_manager.models import Quote as PDFQuote

class DocumentNodeChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.text.replace('[PARAGRAPH]', '').strip()

class TrameNarrativeForm(forms.ModelForm):
    allegations_ciblees = DocumentNodeChoiceField(
        queryset=DocumentNode.objects.filter(is_true=False, is_falsifiable=True),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Targeted Allegations"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        link_list = []
        if self.instance and self.instance.pk:
            # Add related events
            events = self.instance.evenements.all()
            if events:
                event_menu = []
                for event in events:
                    event_menu.append({
                        'title': f'Event: {event.date} - {event.explanation[:50]}...',
                        'value': f'<blockquote><p>{event.explanation}</p><cite>Event on {event.date}</cite></blockquote>'
                    })
                link_list.append({'title': 'Events', 'menu': event_menu})

            # Add related email quotes
            email_quotes = self.instance.citations_courriel.all()
            if email_quotes:
                email_quote_menu = []
                for quote in email_quotes:
                    email_quote_menu.append({
                        'title': f'Email Quote: {quote.quote_text[:50]}...',
                        'value': f'<blockquote><p>{quote.quote_text}</p><cite>Email Quote</cite></blockquote>'
                    })
                link_list.append({'title': 'Email Quotes', 'menu': email_quote_menu})

            # Add related PDF quotes
            pdf_quotes = self.instance.citations_pdf.all()
            if pdf_quotes:
                pdf_quote_menu = []
                for quote in pdf_quotes:
                    pdf_quote_menu.append({
                        'title': f'PDF Quote (p.{quote.page_number}): {quote.quote_text[:50]}...',
                        'value': f'<blockquote><p>{quote.quote_text}</p><cite>Source: {quote.pdf_document.title}, page {quote.page_number}</cite></blockquote>'
                    })
                link_list.append({'title': 'PDF Quotes', 'menu': pdf_quote_menu})

        # Configure TinyMCE
        self.fields['resume'].widget = TinyMCE(
            attrs={'cols': 80, 'rows': 30},
            mce_attrs={'link_list': link_list}
        )

    class Meta:
        model = TrameNarrative
        fields = [
            'titre',
            'resume',
            'type_argument',
            'allegations_ciblees',
        ]
