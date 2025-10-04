from django.core.management.base import BaseCommand
from django.db import transaction
from photos.models import Photo
from events.models import Event  # MODIFIED
from datetime import timedelta

class Command(BaseCommand):
    help = 'Deletes all existing Events and re-clusters photos into new Event objects.' # MODIFIED

    @transaction.atomic
    def handle(self, *args, **options):
        # 1. Perform a "Clean Install" by deleting all existing events
        self.stdout.write(self.style.WARNING("Deleting all existing Event objects...")) # MODIFIED
        count, _ = Event.objects.all().delete() # MODIFIED
        self.stdout.write(self.style.SUCCESS(f"Successfully deleted {count} old Event objects.")) # MODIFIED

        # 2. Re-cluster photos
        self.stdout.write("Starting photo clustering to create new Events...") # MODIFIED
        photos_to_cluster = Photo.objects.filter(datetime_original__isnull=False).order_by('datetime_original')

        if not photos_to_cluster:
            self.stdout.write(self.style.SUCCESS("No photos with dates found to cluster."))
            return

        event_break_threshold = timedelta(hours=2)
        current_cluster = []
        
        for photo in photos_to_cluster:
            if not current_cluster:
                current_cluster.append(photo)
                continue

            last_photo_time = current_cluster[-1].datetime_original
            current_photo_time = photo.datetime_original

            if (current_photo_time - last_photo_time) > event_break_threshold:
                self.create_event_from_cluster(current_cluster) # MODIFIED
                current_cluster = [photo]
            else:
                current_cluster.append(photo)
        
        if current_cluster:
            self.create_event_from_cluster(current_cluster) # MODIFIED

        self.stdout.write(self.style.SUCCESS("Photo clustering complete."))

    def create_event_from_cluster(self, photos): # MODIFIED
        if not photos:
            return

        photos.sort(key=lambda p: p.datetime_original)
        start_time = photos[0].datetime_original
        end_time = photos[-1].datetime_original

        # Create the explanation text in the desired format
        explanation_template = (
            f"On {start_time.strftime('%Y-%m-%d')} between "
            f"{start_time.strftime('%H:%M')} and {end_time.strftime('%H:%M')}: "
        )
        
        # Create the new event object with the correct data
        event = Event.objects.create( # MODIFIED
            date=start_time.date(),
            explanation=explanation_template
        )
        
        event.linked_photos.add(*photos)
        
        self.stdout.write(f"  Created Event for cluster of {len(photos)} photos from {start_time.date()}.") # MODIFIED
