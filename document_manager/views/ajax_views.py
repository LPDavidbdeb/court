from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.db import transaction
import json

from ..models import DocumentNode

@require_POST
@transaction.atomic
def update_node_truth_view(request):
    """
    Handles AJAX requests to update the is_true and is_falsifiable fields of a DocumentNode.
    """
    try:
        data = json.loads(request.body)
        node_id = data.get('node_id')
        field_to_update = data.get('field')
        new_value = data.get('value')

        if not all([node_id, field_to_update, new_value is not None]):
            return JsonResponse({'status': 'error', 'message': 'Invalid data provided.'}, status=400)

        node = get_object_or_404(DocumentNode, pk=node_id)

        if field_to_update == 'is_true':
            node.is_true = new_value
            # Enforce business rule: If a claim is true, it cannot be falsifiable.
            if new_value is True:
                node.is_falsifiable = None
        elif field_to_update == 'is_falsifiable':
            # Enforce business rule: A claim can only be falsifiable if it is false.
            if node.is_true:
                return JsonResponse({'status': 'error', 'message': 'A true statement cannot be marked as falsifiable.'}, status=400)
            node.is_falsifiable = new_value
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid field specified.'}, status=400)

        node.save()
        return JsonResponse({'status': 'success', 'message': f'Node {node_id} updated.'})

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
