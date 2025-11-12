from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType

from ..models import LibraryNode, Document, Statement
from ..forms.manual_forms import LibraryNodeCreateForm

@require_POST
def add_library_node_ajax(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)
    form = LibraryNodeCreateForm(request.POST)

    reference_node_pk = request.POST.get('reference_node_pk')
    action_type = request.POST.get('action_type') # 'add_child', 'add_sibling_left', 'add_sibling_right', 'add_parent', 'add_root'

    if form.is_valid():
        try:
            with transaction.atomic():
                new_node_instance = form.save(commit=False, document=document)
                
                if not reference_node_pk and action_type == 'add_root':
                    # This is for creating the very first root node for a document
                    LibraryNode.add_root(instance=new_node_instance)
                    message = f"Root node '{new_node_instance.item}' created successfully."
                else:
                    reference_node = get_object_or_404(LibraryNode, pk=reference_node_pk, document=document)

                    # Backend validation for root nodes (in case frontend is bypassed)
                    if reference_node.is_root() and (action_type == 'add_sibling_left' or action_type == 'add_sibling_right' or action_type == 'add_parent'):
                        return JsonResponse({'status': 'error', 'message': f"Cannot '{action_type.replace('_', ' ')}' to a root node."}, status=400)

                    if action_type == 'add_child':
                        reference_node.add_child(instance=new_node_instance)
                        message = f"Child node '{new_node_instance.item}' added to '{reference_node.item}'."
                    elif action_type == 'add_sibling_left':
                        reference_node.add_sibling(instance=new_node_instance, pos='left')
                        message = f"Sibling node '{new_node_instance.item}' added to the left of '{reference_node.item}'."
                    elif action_type == 'add_sibling_right':
                        reference_node.add_sibling(instance=new_node_instance, pos='right')
                        message = f"Sibling node '{new_node_instance.item}' added to the right of '{reference_node.item}'."
                    elif action_type == 'add_parent':
                        # Corrected logic for 'add_parent':
                        # 1. Add the new_node_instance as a sibling to the reference_node.
                        #    This inserts new_node_instance into the tree.
                        reference_node.add_sibling(instance=new_node_instance, pos='left') # Position doesn't strictly matter here as reference_node will be moved.
                        
                        # 2. Now, move the original reference_node to be a child of the new_node_instance.
                        #    new_node_instance is now a valid node in the tree.
                        reference_node.move(new_node_instance, pos='last-child')
                        message = f"Node '{new_node_instance.item}' created as parent of '{reference_node.item}'."
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Invalid action type.'}, status=400)
                
                return JsonResponse({'status': 'success', 'message': message, 'node_id': new_node_instance.pk})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        errors = form.errors.as_json()
        return JsonResponse({'status': 'error', 'message': 'Form validation failed.', 'errors': errors}, status=400)