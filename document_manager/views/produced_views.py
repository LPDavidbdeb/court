from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from ..models import Document, Statement, LibraryNode, DocumentSource
from ..forms.manual_forms import ProducedDocumentForm, NodeForm
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
            text=f"Root node for {self.object.title}"
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
        root_node = LibraryNode.objects.get(document=self.object, depth=1)
        # Use prefetch_related for efficiency
        context['nodes'] = LibraryNode.get_tree(root_node).prefetch_related('content_object')
        context['modal_form'] = NodeForm()
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
            
            new_statement = Statement.objects.create(text=data['text'])
            
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
                new_statement = Statement.objects.create(text=data['text'])
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
    """AJAX view to delete a node (and all its children)."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

    try:
        node_to_delete = get_object_or_404(LibraryNode, pk=node_pk)
        
        if node_to_delete.is_root():
            return JsonResponse({'status': 'error', 'message': 'Cannot delete the root node.'}, status=400)
            
        # REFACTORED: Get the content object *before* deleting the node
        content_object_to_delete = node_to_delete.content_object
        
        node_to_delete.delete() # This is recursive
        
        # Clean up the orphaned content object (e.g., Statement)
        if content_object_to_delete:
            content_object_to_delete.delete()
            
        return JsonResponse({'status': 'success', 'message': 'Node and its children deleted.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
