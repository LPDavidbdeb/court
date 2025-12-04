import os
from django.core.management.base import BaseCommand
from django.core.files import File
from email_manager.models import Email
from django.conf import settings


class Command(BaseCommand):
    help = 'Migrates local EML files to the new FileField for cloud storage.'

    def handle(self, *args, **options):
        if 'google' not in settings.DEFAULT_FILE_STORAGE.lower():
            self.stdout.write(self.style.ERROR("Enable Google Cloud Storage in settings first!"))
            return

        # Find emails that have a local path but no cloud file yet
        emails = Email.objects.filter(eml_file='', eml_file_path__isnull=False)
        self.stdout.write(f"Found {emails.count()} emails to migrate.")

        for email_obj in emails:
            local_path = email_obj.eml_file_path

            if os.path.exists(local_path):
                try:
                    with open(local_path, 'rb') as f:
                        # Create a Django File object
                        djangofile = File(f)

                        # Determine a filename (e.g., "threadID_messageID.eml")
                        filename = os.path.basename(local_path)

                        # Save to the new field. This triggers the upload to GCS.
                        email_obj.eml_file.save(filename, djangofile, save=True)

                        self.stdout.write(self.style.SUCCESS(f"Uploaded: {filename}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error on {local_path}: {e}"))
            else:
                self.stdout.write(self.style.WARNING(f"File not found locally: {local_path}"))