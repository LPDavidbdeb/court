from django.db import transaction, models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from ..models import Document, Statement, LibraryNode, DocumentSource
from ..forms.manual_forms import ProducedDocumentForm, NodeForm, LibraryNodeCreateForm
from django.contrib.contenttypes.models import ContentType
import json
from argument_manager.models import TrameNarrative
from datetime import date

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
            is_user_created=True
        )
        
        LibraryNode.add_root(
            document=self.object,
            content_object=root_statement,
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
        
        all_nodes = list(LibraryNode.objects.filter(
            document=self.object
        ).select_related('content_type').prefetch_related('content_object').order_by('path'))

        trame_narrative_ct = ContentType.objects.get_for_model(TrameNarrative)
        narrative_nodes = [node for node in all_nodes if node.content_type_id == trame_narrative_ct.id and node.content_object is not None]

        if narrative_nodes:
            narratives_to_prefetch = [node.content_object for node in narrative_nodes]

            prefetch_lookups = [
                'evenements',
                'citations_courriel__email',
                'citations_pdf__pdf_document',
                'photo_documents',
                'source_statements' # NEW
            ]
            
            models.prefetch_related_objects(narratives_to_prefetch, *prefetch_lookups)

        context['nodes'] = [node for node in all_nodes if node.depth == 1]
        
        context['modal_form'] = NodeForm()
        context['library_node_create_form'] = LibraryNodeCreateForm()
        return context

# --- AJAX Views ---
@transaction.atomic
def ajax_add_node(request, node_pk):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
    try:
        parent_node = get_object_or_404(LibraryNode, pk=node_pk)
        form = NodeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_statement = Statement.objects.create(text=data['text'], is_user_created=True)
            new_node = parent_node.add_child(
                document=parent_node.document,
                content_object=new_statement,
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
    node_to_edit = get_object_or_404(LibraryNode.objects.select_related('content_type'), pk=node_pk)
    if request.method == 'POST':
        form = NodeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            node_to_edit.item = data['item']
            node_to_edit.save()
            if node_to_edit.content_object and hasattr(node_to_edit.content_object, 'text'):
                node_to_edit.content_object.text = data['text']
                node_to_edit.content_object.save()
            else:
                new_statement = Statement.objects.create(text=data['text'], is_user_created=True)
                node_to_edit.content_object = new_statement
                node_to_edit.save()
            return JsonResponse({'status': 'success', 'message': 'Node updated.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Form is invalid', 'errors': form.errors.as_json()}, status=400)
    
    text_content = ''
    if node_to_edit.content_object and hasattr(node_to_edit.content_object, 'text'):
        text_content = node_to_edit.content_object.text
    data = {'item': node_to_edit.item, 'text': text_content}
    return JsonResponse(data)

@transaction.atomic
def ajax_delete_node(request, node_pk):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
    try:
        node_to_delete = get_object_or_404(LibraryNode, pk=node_pk)
        if node_to_delete.is_root():
            return JsonResponse({'status': 'error', 'message': 'Cannot delete the root node.'}, status=400)
        
        nodes_to_be_deleted = [node_to_delete] + list(node_to_delete.get_descendants())
        content_objects_to_consider = {}
        for node in nodes_to_be_deleted:
            if node.content_object:
                key = (node.content_type_id, node.object_id)
                if key not in content_objects_to_consider:
                    content_objects_to_consider[key] = node.content_object

        node_to_delete.delete()

        statement_content_type = ContentType.objects.get_for_model(Statement)
        for (ct_id, obj_id), content_obj in content_objects_to_consider.items():
            if ct_id == statement_content_type.id and isinstance(content_obj, Statement):
                if content_obj.is_user_created:
                    if not LibraryNode.objects.filter(content_type=statement_content_type, object_id=content_obj.pk).exists():
                        content_obj.delete()
            
        return JsonResponse({'status': 'success', 'message': f"Node '{node_to_delete.item}' and its descendants deleted successfully."})
    except Exception as e:
        import traceback
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
