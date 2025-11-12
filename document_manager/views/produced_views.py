from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from ..models import Document, Statement, LibraryNode, DocumentSource
from ..forms.manual_forms import ProducedDocumentForm, NodeForm, LibraryNodeCreateForm
from django.contrib.contenttypes.models import ContentType # NEW: Import ContentType
import json

class ProducedDocumentListView(ListView):
    """Lists only the manually 'Produced' documents."""
    model = Document
    template_name = 'document_manager/produced/list.html'
    context_object_name = 'documents'

    def get_queryset(self):
        return Document.objects.filter(source_type=DocumentSource.PRODUCED).order_by('-created_at')

class ProducedDocumentCreateView(CreateView):
    """View to create a new, empty 'Produced' document."""
    model = Document
    form_class = ProducedDocumentForm
    template_name = 'document_manager/produced/form.html'

    @transaction.atomic
    def form_valid(self, form):
        self.object = form.save()
        
        root_statement = Statement.objects.create(
            text=f"Root node for {self.object.title}",
            is_user_created=True # Mark the initial root statement as user-created
        )
        
        # REFACTORED: Use content_object for the root node
        LibraryNode.add_root(
            document=self.object,
            content_object=root_statement, # Use the generic foreign key
            item=self.object.title
        )
        
        return redirect('document_manager:produced_editor', pk=self.object.pk)

class ProducedDocumentEditorView(DetailView):
    """The main editor interface for building a document's tree."""
    model = Document
    template_name = 'document_manager/produced/editor.html'
    context_object_name = 'document'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # --- FIX: Only pass root nodes to the template for initial iteration ---
        # The _node.html template will handle recursive rendering of children.
        context['nodes'] = LibraryNode.objects.filter(
            document=self.object, 
            depth=1
        ).prefetch_related('content_object').order_by('path')
        
        context['modal_form'] = NodeForm()
        context['library_node_create_form'] = LibraryNodeCreateForm()
        return context

# --- AJAX Views for Tree Manipulation (REFACTORED) ---

@transaction.atomic
def ajax_add_node(request, node_pk):
    """AJAX view to add a new child node."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

    try:
        parent_node = get_object_or_404(LibraryNode, pk=node_pk)
        form = NodeForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            
            new_statement = Statement.objects.create(text=data['text'], is_user_created=True) # NEW: Mark as user-created
            
            # REFACTORED: Use content_object
            new_node = parent_node.add_child(
                document=parent_node.document,
                content_object=new_statement, # Use the generic foreign key
                item=data['item']
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Node added successfully',
                'new_node': {'id': new_node.id, 'item': new_node.item, 'text': new_statement.text}
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'Form is invalid', 'errors': form.errors.as_json()}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@transaction.atomic
def ajax_edit_node(request, node_pk):
    """AJAX view to edit an existing node's item and statement text."""
    # REFACTORED: Use select_related('content_type') for GFK
    node_to_edit = get_object_or_404(LibraryNode.objects.select_related('content_type'), pk=node_pk)
    
    if request.method == 'POST':
        form = NodeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            node_to_edit.item = data['item']
            node_to_edit.save()
            
            # REFACTORED: Update associated content_object
            if node_to_edit.content_object and hasattr(node_to_edit.content_object, 'text'):
                node_to_edit.content_object.text = data['text']
                node_to_edit.content_object.save()
            else:
                # This case is unlikely if all nodes are Statements, but it's safe to handle
                # If a node previously had no content_object or a non-Statement, and now text is provided
                new_statement = Statement.objects.create(text=data['text'], is_user_created=True) # NEW: Mark as user-created
                node_to_edit.content_object = new_statement
                node_to_edit.save()
                
            return JsonResponse({'status': 'success', 'message': 'Node updated.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Form is invalid', 'errors': form.errors.as_json()}, status=400)
    
    # GET request: Return current data to populate the modal
    text_content = ''
    if node_to_edit.content_object and hasattr(node_to_edit.content_object, 'text'):
        text_content = node_to_edit.content_object.text

    data = {
        'item': node_to_edit.item,
        'text': text_content
    }
    return JsonResponse(data)


@transaction.atomic
def ajax_delete_node(request, node_pk):
    """AJAX view to delete a node (and all its children) with nuanced content_object deletion."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

    try:
        node_to_delete = get_object_or_404(LibraryNode, pk=node_pk)
        
        if node_to_delete.is_root():
            return JsonResponse({'status': 'error', 'message': 'Cannot delete the root node.'}, status=400)
            
        # Get all nodes that will be deleted (the node itself and its descendants)
        nodes_to_be_deleted = [node_to_delete] + list(node_to_delete.get_descendants())
        
        # Collect all unique content_objects associated with these nodes
        content_objects_to_consider = {} # { (content_type_id, object_id): content_object_instance }
        for node in nodes_to_be_deleted:
            if node.content_object:
                key = (node.content_type_id, node.object_id)
                if key not in content_objects_to_consider:
                    content_objects_to_consider[key] = node.content_object

        # Perform the deletion of LibraryNodes first
        node_to_delete.delete() # This deletes the node and all its descendants

        # Now, iterate through the collected content_objects and apply nuanced deletion
        statement_content_type = ContentType.objects.get_for_model(Statement)

        for (ct_id, obj_id), content_obj in content_objects_to_consider.items():
            if ct_id == statement_content_type.id and isinstance(content_obj, Statement):
                if content_obj.is_user_created:
                    # Check if this user-created Statement is still referenced by any *other* LibraryNode
                    # that was NOT part of the current deletion operation.
                    # We need to exclude the nodes that were just deleted.
                    # Since node_to_delete.delete() already happened, we just check for *any* remaining references.
                    remaining_references = LibraryNode.objects.filter(
                        content_type=statement_content_type,
                        object_id=content_obj.pk
                    ).exists()

                    if not remaining_references:
                        content_obj.delete() # Delete the Statement if no other nodes reference it
            # For other content_object types (EmailQuote, PDFQuote, Event, PhotoDocument), do nothing (don't delete)
            
        return JsonResponse({'status': 'success', 'message': f"Node '{node_to_delete.item}' and its descendants deleted successfully."})
    except Exception as e:
        import traceback
        return JsonResponse({'status': 'error', 'message': str(e), 'traceback': traceback.format_exc()}, status=500)
