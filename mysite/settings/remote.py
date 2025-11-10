from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Add your remote database settings, allowed hosts, etc. here
ALLOWED_HOSTS = [
    'court-app-141670575225.us-central1.run.app',
    'localhost',
    '127.0.0.1',
]


# --- Google Cloud Storage Settings ---

# The name of the GCS bucket you created
GS_BUCKET_NAME = os.getenv('GS_BUCKET_NAME')

# Use GCS for default file storage (i.e., for ImageField, FileField)
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

# Use GCS for static files
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

# --- Database Settings (from environment variables) ---

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Check if running on Google Cloud Run and adjust the database HOST
# The value of this env var is set in the deploy.yml file
if os.getenv('DJANGO_ENV') == 'remote':
    # When connecting via a Unix socket, HOST is the socket path and PORT must be empty.
    DATABASES['default']['HOST'] = f"/cloudsql/{os.getenv('DB_INSTANCE_CONNECTION_NAME')}"
    DATABASES['default']['PORT'] = ''
