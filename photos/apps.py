from django.apps import AppConfig


class PhotosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'photos'

    def ready(self):
        # Register the HEIF/HEIC opener so Pillow (and therefore Django's
        # ImageField validation and PhotoProcessingService) can decode .heic/.heif
        # uploads. Monkey-patches PIL process-wide; safe to call once at startup.
        from pillow_heif import register_heif_opener
        register_heif_opener()
