from django.contrib.contenttypes.models import ContentType
from django.db import models
from .models import LegalCase, ExhibitRegistry
from argument_manager.models import TrameNarrative

def refresh_case_exhibits(case_id):
    """
    Analyzes all contestations within a case, finds all unique pieces of evidence,
    and assigns a permanent, sequential exhibit number (P-Number) to each one.
    This function is designed to be idempotent and maintain stable numbers.
    """
    try:
        case = LegalCase.objects.get(pk=case_id)
    except LegalCase.DoesNotExist:
        return 0 # Or raise an error

    # 1. Gather ALL unique evidence objects from ALL contestations in this case
    all_evidence_objects = set()
    for contestation in case.contestations.prefetch_related('supporting_narratives__evenements', 'supporting_narratives__citations_courriel__email', 'supporting_narratives__citations_pdf__pdf_document', 'supporting_narratives__photo_documents').all():
        for narrative in contestation.supporting_narratives.all():
            for event in narrative.evenements.all():
                all_evidence_objects.add(event)
            for email_quote in narrative.citations_courriel.all():
                all_evidence_objects.add(email_quote.email)
            for pdf_quote in narrative.citations_pdf.all():
                all_evidence_objects.add(pdf_quote.pdf_document)
            for photo_doc in narrative.photo_documents.all():
                all_evidence_objects.add(photo_doc)
            # Note: We add the core evidence (Email, PDFDocument), not the Quotes themselves.
            
    # 2. Get the current highest exhibit number for this case
    current_max = case.exhibits.aggregate(max_num=models.Max('exhibit_number'))['max_num'] or 0
    
    # 3. Register each unique piece of evidence if it's not already in the registry
    for item in all_evidence_objects:
        if item is None:
            continue # Skip if an evidence link is broken

        ct = ContentType.objects.get_for_model(item)
        
        # get_or_create ensures we don't make duplicates. The number is only assigned
        # if the object is new to this case.
        obj, created = ExhibitRegistry.objects.get_or_create(
            case=case,
            content_type=ct,
            object_id=item.pk,
            defaults={'exhibit_number': current_max + 1}
        )
        
        # If a new exhibit was created, increment the counter for the next potential new one
        if created:
            current_max += 1

    return current_max
