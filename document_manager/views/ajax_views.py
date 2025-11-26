from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
import json
from ..models import Statement
from ai_services.services import analyze_document_content
from pdf_manager.models import PDFDocument
from photos.models import PhotoDocument

@require_POST
def update_statement_flags(request):
    try:
        data = json.loads(request.body)
        statement_id = data.get('statement_id')
        field = data.get('field')
        value = data.get('value')

        if not all([statement_id, field, value is not None]):
            return JsonResponse({'status': 'error', 'message': 'Missing data.'}, status=400)

        if field not in ['is_true', 'is_falsifiable']:
            return JsonResponse({'status': 'error', 'message': 'Invalid field.'}, status=400)

        statement = Statement.objects.get(pk=statement_id)
        
        if field == 'is_true' and value is True:
            statement.is_falsifiable = False
        
        setattr(statement, field, value)
        statement.save()

        return JsonResponse({'status': 'success', 'message': 'Statement updated.'})

    except Statement.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Statement not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

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
