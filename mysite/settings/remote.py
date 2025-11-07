from .base import *

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
