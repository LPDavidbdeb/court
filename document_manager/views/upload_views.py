import csv
import os
import datetime
import traceback
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.conf import settings
from django.views.decorators.http import require_POST
from ..forms import StructuredDocumentUploadForm
from ..models import DocumentNode

# ==============================================================================
# NEW: Interactive Detail View
# ==============================================================================
def interactive_detail_view(request, pk):
    """
    Displays a document with interactive toggles for truth values.
    """
    document_root = get_object_or_404(DocumentNode, pk=pk, depth=2)
    descendants = document_root.get_descendants().order_by('path')
    
    # Use the same formatting logic as the clean view
    formatted_nodes = _format_nodes_for_display(descendants)
    
    context = {
        'document': document_root,
        'formatted_nodes': formatted_nodes,
    }
    return render(request, 'document_manager/interactive_detail_view.html', context)

# ==============================================================================
# Clean Formatted Detail View
# ==============================================================================

def clean_detail_view(request, pk):
    """
    Displays a document with legal-style numbering.
    """
    document_root = get_object_or_404(DocumentNode, pk=pk, depth=2)
    descendants = document_root.get_descendants().order_by('path')
    
    formatted_nodes = _format_nodes_for_display(descendants)
    
    context = {
        'document': document_root,
        'formatted_nodes': formatted_nodes,
    }
    return render(request, 'document_manager/clean_detail_view.html', context)

def _format_nodes_for_display(nodes):
    """
    Helper function to add numbering and indentation to each node.
    """
    formatted_list = []
    counters = {3: 0, 4: 0, 5: 0}

    for node in nodes:
        depth = node.get_depth()
        
        if depth == 3:
            counters[3] += 1
            counters[4] = 0
            counters[5] = 0
            node.numbering = f"{counters[3]}."
        elif depth == 4:
            counters[4] += 1
            counters[5] = 0
            node.numbering = f"{chr(96 + counters[4])}."
        elif depth == 5:
            counters[5] += 1
            roman_map = {1: 'i', 2: 'ii', 3: 'iii', 4: 'iv', 5: 'v'}
            node.numbering = f"{roman_map.get(counters[5], counters[5])}."
        else:
            node.numbering = ""
        
        node.indent_pixels = (depth - 3) * 40
            
        formatted_list.append(node)
        
    return formatted_list

# ==============================================================================
# Library Reset View
# ==============================================================================
@require_POST
@transaction.atomic
def reset_library_view(request):
    try:
        DocumentNode.objects.all().delete()
        from django.db import connection
        with connection.cursor() as cursor:
            table_name = DocumentNode._meta.db_table
            cursor.execute(f"TRUNCATE TABLE {table_name}")
        DocumentNode.add_root(item="Main Library", node_type='library')
        messages.success(request, "The document library has been reset successfully.")
    except Exception as e:
        messages.error(request, f"An error occurred while resetting the library: {e}")
    return redirect('document_manager:document_list')

# ==============================================================================
# Upload and Processing Views
# ==============================================================================

def document_list_view(request):
    root_documents = DocumentNode.objects.filter(depth=2, node_type='document').order_by('-created_at')
    return render(request, 'document_manager/document_list.html', {'documents': root_documents})

def document_node_detail_view(request, pk):
    node = get_object_or_404(DocumentNode, pk=pk)
    return render(request, 'document_manager/document_node_detail.html', {'node': node})

def upload_structured_document_view(request):
    if request.method == 'POST':
        form = StructuredDocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            root_name = form.cleaned_data['root_name']
            csv_file = form.cleaned_data['csv_file']

            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            unique_filename = f"{timestamp}_{csv_file.name}"
            save_dir = os.path.join(settings.BASE_DIR, 'DL', 'structured_document')
            os.makedirs(save_dir, exist_ok=True)
            file_path = os.path.join(save_dir, unique_filename)

            try:
                with open(file_path, 'wb+') as destination:
                    for chunk in csv_file.chunks():
                        destination.write(chunk)
                
                new_document_node = _process_csv_and_integrate(file_path, root_name)
                messages.success(request, f"Successfully imported document '{root_name}'.")
                return redirect('document_manager:documentnode_detail', pk=new_document_node.pk)

            except Exception as e:
                error_type = type(e).__name__
                error_message = str(e)
                tb_str = traceback.format_exc()
                full_error = f"<p><strong>An error occurred during processing.</strong></p>"
                full_error += f"<p><strong>Type:</strong> {error_type}</p>"
                full_error += f"<p><strong>Message:</strong> {error_message}</p>"
                full_error += f"<h6>Traceback:</h6><pre>{tb_str}</pre>"
                messages.error(request, full_error, extra_tags='safe')

                if os.path.exists(file_path):
                    os.remove(file_path)
                return render(request, 'document_manager/upload_structured_document.html', {'form': form})
    else:
        form = StructuredDocumentUploadForm()

    return render(request, 'document_manager/upload_structured_document.html', {'form': form})

@transaction.atomic
def _process_csv_and_integrate(file_path, document_title):
    try:
        library_root = DocumentNode.objects.get(depth=1, node_type='library')
    except DocumentNode.DoesNotExist:
        raise Exception("No 'Library' root node found. Please create a library before uploading documents.")

    with open(file_path, mode='r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        next(reader) # Skip header
        rows = [row for row in reader if any(field.strip() for field in row) and row[0].strip()]

    rows_by_id = {row[0]: {'id': row[0], 'parent_id': row[1].strip(), 'claim_text': row[2]} for row in rows}
    created_nodes = {}

    def process_node(node_id):
        if not node_id or node_id not in rows_by_id:
            return None

        if node_id in created_nodes:
            return created_nodes[node_id]

        row_data = rows_by_id[node_id]
        parent_id = row_data['parent_id']
        claim_text = row_data['claim_text']
        item_text = ' '.join(claim_text.split()[:7]) + '...'

        if not parent_id or parent_id == '0':
            new_node = library_root.add_child(
                item=document_title,
                text=claim_text,
                node_type='document'
            )
        else:
            parent_node = process_node(parent_id)
            if not parent_node:
                raise Exception(f"Could not find or create parent node with ID '{parent_id}' for child node '{node_id}'.")
            new_node = parent_node.add_child(
                item=item_text,
                text=claim_text,
                node_type='paragraph'
            )
        
        created_nodes[node_id] = new_node
        return new_node

    for row_id in rows_by_id.keys():
        process_node(row_id)
    
    document_root_id = next((rid for rid, r in rows_by_id.items() if not r['parent_id'] or r['parent_id'] == '0'), None)
    if not document_root_id or document_root_id not in created_nodes:
        raise Exception("Could not determine the root node of the uploaded document. Ensure one row has a blank or '0' parent_id.")
    
    return created_nodes[document_root_id]
