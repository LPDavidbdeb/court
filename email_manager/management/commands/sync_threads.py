from django.core.management.base import BaseCommand, CommandError
from email_manager.models import Email, EmailThread
from DAL.gmailDAO import GmailDAO
from DAL.EmailFileDAO import EmlFileDAO
from dateutil import parser

class Command(BaseCommand):
    help = 'Syncs saved email threads with Gmail to fetch any missing messages.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--thread_pk',
            type=int,
            help='Specify the database PK of a single EmailThread to sync.',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting email thread synchronization..."))

        thread_pk = options['thread_pk']
        threads_to_sync = []

        if thread_pk:
            try:
                thread = EmailThread.objects.get(pk=thread_pk)
                # Check if any email in the thread is from gmail
                if not thread.emails.filter(dao_source='gmail').exists():
                    raise CommandError(f"Thread PK {thread_pk} is not a Gmail thread and cannot be synced.")
                threads_to_sync.append(thread)
                self.stdout.write(f"Targeting single thread: '{thread.subject}' (PK: {thread.pk})")
            except EmailThread.DoesNotExist:
                raise CommandError(f"EmailThread with PK {thread_pk} does not exist.")
        else:
            threads_to_sync = EmailThread.objects.filter(emails__dao_source='gmail').distinct()
            self.stdout.write(f"Found {threads_to_sync.count()} Gmail threads to sync.")

        if not threads_to_sync.count():
            self.stdout.write(self.style.WARNING("No Gmail threads found to sync."))
            return

        dao = GmailDAO()
        if not dao.connect():
            raise CommandError("Could not connect to Gmail API. Please check credentials.")

        # FIXED: Create an instance of the EmlFileDAO to use for parsing.
        eml_parser = EmlFileDAO()
        total_synced_count = 0

        for thread in threads_to_sync:
            self.stdout.write(f"---\nChecking thread: '{thread.subject}' (Thread ID: {thread.thread_id})")

            try:
                remote_message_ids = {msg['id'] for msg in dao.get_raw_thread_messages(thread.thread_id)}
                local_message_ids = set(thread.emails.values_list('message_id', flat=True))
                missing_ids = remote_message_ids - local_message_ids

                if not missing_ids:
                    self.stdout.write(self.style.SUCCESS("Thread is already up to date."))
                    continue

                self.stdout.write(self.style.WARNING(f"Found {len(missing_ids)} missing messages. Fetching them now..."))

                for msg_id in missing_ids:
                    raw_message = dao.get_raw_message(msg_id)
                    if not raw_message:
                        self.stderr.write(self.style.ERROR(f"Could not fetch message ID {msg_id}. Skipping."))
                        continue

                    # FIXED: Call the parsing method on the instance.
                    email_data = eml_parser.parse_raw_message_data(raw_message)
                    date_sent_dt = parser.parse(email_data['headers'].get('Date')) if email_data['headers'].get('Date') else None

                    Email.objects.create(
                        thread=thread,
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
                    self.stdout.write(f"  - Saved new message: '{email_data['headers'].get('Subject')}'")
                    total_synced_count += 1

            except Exception as e:
                self.stderr.write(self.style.ERROR(f"An error occurred while syncing thread {thread.thread_id}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"\nSynchronization complete. Fetched {total_synced_count} new messages in total."))
