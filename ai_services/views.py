from django.http import JsonResponse
from django.shortcuts import get_object_or_404
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

    success = analyze_document_content(obj)

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
        return JsonResponse({'status': 'error', 'message': 'Invalid type'}, status=400)

    # Clear the field
    obj.ai_analysis = ""
    obj.save()

    return JsonResponse({'status': 'success', 'message': 'Analysis cleared.'})
