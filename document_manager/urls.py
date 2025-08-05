from django.urls import path
from .views.crud_views import (
    DocumentNodeListView,
    DocumentNodeDetailView,
    DocumentNodeCreateView,
    DocumentNodeUpdateView,
    DocumentNodeDeleteView,
    LibraryCreateView,
    DocumentCreateView,
    RebuildTreeView,
    AddNodeModalView
)
app_name = 'document_manager'

urlpatterns = [
    path('library/add/', LibraryCreateView.as_view(), name='library_add'),
    path('document/add/', DocumentCreateView.as_view(), name='document_add'),
    path('', DocumentNodeListView.as_view(), name='document_list'),
    path('node/<int:pk>/', DocumentNodeDetailView.as_view(), name='documentnode_detail'),
    path('node/<int:pk>/edit/', DocumentNodeUpdateView.as_view(), name='documentnode_edit'),
    path('node/<int:pk>/delete/', DocumentNodeDeleteView.as_view(), name='documentnode_delete'),

    path('rebuild_tree/', RebuildTreeView.as_view(), name='rebuild_tree'),

    # URL for adding a generic child node (e.g., section, paragraph) to a specific parent
    # This URL is used for full-page redirects if not using the modal.
    path('node/<int:parent_pk>/add_child/', DocumentNodeCreateView.as_view(), name='documentnode_add_child'),

    # NEW: URL for handling the modal form submission (AJAX)
    path('add_node_modal/', AddNodeModalView.as_view(), name='add_node_modal'),
]

