from django.shortcuts import render
from .services import global_semantic_search

def semantic_search_view(request):
    """
    View to display and process global semantic search.
    """
    query = request.GET.get('q', '').strip()
    results = []
    
    if query:
        results = global_semantic_search(query)
        
    return render(request, 'core/semantic_search.html', {
        'query': query,
        'results': results,
    })
