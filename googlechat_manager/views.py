from django.http import JsonResponse
from django.shortcuts import render
from .models import ChatMessage
from django.core.paginator import Paginator

def single_chat_stream(request):
    """
    Renders a single, continuous chat stream view.
    Initially loads the latest page of messages.
    """
    all_messages = ChatMessage.objects.select_related('sender').order_by('timestamp')
    paginator = Paginator(all_messages, 50)
    last_page_num = paginator.num_pages
    page_obj = paginator.page(last_page_num)
    
    context = {
        'chat_messages': page_obj.object_list, # Renamed from 'messages'
        'page_number': last_page_num,
        'has_previous': page_obj.has_previous(),
    }
    return render(request, 'googlechat_manager/chat_stream.html', context)


def load_more_messages(request):
    """
    API endpoint to fetch a specific page of older messages.
    """
    page_number = int(request.GET.get('page', 1))
    
    all_messages = ChatMessage.objects.select_related('sender').order_by('timestamp')
    paginator = Paginator(all_messages, 50)
    
    if page_number < 1 or page_number > paginator.num_pages:
        return JsonResponse({'messages': [], 'has_previous': False})
        
    page_obj = paginator.page(page_number)
    
    messages_data = [
        {
            'sender_name': msg.sender.name if msg.sender else "Unknown",
            'text_content': msg.text_content,
            'timestamp': msg.timestamp.strftime('%b %d, %Y, %I:%M %p'),
        }
        for msg in page_obj.object_list
    ]
    
    # The key 'messages' here is for the JSON response, which is fine.
    # It does not conflict with the Django template context.
    return JsonResponse({
        'messages': messages_data,
        'has_previous': page_obj.has_previous(),
    })