from django import forms
from tinymce.widgets import TinyMCE
from .models import TrameNarrative, PerjuryArgument
from document_manager.models import LibraryNode, Statement # REFACTORED
from events.models import Event
from email_manager.models import Quote as EmailQuote
from pdf_manager.models import Quote as PDFQuote
from django.contrib.contenttypes.models import ContentType

# REFACTORED: This field now handles LibraryNode objects
class LibraryNodeChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        # obj is a LibraryNode instance. We try to get its linked statement text.
        if hasattr(obj, 'content_object') and isinstance(obj.content_object, Statement):
            statement_text = obj.content_object.text
            return f"{obj.item}: '{statement_text[:50]}...'"
        return obj.item # Fallback for nodes without a statement

class TrameNarrativeForm(forms.ModelForm):
    # REFACTORED: The queryset now targets LibraryNode
    allegations_ciblees = LibraryNodeChoiceField(
        # Query for LibraryNode objects whose content_object is a Statement
        # that meets the perjury criteria.
        queryset=LibraryNode.objects.filter(
            content_type=ContentType.objects.get_for_model(Statement),
            object_id__in=Statement.objects.filter(is_true=False, is_falsifiable=True).values_list('id', flat=True)
        ).select_related('content_type'), # Use select_related for efficiency
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Targeted Allegations"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        link_list = []
        if self.instance and self.instance.pk:
            # This part of the logic remains the same as it deals with the
            # relationships on the TrameNarrative model itself, which have not changed.
            events = self.instance.evenements.all()
            if events:
                event_menu = []
                for event in events:
                    event_menu.append({
                        'title': f'Event: {event.date} - {event.explanation[:50]}...',
                        'value': f'<blockquote><p>{event.explanation}</p><cite>Event on {event.date}</cite></blockquote>'
                    })
                link_list.append({'title': 'Events', 'menu': event_menu})

            email_quotes = self.instance.citations_courriel.all()
            if email_quotes:
                email_quote_menu = []
                for quote in email_quotes:
                    email_quote_menu.append({
                        'title': f'Email Quote: {quote.quote_text[:50]}...',
                        'value': f'<blockquote><p>{quote.quote_text}</p><cite>Email Quote</cite></blockquote>'
                    })
                link_list.append({'title': 'Email Quotes', 'menu': email_quote_menu})

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
            attrs={'cols': 80, 'rows': 30, 'style': 'width: 100%;'},
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

class PerjuryArgumentForm(forms.ModelForm):
    class Meta:
        model = PerjuryArgument
        fields = [
            'trame_narrative',
            'targeted_statements',
            'title',
            'order',
            'text_declaration',
            'text_proof',
            'text_mens_rea',
            'text_intent',
        ]
        widgets = {
            'text_declaration': TinyMCE(attrs={'cols': 80, 'rows': 10}),
            'text_proof': TinyMCE(attrs={'cols': 80, 'rows': 10}),
            'text_mens_rea': TinyMCE(attrs={'cols': 80, 'rows': 10}),
            'text_intent': TinyMCE(attrs={'cols': 80, 'rows': 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['targeted_statements'].queryset = Statement.objects.filter(
            is_true=False, is_falsifiable=True
        )
