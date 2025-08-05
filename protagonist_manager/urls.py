from django.urls import path
from .views.model_views import (
    ProtagonistListView,
    ProtagonistDetailView,
    ProtagonistCreateView,
    ProtagonistUpdateView,
    ProtagonistDeleteView,
    ProtagonistEmailCreateView,
    ProtagonistEmailDeleteView,
)

from .views.search_protagonist_ajax import search_protagonists_ajax
app_name = 'protagonist_manager' # Namespace for URLs

urlpatterns = [
    path('', ProtagonistListView.as_view(), name='protagonist_list'), # List all protagonists
    path('add/', ProtagonistCreateView.as_view(), name='protagonist_add'), # Add new protagonist
    path('<int:pk>/', ProtagonistDetailView.as_view(), name='protagonist_detail'), # View protagonist details
    path('<int:pk>/edit/', ProtagonistUpdateView.as_view(), name='protagonist_edit'), # Edit protagonist
    path('<int:pk>/delete/', ProtagonistDeleteView.as_view(), name='protagonist_delete'), # Delete protagonist

    path('<int:pk>/emails/add/', ProtagonistEmailCreateView.as_view(), name='protagonist_email_add'), # Add email to protagonist
    path('<int:protagonist_pk>/emails/<int:pk>/delete/', ProtagonistEmailDeleteView.as_view(), name='protagonist_email_delete'),

#   New AJAX endpoint
    path('ajax/search_protagonists/', search_protagonists_ajax, name='search_protagonists_ajax'),
]
