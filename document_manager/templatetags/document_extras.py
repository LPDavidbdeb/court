from django import template
from datetime import date

register = template.Library()

@register.filter(name='get_model_name')
def get_model_name(value):
    """Returns the name of the model for a given object."""
    if hasattr(value, '__class__'):
        return value.__class__.__name__
    return ''

@register.inclusion_tag('document_manager/partials/_narrative_evidence_list.html')
def display_narrative_evidence(narrative):
    """
    An inclusion tag to display a chronologically sorted list of evidence 
    for a given TrameNarrative object.
    """
    # 1. Create a flat list of all evidence objects.
    flat_evidence_list = []
    
    # Use prefetch_related fields if available
    flat_evidence_list.extend(list(narrative.evenements.all()))
    flat_evidence_list.extend(list(narrative.citations_courriel.all()))
    flat_evidence_list.extend(list(narrative.citations_pdf.all()))
    flat_evidence_list.extend(list(narrative.photo_documents.all()))

    # 2. Define a robust function to get a consistent date for sorting.
    def get_evidence_date(evidence):
        model_name = get_model_name(evidence)
        try:
            if model_name == 'Event':
                return evidence.date
            if model_name == 'Quote':
                if hasattr(evidence, 'email') and evidence.email and evidence.email.date_sent:
                    return evidence.email.date_sent.date()
                if hasattr(evidence, 'pdf_document') and evidence.pdf_document:
                    # Handle cases where document_date might be None
                    return evidence.pdf_document.document_date or evidence.pdf_document.uploaded_at.date()
            if model_name == 'PhotoDocument':
                return evidence.created_at.date()
        except AttributeError:
            # If any attribute is missing, fall back
            return date.max
        return date.max # Fallback for no date or recognized model

    # 3. Sort the flat list chronologically.
    flat_evidence_list.sort(key=get_evidence_date)

    return {'evidence_list': flat_evidence_list}
