from django.urls import path
# This is for the new DownloadEmlView
from . import download_views
# This is for the AddQuoteView
from . import quote_views
# This is for the original, existing views from the sub-package
from .views import email_namager_view

app_name = 'email_manager'

urlpatterns = [
    # Original, working URLs
    path('search/', email_namager_view.email_search_view, name='email_search'),
    path('save_thread/', email_namager_view.save_thread_view, name='save_thread'),
    path('email/<int:pk>/', email_namager_view.email_detail_view, name='email_detail'),
    path('emails/', email_namager_view.email_list_view, name='email_list'),
    path('email/<int:pk>/delete/', email_namager_view.email_delete_view, name='email_delete'),
    path('upload_eml/', email_namager_view.upload_eml_view, name='upload_eml'),

    # --- Quote Management ---
    path('add-quote/<int:email_pk>/', quote_views.AddQuoteView.as_view(), name='add_quote'),

    # --- EML Download ---
    path('download-eml/<int:pk>/', download_views.DownloadEmlView.as_view(), name='download_eml'),
]
