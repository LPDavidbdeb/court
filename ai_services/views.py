import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .services import analyze_document_content
from pdf_manager.models import PDFDocument
from photos.models import PhotoDocument

def trigger_ai_analysis(request, doc_type, pk):
    if doc_type == 'pdf':
        obj = get_object_or_404(PDFDocument, pk=pk)
    elif doc_type == 'photo':
        obj = get_object_or_404(PhotoDocument, pk=pk)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid type'}, status=400)

    # 1. Default Persona
    persona_key = 'forensic_clerk'

    # 2. Check for POST data (JSON)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            persona_key = data.get('persona', persona_key)
        except json.JSONDecodeError:
            pass
    
    # 3. Pass persona to service
    success = analyze_document_content(obj, persona_key=persona_key)

    if success:
        return JsonResponse({'status': 'success', 'analysis': obj.ai_analysis})
    else:
        return JsonResponse({'status': 'error', 'message': 'Analysis failed'}, status=500)

@require_POST
def clear_ai_analysis(request, doc_type, pk):
    if doc_type == 'pdf':
        obj = get_object_or_404(PDFDocument, pk=pk)
    elif doc_type == 'photo':
        obj = get_object_or_404(PhotoDocument, pk=pk)
    else:
        # Or return a JsonResponse for API clients
        return JsonResponse({'status': 'error', 'message': 'Invalid document type'}, status=400)

    obj.ai_analysis = ''
    obj.save()

    # This view is now designed to be called via fetch, so we return JSON.
    return JsonResponse({'status': 'success', 'message': 'Analysis cleared.'})
