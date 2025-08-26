# your_project_root/photos/models.py

from django.db import models
from django.urls import reverse


class Photo(models.Model):
    file = models.ImageField(upload_to='photos/', blank=True, null=True, help_text="The actual image file.")

    # Common File System Metadata
    file_path = models.CharField(max_length=500, unique=True, help_text="Absolute path to the image file.")
    file_name = models.CharField(max_length=255)
    folder_path = models.CharField(max_length=500)
    file_size = models.BigIntegerField(null=True, blank=True)
    last_modified = models.DateTimeField(null=True, blank=True)
    created_on_disk = models.DateTimeField(null=True, blank=True)

    # Basic Image Dimensions & Format
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    image_format = models.CharField(max_length=10, null=True, blank=True)
    image_mode = models.CharField(max_length=20, null=True, blank=True)

    # EXIF/Camera Specific Metadata
    make = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    datetime_original = models.DateTimeField(null=True, blank=True)
    iso_speed = models.IntegerField(null=True, blank=True)
    artist = models.CharField(max_length=255, null=True, blank=True)
    exposure_time = models.CharField(max_length=50, null=True, blank=True) # Can be fraction, so CharField
    f_number = models.FloatField(null=True, blank=True)
    focal_length = models.FloatField(null=True, blank=True)

    # Lens Model
    lens_model = models.CharField(max_length=255, null=True, blank=True)

    # Raw Image Specific Metadata (for CR2, etc.)
    raw_width = models.IntegerField(null=True, blank=True)
    raw_height = models.IntegerField(null=True, blank=True)
    color_depth = models.IntegerField(null=True, blank=True)
    num_colors = models.IntegerField(null=True, blank=True)
    cfa_pattern = models.CharField(max_length=50, null=True, blank=True) # Stored as string representation of list

    # GPS Data
    gps_latitude = models.FloatField(null=True, blank=True)
    gps_longitude = models.FloatField(null=True, blank=True)
    gps_altitude = models.FloatField(null=True, blank=True)
    gps_timestamp = models.DateTimeField(null=True, blank=True)

    # All metadata as JSON (for completeness)
    all_metadata_json = models.JSONField(default=dict, blank=True, null=True)

    # Date extracted from folder name
    date_folder = models.DateField(null=True, blank=True, help_text="Date extracted from the folder name (YYYY-MM-DD)")

    class Meta:
        ordering = ['datetime_original']
        verbose_name = "Photo"
        verbose_name_plural = "Photos"

    def __str__(self):
        return f"{self.file_name} ({self.datetime_original.strftime('%Y-%m-%d') if self.datetime_original else 'No Date'})"

    def get_absolute_url(self):
        # FIXED: Use the correct app_name ('photos') and URL name ('detail')
        return reverse('photos:detail', kwargs={'pk': self.pk})
