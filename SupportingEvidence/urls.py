# your_project_root/evidence/urls.py

from django.urls import path
from . import views

# CORRECTED: Changed the app_name to match the templates
app_name = 'SupportingEvidence'

urlpatterns = [
    path('', views.SupportingEvidenceListView.as_view(), name='list'),
    path('create/', views.SupportingEvidenceCreateView.as_view(), name='create'),
    path('<int:pk>/', views.SupportingEvidenceDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.SupportingEvidenceUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.SupportingEvidenceDeleteView.as_view(), name='delete'),

    path('api/update_explanation/<int:pk>/', views.ExplanationUpdateAPIView.as_view(), name='ajax_update_explanation'),
]
