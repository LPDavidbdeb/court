# This file makes the views directory a Python package and exposes the views from submodules.

# Import views from the original CRUD file
from .crud_views import (
    LibraryCreateView,
    DocumentCreateView,
    DocumentNodeCreateView,
    DocumentNodeListView,
    DocumentNodeDetailView,
    DocumentNodeUpdateView,
    DocumentNodeDeleteView,
    RebuildTreeView,
    AddNodeModalView,
)

# Import views from the upload file
from .upload_views import (
    document_list_view,
    document_node_detail_view,
    upload_structured_document_view,
    reset_library_view,
    clean_detail_view,
    interactive_detail_view, # ADDED
)

# Import views from the new AJAX file
from .ajax_views import (
    update_node_truth_view, # ADDED
)
