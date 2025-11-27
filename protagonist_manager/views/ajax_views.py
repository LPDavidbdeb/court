from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_POST
import json

from ..models import Protagonist

def search_protagonists_ajax(request):
    """
    An AJAX view that searches for protagonists based on a query term.
    """
    term = request.GET.get('term', '')
    
    protagonists = Protagonist.objects.filter(
        Q(first_name__icontains=term) | Q(last_name__icontains=term)
    )[:15]

    results = [
        {
            'id': protagonist.id,
            'text': protagonist.get_full_name()
        }
        for protagonist in protagonists
    ]
    
    return JsonResponse(results, safe=False)

@require_POST
def update_protagonist_role_ajax(request):
    """
    An AJAX view to update the role of a protagonist.
    """
    try:
        data = json.loads(request.body)
        protagonist_id = data.get('protagonist_id')
        new_role = data.get('role')

        if protagonist_id is None or new_role is None:
            return JsonResponse({'status': 'error', 'message': 'Missing data.'}, status=400)

        protagonist = Protagonist.objects.get(pk=protagonist_id)
        protagonist.role = new_role
        protagonist.save(update_fields=['role'])

        return JsonResponse({'status': 'success', 'message': 'Role updated successfully.'})

    except Protagonist.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Protagonist not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
