# your_project_root/photos/urls.py

from django.urls import path
from . import views

app_name = 'photos' # IMPORTANT: Namespace for your photo app's URLs

urlpatterns = [
    path('', views.PhotoListView.as_view(), name='list'),
    path('create/', views.PhotoCreateView.as_view(), name='create'),
    path('<int:pk>/', views.PhotoDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.PhotoUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.PhotoDeleteView.as_view(), name='delete'),
]