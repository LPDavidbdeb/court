from django.urls import path
from .views import email_namager_view

app_name = 'email_manager'

urlpatterns = [
    path('search/', email_namager_view.email_search_view, name='email_search'),
    # UPDATED: This now saves the entire thread, not just one email.
    path('save_thread/', email_namager_view.save_thread_view, name='save_thread'),
    path('email/<int:pk>/', email_namager_view.email_detail_view, name='email_detail'),
    path('emails/', email_namager_view.email_list_view, name='email_list'),
    # FIXED: Removed leading slash from path.
    path('email/<int:pk>/delete/', email_namager_view.email_delete_view, name='email_delete'),
    path('upload_eml/', email_namager_view.upload_eml_view, name='upload_eml'),
]
