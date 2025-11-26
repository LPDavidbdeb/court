from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from ..models import Statement

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
        
        # Enforce logic: if is_true is set to True, is_falsifiable must be False
        if field == 'is_true' and value is True:
            statement.is_falsifiable = False
        
        setattr(statement, field, value)
        statement.save()

        return JsonResponse({'status': 'success', 'message': 'Statement updated.'})

    except Statement.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Statement not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
