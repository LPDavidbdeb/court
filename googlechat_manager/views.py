from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator
from .models import ChatMessage, ChatSequence
from .forms import ChatSequenceForm
import json

def single_chat_stream(request):
    """
    Renders the main chat stream view, which now includes the sequence picker UI.
    """
    all_messages = ChatMessage.objects.select_related('sender').order_by('timestamp')
    paginator = Paginator(all_messages, 50)
    last_page_num = paginator.num_pages
    page_obj = paginator.page(last_page_num)
    
    context = {
        'chat_messages': page_obj.object_list,
        'page_number': last_page_num,
        'has_previous': page_obj.has_previous(),
    }
    return render(request, 'googlechat_manager/chat_stream.html', context)

def load_more_messages(request):
    """
    API endpoint to fetch older messages, now including the message ID.
    """
    page_number = int(request.GET.get('page', 1))
    all_messages = ChatMessage.objects.select_related('sender').order_by('timestamp')
    paginator = Paginator(all_messages, 50)
    
    if page_number < 1 or page_number > paginator.num_pages:
        return JsonResponse({'messages': [], 'has_previous': False})
        
    page_obj = paginator.page(page_number)
    
    messages_data = [
        {
            'id': msg.id, # Crucial for the selection logic
            'sender_name': msg.sender.name if msg.sender else "Unknown",
            'text_content': msg.text_content,
            'timestamp': msg.timestamp.strftime('%b %d, %Y, %I:%M %p'),
        }
        for msg in page_obj.object_list
    ]
    
    return JsonResponse({
        'messages': messages_data,
        'has_previous': page_obj.has_previous(),
    })

def chat_sequence_list(request):
    """List all created sequences for management."""
    sequences = ChatSequence.objects.prefetch_related('messages').order_by('-created_at')
    return render(request, 'googlechat_manager/sequence_list.html', {'sequences': sequences})

@require_POST
def create_sequence_ajax(request):
    """Receives a list of message IDs and a title to create a sequence."""
    data = json.loads(request.body)
    message_ids = data.get('message_ids', [])
    title = data.get('title')

    if not title or not message_ids:
        return JsonResponse({'status': 'error', 'message': 'Missing data'}, status=400)

    sequence = ChatSequence.objects.create(title=title)
    msgs = ChatMessage.objects.filter(id__in=message_ids)
    sequence.messages.set(msgs)
    sequence.update_dates()

    return JsonResponse({
        'status': 'success', 
        'redirect_url': '/chat/sequences/'
    })

@require_POST
def delete_sequence(request, pk):
    seq = get_object_or_404(ChatSequence, pk=pk)
    seq.delete()
    messages.success(request, "Sequence deleted.")
    return redirect('googlechat:sequence_list')