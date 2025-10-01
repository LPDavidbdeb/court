# your_project_root/events/urls.py

from django.urls import path
from . import views

# The app is now conceptually 'events'
app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='list'),
    path('create/', views.EventCreateView.as_view(), name='create'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.EventUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='delete'),

    # The URL for the inline explanation update
    path('api/explanation/<int:pk>/update/', views.ExplanationUpdateAPIView.as_view(), name='ajax_update_explanation'),
]
