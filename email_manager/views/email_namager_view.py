import os
import base64
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from dateutil import parser
import email
import uuid

# Local application imports
from DAL.gmailDAO import GmailDAO, ThreadNotFoundError
from DAL.EmailFileDAO import EmlFileDAO
from protagonist_manager.models import Protagonist, ProtagonistEmail
from ..forms import EmailAjaxSearchForm, EmlUploadForm
from ..models import Email, EmailThread


def email_search_view(request):
    """
    Handles searching for emails on the Gmail API.
    """
    form = EmailAjaxSearchForm()
    if request.method != 'POST':
        return render(request, 'email_manager/ajax_search.html', {'form': form})

    form = EmailAjaxSearchForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Invalid search form.")
        return render(request, 'email_manager/ajax_search.html', {'form': form})

    context = _perform_gmail_search(form.cleaned_data)
    context['form'] = form
    return render(request, 'email_manager/ajax_search.html', context)


@require_POST
def save_thread_view(request):
    """
    Saves an entire email thread from Gmail.
    """
    thread_id = request.POST.get('thread_id')
    protagonist_id = request.POST.get('protagonist_id')

    if not thread_id:
        messages.error(request, "No Thread ID provided for saving.")
        return HttpResponseRedirect(reverse('email_manager:email_search'))

    if EmailThread.objects.filter(thread_id=thread_id).exists():
        messages.warning(request, f"Thread (ID: {thread_id}) has already been saved.")
        existing_thread = EmailThread.objects.get(thread_id=thread_id)
        return redirect('email_manager:email_detail', pk=existing_thread.pk)

    dao = GmailDAO()
    if not dao.connect():
        messages.error(request, "Could not connect to Gmail API.")
        return HttpResponseRedirect(reverse('email_manager:email_search'))

    try:
        raw_messages = dao.get_raw_thread_messages(thread_id)
        if not raw_messages:
            messages.error(request, f"Could not retrieve thread data for ID: {thread_id}.")
            return HttpResponseRedirect(reverse('email_manager:email_search'))

        linked_protagonist = Protagonist.objects.filter(pk=protagonist_id).first()

        first_email_data = EmlFileDAO.parse_raw_message_data(raw_messages[0])
        new_thread = EmailThread.objects.create(
            thread_id=thread_id,
            protagonist=linked_protagonist,
            subject=first_email_data['headers'].get('Subject', '(No Subject)'),
        )

        for raw_msg in raw_messages:
            email_data = EmlFileDAO.parse_raw_message_data(raw_msg)
            date_sent_dt = parser.parse(email_data['headers'].get('Date')) if email_data['headers'].get('Date') else None

            Email.objects.create(
                thread=new_thread,
                message_id=email_data['id'],
                dao_source='gmail',
                subject=email_data['headers'].get('Subject'),
                sender=email_data['headers'].get('From'),
                recipients_to=email_data['headers'].get('To'),
                recipients_cc=email_data['headers'].get('Cc'),
                recipients_bcc=email_data['headers'].get('Bcc'),
                date_sent=date_sent_dt,
                body_plain_text=email_data['body_plain_text'],
            )

        messages.success(request, f"Successfully saved thread '{new_thread.subject}'.")
        return redirect('email_manager:email_detail', pk=new_thread.pk)

    except Exception as e:
        messages.error(request, f"An error occurred while saving the thread: {e}")
        return HttpResponseRedirect(reverse('email_manager:email_search'))


def email_detail_view(request, pk):
    thread = get_object_or_404(EmailThread, pk=pk)
    emails_in_thread = thread.emails.all()
    context = {
        'thread': thread,
        'emails_in_thread': emails_in_thread,
        'email': emails_in_thread.first() if emails_in_thread else None,
        'flattened_thread': emails_in_thread,
    }
    return render(request, 'email_manager/email_detail.html', context)


def email_list_view(request):
    email_threads = EmailThread.objects.all().order_by('-updated_at')
    context = {'email_threads': email_threads}
    return render(request, 'email_manager/email_list.html', context)


@require_POST
def email_delete_view(request, pk):
    thread = get_object_or_404(EmailThread, pk=pk)
    thread_subject = thread.subject
    for email_record in thread.emails.all():
        if email_record.eml_file_path and os.path.exists(email_record.eml_file_path):
            try:
                os.remove(email_record.eml_file_path)
            except OSError as e:
                messages.warning(request, f"Failed to delete EML file {email_record.eml_file_path}: {e}")
    thread.delete()
    messages.success(request, f"Thread '{thread_subject}' and all its messages deleted successfully.")
    return HttpResponseRedirect(reverse('email_manager:email_list'))


def upload_eml_view(request):
    if request.method == 'POST':
        form = EmlUploadForm(request.POST, request.FILES)
        if form.is_valid():
            messages.error(request, "EML upload functionality is under construction.")
    else:
        form = EmlUploadForm()
    return render(request, 'email_manager/upload_eml.html', {'form': form})


def _perform_gmail_search(cleaned_data):
    # 1. Get and validate search parameters
    protagonist_id = cleaned_data['protagonist_id']
    manual_participant_email = cleaned_data['manual_participant_email']
    date_sent_str = cleaned_data['date_sent'].strftime('%Y/%m/%d')
    email_excerpt = cleaned_data.get('email_excerpt', '').strip()

    participant_email = manual_participant_email
    selected_protagonist = None
    if protagonist_id:
        try:
            selected_protagonist = Protagonist.objects.get(pk=protagonist_id)
            if selected_protagonist.emails.exists():
                participant_email = selected_protagonist.emails.first().email_address
        except Protagonist.DoesNotExist:
            return {'search_results': {'status': 'error', 'message': 'Selected protagonist not found.'}}

    if not participant_email:
        return {'search_results': {'status': 'error', 'message': 'Please select a protagonist or enter an email.'}}

    # 2. Connect to Gmail and get all matching thread IDs
    dao = GmailDAO()
    if not dao.connect():
        return {'search_results': {'status': 'error', 'message': 'Could not connect to Gmail API.'}}

    all_thread_ids = dao.get_thread_ids_by_participant_and_date(participant_email, date_sent_str)
    if not all_thread_ids:
        return {'search_results': {'status': 'not_found', 'message': 'No email threads found for that participant and date.'}}

    # 3. Filter out threads that are already saved to find only new ones
    saved_thread_ids = set(EmailThread.objects.filter(thread_id__in=all_thread_ids).values_list('thread_id', flat=True))
    new_thread_ids = [tid for tid in all_thread_ids if tid not in saved_thread_ids]

    if not new_thread_ids:
        return {'search_results': {'status': 'not_found', 'message': 'No new, unsaved threads were found. All matching threads for that date have already been saved.'}}

    # 4. Process new threads to find a match
    for thread_id in new_thread_ids:
        raw_messages = dao.get_raw_thread_messages(thread_id)
        if not raw_messages: continue

        parsed_messages = [EmlFileDAO.parse_raw_message_data(msg) for msg in raw_messages]
        if not parsed_messages: continue

        email_thread_obj = {
            'id': thread_id,
            'messages': parsed_messages,
            'subject': parsed_messages[0]['headers'].get('Subject', '(No Subject)')
        }

        # If no excerpt is provided, the first new thread is our match.
        if not email_excerpt:
            return {
                'search_results': {'status': 'success', 'thread': email_thread_obj},
                'selected_protagonist': selected_protagonist
            }
        # Otherwise, search for the excerpt in the new thread.
        else:
            match_found = any(email_excerpt.lower() in msg.get('body_plain_text', '').lower() for msg in parsed_messages)
            if match_found:
                return {
                    'search_results': {'status': 'success', 'thread': email_thread_obj},
                    'selected_protagonist': selected_protagonist
                }

    # 5. If the loop finishes, it means we found new threads, but none matched the excerpt.
    return {'search_results': {'status': 'not_found', 'message': 'Found new threads, but none contained the specified text.'}}
