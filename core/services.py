from pgvector.django import CosineDistance
from email_manager.models import Email
from pdf_manager.models import PDFDocument
from photos.models import PhotoDocument
from document_manager.models import Document
from events.models import Event
from ai_services.services import generate_embedding
from core.mixins import ExhibitableMixin

def global_semantic_search(query_text, limit=10):
    """
    Searches across all primary evidence sources using vector embeddings.
    Leverages the ExhibitableMixin interface for consistent result formatting.
    """
    query_vector = generate_embedding(query_text)
    if not query_vector:
        return []

    results = []
    
    search_configs = [
        {'model': Email, 'type': 'Email', 'icon': 'bi-envelope'},
        {'model': PDFDocument, 'type': 'PDF', 'icon': 'bi-file-pdf'},
        {'model': Event, 'type': 'Événement', 'icon': 'bi-calendar-event'},
        {'model': PhotoDocument, 'type': 'Photo', 'icon': 'bi-camera'},
        {'model': Document, 'type': 'Document', 'icon': 'bi-file-earmark-text'},
    ]

    for config in search_configs:
        qs = config['model'].objects.annotate(
            distance=CosineDistance('embedding', query_vector)
        ).filter(embedding__isnull=False).order_by('distance')[:limit]
        
        for obj in qs:
            if isinstance(obj, ExhibitableMixin):
                results.append({
                    'type': obj.get_exhibit_type(),
                    'icon': config['icon'],
                    'title': obj.get_exhibit_title(),
                    'content': obj.get_exhibit_description(),
                    'date': obj.get_exhibit_date(),
                    'distance': obj.distance,
                    'url': obj.get_absolute_url() if hasattr(obj, 'get_absolute_url') else "#"
                })
            else:
                # Fallback for models without Mixin
                results.append({
                    'type': config['type'],
                    'icon': config['icon'],
                    'title': str(obj),
                    'content': "",
                    'date': None,
                    'distance': obj.distance,
                    'url': "#"
                })

    # Sort all results by distance (closest first)
    results.sort(key=lambda x: x['distance'])

    return results[:limit]
