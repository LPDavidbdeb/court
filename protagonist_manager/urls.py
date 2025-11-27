from django.urls import path
from .views import model_views, ProtagonistCreateWithEmailsView, ajax_views

app_name = 'protagonist_manager'

urlpatterns = [
    # Protagonist list and detail
    path('', model_views.ProtagonistListView.as_view(), name='protagonist_list'),
    path('<int:pk>/', model_views.ProtagonistDetailView.as_view(), name='protagonist_detail'),

    # Protagonist CRUD
    path('create/', ProtagonistCreateWithEmailsView.as_view(), name='protagonist_create'),
    path('<int:pk>/update/', model_views.ProtagonistUpdateView.as_view(), name='protagonist_update'),
    path('<int:pk>/delete/', model_views.ProtagonistDeleteView.as_view(), name='protagonist_delete'),

    # ProtagonistEmail CRUD
    path('<int:protagonist_pk>/add-email/', model_views.ProtagonistEmailCreateView.as_view(), name='add_email'),
    path('email/<int:pk>/update/', model_views.ProtagonistEmailUpdateView.as_view(), name='update_email'),
    path('email/<int:pk>/delete/', model_views.ProtagonistEmailDeleteView.as_view(), name='delete_email'),

    # AJAX views
    path('ajax/search/', ajax_views.search_protagonists_ajax, name='search_protagonists_ajax'),
    path('ajax/update-role/', ajax_views.update_protagonist_role_ajax, name='update_protagonist_role'),
    
    # Merge view
    path('merge/', model_views.MergeProtagonistView.as_view(), name='merge_protagonist'),
]
