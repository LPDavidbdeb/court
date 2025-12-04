import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.db.models import Q
from django.conf import settings
from email_manager.models import Email

class Command(BaseCommand):
    help = 'Migrates local EML files to the new FileField for cloud storage.'

    def handle(self, *args, **options):
        # 1. ROBUST STORAGE CHECK (Fixes the crash)
        is_google_storage = False
        if hasattr(settings, 'STORAGES'):
            backend = settings.STORAGES.get('default', {}).get('BACKEND', '').lower()
            if 'google' in backend or 'gcloud' in backend:
                is_google_storage = True
        elif hasattr(settings, 'DEFAULT_FILE_STORAGE'):
             if 'google' in settings.DEFAULT_FILE_STORAGE.lower():
                 is_google_storage = True

        if not is_google_storage:
            self.stdout.write(self.style.ERROR(
                "ERROR: Google Cloud Storage is not active.\n"
                "Run with: python manage.py migrate_emails_to_cloud --settings=mysite.settings.remote"
            ))
            return

        # 2. ROBUST QUERY (Fixes the "Found 0 emails" issue)
        # Finds emails where the new field is NULL *OR* Empty, but the old field has data.
        emails = Email.objects.filter(
            Q(eml_file__isnull=True) | Q(eml_file=''),
            eml_file_path__isnull=False
        ).exclude(eml_file_path='')

        count = emails.count()
        self.stdout.write(f"Found {count} emails to migrate.")

        for i, email_obj in enumerate(emails):
            local_path = email_obj.eml_file_path

            if os.path.exists(local_path):
                try:
                    with open(local_path, 'rb') as f:
                        djangofile = File(f)
                        filename = os.path.basename(local_path)
                        
                        # Saving to the FileField triggers the upload to Cloud Storage
                        email_obj.eml_file.save(filename, djangofile, save=True)
                        
                        self.stdout.write(self.style.SUCCESS(f"[{i+1}/{count}] Uploaded: {filename}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error on {local_path}: {e}"))
            else:
                self.stdout.write(self.style.WARNING(f"File not found locally: {local_path}"))
