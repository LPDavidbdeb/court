from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Add your remote database settings, allowed hosts, etc. here
# For example:
# ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# --- Google Cloud Storage Settings ---

# The name of the GCS bucket you created
GS_BUCKET_NAME = os.getenv('GS_BUCKET_NAME')

# Use GCS for default file storage (i.e., for ImageField, FileField)
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

# Use GCS for static files
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

# --- Database Settings for Cloud Run ---

# This configuration is for connecting to Cloud SQL from Cloud Run
# It uses a Unix socket for a secure and efficient connection.
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'), # Should be 'django.db.backends.postgresql'
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        # The HOST should be the path to the Cloud SQL socket.
        # This is typically /cloudsql/<PROJECT_ID>:<REGION>:<INSTANCE_NAME>
        'HOST': f"/cloudsql/{os.getenv('GCP_PROJECT_ID')}:{os.getenv('GCP_REGION')}:{os.getenv('DB_INSTANCE_NAME')}",
        'PORT': os.getenv('DB_PORT'), # Usually 5432 for PostgreSQL
    }
}
