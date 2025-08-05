import os
from django.shortcuts import render
from django.conf import settings  # We'll add this to settings.py
from email_manager.forms.EmailSearchForm import EmailSearchForm
from DAL.gmailDAO import GmailDAO
import base64

def email_search_view(request):
    """
    Handles email search based on participant, date, and excerpt.
    Displays a search form and search results.
    """
    form = EmailSearchForm()
    search_results = None
    email_body_content = None
    found_message_id = None
    thread_id = None

    if request.method == 'POST':
        form = EmailSearchForm(request.POST)
        if form.is_valid():
            sender_email = form.cleaned_data['sender_email']
            date_sent = form.cleaned_data['date_sent'].strftime('%Y/%m/%d')  # Format date for DAO
            email_excerpt = form.cleaned_data['email_excerpt']

            # Initialize GmailDAO (ensure client_secret.json is in a known location)
            # You might want to store client_secret_path in Django settings.
            client_secret_path = os.path.join(settings.BASE_DIR, 'client_secret.json')
            client_secret_path = "DL/credentials/gmail_desktop_client.json"
            dao = GmailDAO(client_secret_path)

            if not dao.connect():
                # Handle connection error, e.g., display a message to the user
                search_results = {"error": "Could not connect to Gmail API. Check console for details."}
                return render(request, 'email_manager/search.html', {
                    'form': form,
                    'search_results': search_results
                })

            # 1. Get thread ID first
            thread_id = dao.get_thread_id_by_participant_and_date(sender_email, date_sent)

            if thread_id:
                # 2. Get raw messages in the thread
                raw_messages = dao.get_raw_thread_messages(thread_id)

                if raw_messages:
                    # Filter messages in the thread by excerpt if provided
                    found_message = None
                    for msg in raw_messages:
                        # For simplicity, we'll get the raw message content and search for the excerpt.
                        # In a real application, you might want a more robust email parsing library.
                        full_message_data = dao.get_raw_message(msg['id'])
                        if full_message_data and 'payload' in full_message_data:
                            # Attempt to find the body part
                            parts = full_message_data['payload'].get('parts', [])
                            body_data = None
                            for part in parts:
                                if part['mimeType'] == 'text/plain' and 'body' in part and 'data' in part['body']:
                                    body_data = part['body']['data']
                                    break
                                elif part['mimeType'] == 'text/html' and 'body' in part and 'data' in part['body']:
                                    body_data = part['body']['data']  # Prefer HTML if available
                                    break

                            if body_data:
                                decoded_body = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')
                                if email_excerpt:
                                    if email_excerpt.lower() in decoded_body.lower():
                                        found_message = msg
                                        email_body_content = decoded_body  # Store content of the matching email
                                        found_message_id = msg['id']
                                        break  # Found the message with excerpt, stop
                                else:
                                    # If no excerpt, just take the first message in the thread as a "match"
                                    found_message = msg
                                    email_body_content = decoded_body
                                    found_message_id = msg['id']
                                    break  # Found a message, stop

                    if found_message:
                        search_results = {
                            "status": "success",
                            "message": f"Found a matching email in thread ID: {thread_id}",
                            "message_id": found_message_id,
                            "email_body": email_body_content,
                            "thread_id": thread_id  # Pass thread_id to the template
                        }
                    else:
                        search_results = {
                            "status": "not_found",
                            "message": "No email found in the thread matching the excerpt."
                        }
                else:
                    search_results = {
                        "status": "not_found",
                        "message": "No messages found in the specified thread."
                    }
            else:
                search_results = {
                    "status": "not_found",
                    "message": "No thread found matching the participant and date."
                }

    context = {
        'form': form,
        'search_results': search_results,
        'email_body_content': email_body_content,
        'found_message_id': found_message_id,
        'thread_id': thread_id,  # Also pass thread_id to the template
    }
    return render(request, 'email_manager/search.html', context)


from django.shortcuts import render

# Create your views here.
