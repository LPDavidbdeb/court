from django.urls import path
from . import views

app_name = 'document_manager'

urlpatterns = [
    # URL for the new upload feature
    path('upload/', views.upload_structured_document_view, name='upload_structured_document'),

    # URL for the new document list page
    path('list/', views.document_list_view, name='document_list'),

    # URL for the standard document detail page
    path('document/<int:pk>/', views.document_node_detail_view, name='documentnode_detail'),

    # URL for the clean, formatted document view
    path('clean/<int:pk>/', views.clean_detail_view, name='clean_detail_view'),

    # NEW: URL for the interactive annotation view
    path('interactive/<int:pk>/', views.interactive_detail_view, name='interactive_detail_view'),

    # NEW: URL for the background AJAX update view
    path('ajax/update_truth/', views.update_node_truth_view, name='update_node_truth'),

    # URL for the library reset feature
    path('reset/', views.reset_library_view, name='reset_library'),

    # --- URLs from your original crud_views.py ---
    path('library/add/', views.LibraryCreateView.as_view(), name='library_add'),
    path('document/add/', views.DocumentCreateView.as_view(), name='document_add'),
    path('node/<int:parent_pk>/add/', views.DocumentNodeCreateView.as_view(), name='documentnode_add'),
    path('node/<int:pk>/update/', views.DocumentNodeUpdateView.as_view(), name='documentnode_update'),
    path('node/<int:pk>/delete/', views.DocumentNodeDeleteView.as_view(), name='documentnode_delete'),
    path('rebuild/', views.RebuildTreeView.as_view(), name='rebuild_tree'),
    path('ajax/add_node/', views.AddNodeModalView.as_view(), name='ajax_add_node'),

    # --- Perjury Elements ---
    path('perjury-elements/', views.PerjuryElementWithTrameListView.as_view(), name='perjury_element_list'),
]
