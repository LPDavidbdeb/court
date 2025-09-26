# your_project_root/photos/urls.py

from django.urls import path
from . import views

app_name = 'photos'

urlpatterns = [
    path('', views.PhotoListView.as_view(), name='list'),
    path('create/', views.PhotoCreateView.as_view(), name='create'),
    path('processing/', views.photo_processing_view, name='processing'),
    path('bulk_delete/', views.bulk_delete_photos, name='bulk_delete'),

    # New URL for interactive import
    path('import_single_photo/', views.import_single_photo_view, name='import_single_photo'),

    # NEW: Timeline URLs
    path('timeline/', views.timeline_entry_view, name='timeline_entry'),
    path('timeline/<int:year>/<int:month>/<int:day>/', views.DayTimelineView.as_view(), name='day_timeline'),

    # Standard Detail, Update, Delete
    path('<int:pk>/', views.PhotoDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.PhotoUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.PhotoDeleteView.as_view(), name='delete'),
]
