from django.urls import path
from . import views
from .views import produced_views
from .views import library_node_ajax # NEW: Import the new AJAX views for LibraryNode

app_name = 'document_manager'

urlpatterns = [
    # ... your existing URLs for reproduced documents ...
    path('list/', views.document_list_view, name='document_list'),
    path('document/<int:pk>/', views.document_detail_view, name='document_detail'),
    path('clean/<int:pk>/', views.clean_detail_view, name='clean_detail'),
    path('interactive/<int:pk>/', views.interactive_detail_view, name='interactive_detail'),
    path('perjury-elements/', views.PerjuryElementListView.as_view(), name='perjury_element_list'),

    # --- NEW: URLs for Manually Produced Documents ---
    path('produced/', produced_views.ProducedDocumentListView.as_view(), name='produced_list'),
    path('produced/create/', produced_views.ProducedDocumentCreateView.as_view(), name='produced_create'),
    path('produced/editor/<int:pk>/', produced_views.ProducedDocumentEditorView.as_view(), name='produced_editor'),
    
    # --- NEW: AJAX Endpoints for the Editor ---
    path('ajax/produced/add_node/<int:node_pk>/', produced_views.ajax_add_node, name='ajax_add_node'),
    path('ajax/produced/edit_node/<int:node_pk>/', produced_views.ajax_edit_node, name='ajax_edit_node'),
    path('ajax/produced/delete_node/<int:node_pk>/', produced_views.ajax_delete_node, name='ajax_delete_node'),

    # --- NEW: AJAX Endpoints for LibraryNode Management ---
    path('ajax/library_node/<int:document_pk>/add/', library_node_ajax.add_library_node_ajax, name='add_library_node_ajax'),
]
