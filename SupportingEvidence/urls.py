# your_project_root/evidence/urls.py

from django.urls import path
from . import views

app_name = 'SupportingEvidence'  # CORRECTED: To match the namespace in the project's urls.py

urlpatterns = [
    path('', views.SupportingEvidenceListView.as_view(), name='list'),
    path('create/', views.SupportingEvidenceCreateView.as_view(), name='create'),
    path('<int:pk>/', views.SupportingEvidenceDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.SupportingEvidenceUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.SupportingEvidenceDeleteView.as_view(), name='delete'),

    # The URL for the inline explanation update
    path('api/explanation/<int:pk>/update/', views.ExplanationUpdateAPIView.as_view(), name='ajax_update_explanation'),
]
