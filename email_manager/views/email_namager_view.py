import os
import base64
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from dateutil import parser
import email # Python's built-in email package
import uuid # For generating unique message IDs for uploaded EMLs if needed


# Corrected import paths based on your clarification:

from Models.Email2 import Email
from Models.EmailTread import EmailThread
from DAL.gmailDAO import GmailDAO, ThreadNotFoundError
from DAL.EmailFileDAO import EmlFileDAO

# Import Protagonist model
from protagonist_manager.models import Protagonist, ProtagonistEmail

#from ..forms.EmailSearchForm import EmailSearchForm
from ..forms.EmailAjaxSearchForm import EmailAjaxSearchForm
from ..forms.EmailUploadForm import EmlUploadForm
from ..models import SavedEmail


def email_search_view(request):
    """
    Handles email search based on participant (Protagonist or manual email), date, and excerpt.
    Displays a search form and search results, utilizing Email and EmailThread classes.
    Now handles multiple threads for the same participant and date.
    """
    form = EmailAjaxSearchForm()
    search_results = None
    found_email_object = None
    selected_protagonist = None
    found_message_id = None
    thread_id = None

    if request.method == 'POST':
        form = EmailAjaxSearchForm(request.POST)
        if form.is_valid():
            protagonist_id = form.cleaned_data['protagonist_id']
            manual_participant_email = form.cleaned_data['manual_participant_email']
            date_sent_str = form.cleaned_data['date_sent'].strftime('%Y/%m/%d')
            email_excerpt = form.cleaned_data['email_excerpt']

            participant_email_for_dao = None

            if protagonist_id:
                try:
                    selected_protagonist = Protagonist.objects.get(pk=protagonist_id)
                    if selected_protagonist.emails.exists():
                        participant_email_for_dao = selected_protagonist.emails.first().email_address
                    else:
                        messages.warning(request, "Selected protagonist has no email addresses. Please add one or use manual email search.")
                        return render(request, 'email_manager/ajax_search.html', {'form': form})
                except Protagonist.DoesNotExist:
                    messages.error(request, "Selected protagonist not found.")
                    return render(request, 'email_manager/ajax_search.html', {'form': form})
            elif manual_participant_email:
                participant_email_for_dao = manual_participant_email
            else:
                messages.error(request, "Please select a protagonist or enter a specific email address to search.")
                return render(request, 'email_manager/ajax_search.html', {'form': form})

            if not participant_email_for_dao:
                messages.error(request, "No participant email could be determined for search.")
                return render(request, 'email_manager/ajax_search.html', {'form': form})

            dao = GmailDAO()
            if not dao.connect():
                messages.error(request, "Could not connect to Gmail API. Please check server logs.")
                return render(request, 'email_manager/ajax_search.html', {'form': form})

            # --- NEW LOGIC TO HANDLE MULTIPLE THREADS ---
            thread_ids = dao.get_thread_ids_by_participant_and_date(participant_email_for_dao, date_sent_str)

            if not thread_ids:
                search_results = {
                    "status": "not_found",
                    "message": "No email threads found matching the participant and date."
                }
            else:
                # Loop through all found threads to find a matching email
                for current_thread_id in thread_ids:
                    raw_messages = dao.get_raw_thread_messages(current_thread_id)
                    if not raw_messages:
                        continue  # Skip this thread if it's empty or fails to load

                    email_thread = EmailThread(raw_messages, dao_instance=dao, source="gmail")

                    if email_excerpt:
                        matching_emails = email_thread.find_emails_by_string(email_excerpt, case_sensitive=False)
                        if matching_emails:
                            found_email_object = matching_emails[0]
                            break  # Found a match, stop searching other threads
                    else:
                        # If no excerpt, just use the first message of the first valid thread
                        if email_thread.messages:
                            found_email_object = email_thread.messages[0]
                            break # Stop after finding the first message

                # After the loop, check if we found an email
                if found_email_object:
                    found_message_id = found_email_object.id
                    thread_id = found_email_object.thread_id
                    search_results = {
                        "status": "success",
                        "message": f"Found a matching email in thread ID: {thread_id}",
                        "message_id": found_message_id,
                        "thread_id": thread_id
                    }
                else:
                    # If loop finishes with no found email
                    search_results = {
                        "status": "not_found",
                        "message": "Found email threads, but no specific email matched the excerpt."
                    }

    context = {
        'form': form,
        'search_results': search_results,
        'found_message_id': found_message_id,
        'thread_id': thread_id,
        'found_email_object': found_email_object,
        'selected_protagonist': selected_protagonist,
    }
    return render(request, 'email_manager/ajax_search.html', context)


@require_POST
def save_email_view(request):
    """
    Handles saving a found email to the database and as an .eml file.
    It now also links to an existing Protagonist or creates a new one.
    Redirects to the detail view of the saved email on success, or to search on error.
    """
    message_id = request.POST.get('message_id')
    protagonist_id = request.POST.get('protagonist_id')
    search_participant_email = request.POST.get('search_participant_email')
    protagonist_search_name = request.POST.get('protagonist_search_name', '').strip()

    if not message_id:
        messages.error(request, "No message ID provided for saving.")
        return HttpResponseRedirect(reverse('email_manager:email_search'))

    dao = GmailDAO()

    if not dao.connect():
        messages.error(request, "Could not connect to Gmail API to save email. Check server logs.")
        return HttpResponseRedirect(reverse('email_manager:email_search'))

    try:
        raw_message_data = dao.get_raw_message(message_id)
        if not raw_message_data:
            messages.error(request, f"Could not retrieve full message data for ID: {message_id}.")
            return HttpResponseRedirect(reverse('email_manager:email_search'))

        email_obj = Email(raw_message_data, dao_instance=dao, source="gmail")

        eml_base_dir = os.path.join(settings.BASE_DIR, 'DL', 'email')

        eml_saved_successfully = email_obj.save_eml(base_download_dir=eml_base_dir)

        if not eml_saved_successfully:
            messages.warning(request,
                             f"Failed to save .eml file for message ID {message_id}. Email metadata will still be saved.")

        subject = email_obj.headers.get('Subject')
        sender = email_obj.headers.get('From')
        recipients_to = email_obj.headers.get('To')
        recipients_cc = email_obj.headers.get('Cc')
        recipients_bcc = email_obj.headers.get('Bcc')

        date_sent_str = email_obj.headers.get('Date')
        date_sent_dt = None
        if date_sent_str:
            try:
                date_sent_dt = parser.parse(date_sent_str)
            except ValueError:
                print(f"Warning: Could not parse date string '{date_sent_str}' for message {message_id}.")

        full_plain_text_body = email_obj.body_plain_text

        try:
            date_part_for_path = date_sent_dt.strftime('%Y%m%d') if date_sent_dt else "YYYYMMDD"
            sender_initial_for_path = email_obj._get_initial(sender)
            receiver_initial_for_path = email_obj._get_initial(recipients_to)
            subject_part_for_path = email_obj._sanitize_filename_part(subject, max_length=100)
            derived_filename = f"{date_part_for_path}_{sender_initial_for_path}_{receiver_initial_for_path}_{subject_part_for_path}.eml"
            full_eml_file_path = os.path.join(eml_base_dir, email_obj.source, derived_filename)
        except Exception as e:
            print(f"Warning: Could not derive EML file path for message {message_id}: {e}")
            full_eml_file_path = None

        linked_protagonist = None
        if protagonist_id:
            try:
                linked_protagonist = Protagonist.objects.get(pk=protagonist_id)
            except Protagonist.DoesNotExist:
                messages.warning(request,
                                 f"Selected protagonist (ID: {protagonist_id}) not found. Saving email without linked protagonist.")
        elif search_participant_email:
            try:
                protagonist_email_obj = ProtagonistEmail.objects.get(email_address__iexact=search_participant_email)
                linked_protagonist = protagonist_email_obj.protagonist
                messages.info(request, f"Linked email to existing protagonist: {linked_protagonist.get_full_name()}.")
            except ProtagonistEmail.DoesNotExist:
                name_parts = protagonist_search_name.split(maxsplit=1)
                first_name = name_parts[0] if name_parts else "Unknown"
                last_name = name_parts[1] if len(name_parts) > 1 else ""

                try:
                    linked_protagonist = Protagonist.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        role="Participant (Auto-created)"
                    )
                    ProtagonistEmail.objects.create(
                        protagonist=linked_protagonist,
                        email_address=search_participant_email,
                        description="Auto-added from Email Search"
                    )
                    messages.success(request,
                                     f"New protagonist '{linked_protagonist.get_full_name()}' created and linked!")
                except Exception as e:
                    messages.error(request, f"Failed to auto-create protagonist for {search_participant_email}: {e}")
                    linked_protagonist = None

        saved_email_instance, created = SavedEmail.objects.update_or_create(
            message_id=email_obj.id,
            defaults={
                'thread_id': email_obj.thread_id,
                'protagonist': linked_protagonist,
                'dao_source': email_obj.source,
                'subject': subject,
                'sender': sender,
                'recipients_to': recipients_to,
                'recipients_cc': recipients_cc,
                'recipients_bcc': recipients_bcc,
                'date_sent': date_sent_dt,
                'body_plain_text': full_plain_text_body,
                'eml_file_path': full_eml_file_path,
            }
        )

        if created:
            messages.success(request, f"Email '{subject}' (ID: {message_id}) saved successfully!")
        else:
            messages.info(request, f"Email '{subject}' (ID: {message_id}) already exists and was updated.")

        return HttpResponseRedirect(reverse('email_manager:email_detail', args=[saved_email_instance.pk]))

    except Exception as e:
        print(f"Error saving email {message_id}: {e}")
        messages.error(request, f"An error occurred while saving the email: {e}")
        return HttpResponseRedirect(reverse('email_manager:email_search'))


def email_detail_view(request, pk):
    saved_email = get_object_or_404(SavedEmail, pk=pk)
    email_thread = None
    thread_error_message = None

    if saved_email.dao_source == 'gmail' and saved_email.thread_id:
        token_path = os.path.join(settings.BASE_DIR, 'token.json')
        dao = GmailDAO(token_path=token_path)

        if dao.connect():
            try:
                raw_messages = dao.get_raw_thread_messages(saved_email.thread_id)
                # DEBUG: Check how many messages are being fetched
                print(f"DEBUG: Fetched {len(raw_messages) if raw_messages is not None else 'None'} messages for thread {saved_email.thread_id}")

                if raw_messages is not None:
                    email_thread = EmailThread(raw_messages, dao_instance=dao, source="gmail")
                else:
                    thread_error_message = "Could not retrieve the email thread due to a connection issue with Gmail."
                    if os.path.exists(token_path):
                        try:
                            os.remove(token_path)
                            messages.info(request, "Your Gmail authentication token may have been invalid. It has been reset. Please try again to re-authorize.")
                        except OSError as e:
                            messages.error(request, f"Critical Error: Could not delete the invalid token file at {token_path}. Please check file permissions. Error: {e}")
                    return HttpResponseRedirect(request.path)

            except ThreadNotFoundError:
                thread_error_message = "The email thread could not be found in Gmail. It might have been deleted."
            except Exception as e:
                thread_error_message = f"An unexpected error occurred: {e}"
                print(f"Unexpected error in email_detail_view: {e}")

        else:
            thread_error_message = "Could not connect to the Gmail API. Please ensure your credentials file is correctly configured in settings.py and complete the authentication process."

    context = {
        'email': saved_email,
        'email_thread': email_thread,
        'thread_error_message': thread_error_message,
    }
    return render(request, 'email_manager/email_detail.html', context)


def email_list_view(request):
    saved_emails = SavedEmail.objects.all().order_by('-date_sent')
    context = {
        'saved_emails': saved_emails
    }
    return render(request, 'email_manager/email_list.html', context)


@require_POST
def email_delete_view(request, pk):
    saved_email = get_object_or_404(SavedEmail, pk=pk)

    if saved_email.eml_file_path and os.path.exists(saved_email.eml_file_path):
        try:
            os.remove(saved_email.eml_file_path)
            messages.success(request, f"Associated EML file deleted: {saved_email.eml_file_path}")
        except OSError as e:
            messages.warning(request, f"Failed to delete EML file {saved_email.eml_file_path}: {e}")

    try:
        saved_email.delete()
        messages.success(request, f"Email '{saved_email.subject}' (ID: {saved_email.message_id}) deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting email '{saved_email.subject}': {e}")

    return HttpResponseRedirect(reverse('email_manager:email_list'))


def upload_eml_view(request):
    EXCLUDE_EMAIL = "louisphilippe.david@gmail.com"

    if request.method == 'POST':
        form = EmlUploadForm(request.POST, request.FILES)
        if form.is_valid():
            eml_file = form.cleaned_data['eml_file']
            linked_protagonist = form.cleaned_data['protagonist']

            eml_dao = EmlFileDAO()

            try:
                raw_eml_content = eml_file.read()
                msg = email.message_from_bytes(raw_eml_content)

                headers_list = []
                for k, v in msg.items():
                    headers_list.append({'name': k, 'value': v})

                body_plain_text = None
                if msg.is_multipart():
                    for part in msg.walk():
                        ctype = part.get_content_type()
                        cdispo = str(part.get('Content-Disposition'))

                        if ctype == 'text/plain' and 'attachment' not in cdispo:
                            try:
                                body_plain_text = part.get_payload(decode=True).decode(
                                    part.get_content_charset() or 'utf-8', errors='ignore')
                                break
                            except Exception as e:
                                print(f"Warning: Could not decode text/plain part: {e}")
                        elif ctype == 'text/html' and 'attachment' not in cdispo and not body_plain_text:
                            try:
                                body_plain_text = part.get_payload(decode=True).decode(
                                    part.get_content_charset() or 'utf-8', errors='ignore')
                            except Exception as e:
                                print(f"Warning: Could not decode text/html part: {e}")
                else:
                    ctype = msg.get_content_type()
                    if ctype in ['text/plain', 'text/html']:
                        try:
                            body_plain_text = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8',
                                                                                  errors='ignore')
                        except Exception as e:
                            print(f"Warning: Could not decode single-part body: {e}")

                generated_message_id = f"eml-{uuid.uuid4()}"

                eml_raw_message_data = {
                    'id': generated_message_id,
                    'threadId': generated_message_id,
                    'snippet': (body_plain_text[:100] + '...') if body_plain_text and len(
                        body_plain_text) > 100 else body_plain_text,
                    'payload': {
                        'headers': headers_list,
                        'body': {
                            'data': base64.urlsafe_b64encode(body_plain_text.encode('utf-8', errors='ignore')).decode(
                                'ascii')} if body_plain_text else {}
                    }
                }

                email_obj = Email(eml_raw_message_data, dao_instance=eml_dao, source="uploaded_eml")

                eml_message_id_header = email_obj.headers.get('Message-ID')
                if eml_message_id_header:
                    clean_eml_message_id = eml_message_id_header.strip('<>').replace('@', '_').replace('.', '_')
                    email_obj.id = f"eml-{clean_eml_message_id}"
                    email_obj.thread_id = f"eml-thread-{clean_eml_message_id}"

                participant_emails_in_eml = email_obj.get_all_participant_emails()

                found_protagonist_for_suggestion = None
                for eml_email in participant_emails_in_eml:
                    if eml_email.lower() == EXCLUDE_EMAIL.lower():
                        continue
                    try:
                        protagonist_email_obj = ProtagonistEmail.objects.get(email_address__iexact=eml_email)
                        found_protagonist_for_suggestion = protagonist_email_obj.protagonist
                        break
                    except ProtagonistEmail.DoesNotExist:
                        continue
                if not linked_protagonist and found_protagonist_for_suggestion:
                    linked_protagonist = found_protagonist_for_suggestion

                eml_base_dir = os.path.join(settings.BASE_DIR, 'DL', 'email')

                try:
                    date_sent_str = email_obj.headers.get('Date')
                    date_sent_dt = parser.parse(date_sent_str) if date_sent_str else None
                    date_part_for_path = date_sent_dt.strftime('%Y%m%d') if date_sent_dt else "YYYYMMDD"
                    sender_initial_for_path = email_obj._get_initial(email_obj.headers.get('From'))
                    receiver_initial_for_path = email_obj._get_initial(email_obj.headers.get('To'))
                    subject_part_for_path = email_obj._sanitize_filename_part(
                        email_obj.headers.get('Subject', 'No_Subject'), max_length=100)
                    eml_filename = f"{date_part_for_path}_{sender_initial_for_path}_{receiver_initial_for_path}_{subject_part_for_path}.eml"
                except Exception as e:
                    print(f"Warning: Could not derive EML filename for uploaded file: {e}")
                    eml_filename = f"uploaded_eml_{generated_message_id}.eml"

                target_eml_dir = os.path.join(eml_base_dir, email_obj.source)
                os.makedirs(target_eml_dir, exist_ok=True)
                full_eml_file_path = os.path.join(target_eml_dir, eml_filename)

                with open(full_eml_file_path, 'wb+') as destination:
                    destination.write(raw_eml_content)
                messages.success(request, f"EML file saved to: {full_eml_file_path}")

                subject = email_obj.headers.get('Subject')
                sender = email_obj.headers.get('From')
                recipients_to = email_obj.headers.get('To')
                recipients_cc = email_obj.headers.get('Cc')
                recipients_bcc = email_obj.headers.get('Bcc')
                date_sent_dt = date_sent_dt

                saved_email_instance, created = SavedEmail.objects.update_or_create(
                    message_id=email_obj.id,
                    defaults={
                        'thread_id': email_obj.thread_id,
                        'protagonist': linked_protagonist,
                        'dao_source': email_obj.source,
                        'subject': subject,
                        'sender': sender,
                        'recipients_to': recipients_to,
                        'recipients_cc': recipients_cc,
                        'recipients_bcc': recipients_bcc,
                        'date_sent': date_sent_dt,
                        'body_plain_text': email_obj.body_plain_text,
                        'eml_file_path': full_eml_file_path,
                    }
                )

                if created:
                    messages.success(request, f"EML Email '{subject}' saved successfully!")
                else:
                    messages.info(request, f"EML Email '{subject}' already exists and was updated.")

                redirect_url = reverse('email_manager:email_detail', args=[saved_email_instance.pk])
                if found_protagonist_for_suggestion:
                    redirect_url += f"?suggested_protagonist_id={found_protagonist_for_suggestion.pk}"
                return HttpResponseRedirect(redirect_url)

            except Exception as e:
                print(f"Error processing uploaded EML file: {e}")
                messages.error(request, f"An error occurred while processing the EML file: {e}")
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        initial_data = {}
        suggested_protagonist_id = request.GET.get('suggested_protagonist_id')
        if suggested_protagonist_id:
            try:
                Protagonist.objects.get(pk=suggested_protagonist_id)
                initial_data['protagonist'] = suggested_protagonist_id
                messages.info(request, "Protagonist suggested based on uploaded EML content.")
            except Protagonist.DoesNotExist:
                messages.warning(request, "Suggested protagonist not found.")

        form = EmlUploadForm(initial=initial_data)

    context = {'form': form}
    return render(request, 'email_manager/upload_eml.html', context)
