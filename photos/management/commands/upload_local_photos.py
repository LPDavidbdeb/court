# photos/management/commands/upload_local_photos.py

import os
from django.core.management.base import BaseCommand
from django.core.files import File
from photos.models import Photo
from django.conf import settings

class Command(BaseCommand):
    help = '''Uploads local photo files to Google Cloud Storage based on the file_path stored in the database.'''

    def handle(self, *args, **options):
        # Ensure this command is only run in a production-like environment
        # where django-storages is configured to use GCS.
        if not settings.DEFAULT_FILE_STORAGE == 'storages.backends.gcloud.GoogleCloudStorage':
            self.stdout.write(self.style.ERROR(
                "This command should only be run in an environment configured for Google Cloud Storage."
            ))
            return

        self.stdout.write("Starting upload of local photos to Google Cloud Storage...")

        photos_to_upload = Photo.objects.filter(file__isnull=True).order_by('pk')
        total_photos = photos_to_upload.count()
        self.stdout.write(f"Found {total_photos} photos to upload.")

        for i, photo in enumerate(photos_to_upload):
            # The full path to the local file is stored in the 'file_path' field
            local_file_path = photo.file_path

            if not os.path.exists(local_file_path):
                self.stdout.write(self.style.WARNING(
                    f"[{i + 1}/{total_photos}] SKIPPING: File not found for Photo {photo.pk}: {local_file_path}"
                ))
                continue

            try:
                with open(local_file_path, 'rb') as f:
                    # We use the file_name for the destination filename in GCS
                    django_file = File(f)
                    # When we save the file field, django-storages automatically handles the upload to GCS.
                    # The `get_photo_upload_path` function in the model determines the destination path.
                    photo.file.save(photo.file_name, django_file, save=True)

                self.stdout.write(self.style.SUCCESS(
                    f"[{i+1}/{total_photos}] SUCCESS: Uploaded Photo {photo.pk} to {photo.file.name}"
                ))

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"[{i + 1}/{total_photos}] FAILED: Could not upload Photo {photo.pk}. Error: {e}"
                ))

        self.stdout.write(self.style.SUCCESS("Photo upload process complete."))

        # This will find and stop any running cloud-sql-proxy processes
