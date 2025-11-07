# your_project_root/mysite/urls.py

from django.contrib import admin
from django.urls import path, include

# --- NEW IMPORTS for serving static and media files in development ---
from django.conf import settings
from django.conf.urls.static import static
# --- END NEW IMPORTS ---

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), # django-allauth URLs
    path('tinymce/', include('tinymce.urls')),
    path('events/', include('events.urls')), 
    path('arguments/', include('argument_manager.urls')), # ADDED
    path('photos/', include('photos.urls')),
    path('emails/', include('email_manager.urls')),
    path('protagonists/', include('protagonist_manager.urls')),
    path('documents/', include('document_manager.urls')),
    path('pdfs/', include('pdf_manager.urls')),
    path('', include('core.urls')), # For the home_view we discussed earlier
]

# --- IMPORTANT: ONLY FOR DEVELOPMENT ---
# This block tells Django's development server how to serve static and media files.
# In a production environment, a dedicated web server (like Nginx or Apache)
# handles serving these files directly, bypassing Django for performance and security.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
