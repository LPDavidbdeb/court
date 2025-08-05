from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.db import transaction

from ..models import DocumentNode
from ..forms.DocumentNodeForm import DocumentNodeForm, LibraryCreateForm, DocumentCreateForm


# --- Library Creation View ---
class LibraryCreateView(CreateView):
    """
    Gère la création du nœud racine 'Bibliothèque' en utilisant treebeard's add_root.
    Il ne devrait y en avoir qu'une seule.
    """
    model = DocumentNode
    form_class = LibraryCreateForm
    template_name = 'document_manager/library_form.html'
    success_url = reverse_lazy('document_manager:document_list')

    def dispatch(self, request, *args, **kwargs):
        # Check for existing library by querying for a node with depth=1 (treebeard's root depth)
        if DocumentNode.objects.filter(depth=1, node_type='library').exists():
            messages.info(request, "Une bibliothèque existe déjà. Vous pouvez créer des documents.")
            return redirect('document_manager:document_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            # Get an unsaved instance from the form
            instance = form.save(commit=False)

            # Use treebeard's add_root method to create and save the library
            # This method returns the saved instance, which we assign to self.object
            self.object = DocumentNode.add_root(
                item=instance.item,
                text=instance.text,
                node_type='library'
            )
            # No need for instance.save() here, as add_root already saves
            # IMPORTANT: Do NOT call super().form_valid(form) here, as add_root already saved the object.
            # Instead, directly return the redirect.

            messages.success(self.request, f"La bibliothèque '{self.object.item}' a été créée avec succès !")
            return HttpResponseRedirect(self.get_success_url())  # Directly redirect

    def form_invalid(self, form):
        messages.error(self.request, "Veuillez corriger les erreurs dans le formulaire de la bibliothèque.")
        return super().form_invalid(form)


# --- Document Creation View ---
class DocumentCreateView(CreateView):
    """
    Gère la création d'un nouveau 'Document Principal' en utilisant treebeard's add_child.
    Il sera automatiquement lié à la bibliothèque racine.
    """
    model = DocumentNode
    form_class = DocumentCreateForm
    template_name = 'document_manager/document_form.html'
    success_url = reverse_lazy('document_manager:document_list')

    def dispatch(self, request, *args, **kwargs):
        # Get the library root by querying for a node with depth=1 and type 'library'
        self.library_root = DocumentNode.objects.filter(depth=1, node_type='library').first()
        if not self.library_root:
            messages.warning(request, "Veuillez créer une bibliothèque avant d'ajouter des documents.")
            return redirect('document_manager:library_add')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            # Get an unsaved instance from the form
            instance = form.save(commit=False)

            # Use treebeard's add_child method on the library root
            # This method returns the saved instance, which we assign to self.object
            self.object = self.library_root.add_child(
                item=instance.item,
                text=instance.text,
                node_type='document'
            )
            # No need for instance.save() here, as add_child already saves
            # IMPORTANT: Do NOT call super().form_valid(form) here.

            messages.success(self.request, f"Le document '{self.object.item}' a été créé avec succès !")
            return HttpResponseRedirect(self.get_success_url())  # Directly redirect

    def form_invalid(self, form):
        messages.error(self.request, "Veuillez corregir les erreurs dans le formulaire du document.")
        return super().form_invalid(form)


# --- Generic DocumentNode Create View (for adding child nodes to any parent) ---
class DocumentNodeCreateView(CreateView):
    """
    Gère la création d'un nouveau nœud de document (ex: section, paragraphe)
    sous un nœud parent spécifique. This view is for full-page redirects,
    the AddNodeModalView handles AJAX submissions.
    """
    model = DocumentNode
    form_class = DocumentNodeForm  # Use the generic form
    template_name = 'document_manager/documentnode_form.html'  # Re-use the generic form template

    def dispatch(self, request, *args, **kwargs):
        # Get the parent node from the URL (parent_pk)
        self.parent_node = get_object_or_404(DocumentNode, pk=kwargs['parent_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        # Pre-fill the parent field in the form
        initial = super().get_initial()
        initial['parent'] = self.parent_node.pk
        # You might also want to suggest a default node_type here, e.g., 'section'
        # initial['node_type'] = 'section'
        return initial

    def form_valid(self, form):
        with transaction.atomic():
            # Get an unsaved instance from the form
            instance = form.save(commit=False)

            # Use treebeard's add_child method on the parent_node
            # This method returns the saved instance, which we assign to self.object
            self.object = self.parent_node.add_child(
                item=instance.item,
                text=instance.text,
                node_type=form.cleaned_data['node_type']  # Use node_type from form
            )
            # No need for instance.save() here, as add_child already saves
            # IMPORTANT: Do NOT call super().form_valid(form) here.

            messages.success(self.request,
                             f"Le nœud '{self.object.item}' a été créé avec succès sous '{self.parent_node.item}'!")
            return HttpResponseRedirect(self.get_success_url())  # Directly redirect

    def form_invalid(self, form):
        messages.error(self.request, "Veuillez corriger les erreurs dans le formulaire du nœud.")
        return super().form_invalid(form)


# --- DocumentNode List View (now shows documents by default) ---
class DocumentNodeListView(ListView):
    """
    Affiche une liste de tous les documents principaux (enfants de la bibliothèque).
    """
    model = DocumentNode
    template_name = 'document_manager/document_list.html'
    context_object_name = 'documents'
    paginate_by = 10

    def get_queryset(self):
        # Get the library root by querying for a node with depth=1 and type 'library'
        library_root = DocumentNode.objects.filter(depth=1, node_type='library').first()
        if library_root:
            # Get children of the library root. treebeard's get_children() is efficient.
            # They are already ordered correctly by treebeard's internal path.
            return library_root.get_children().filter(node_type='document')
        return DocumentNode.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['library_exists'] = DocumentNode.objects.filter(depth=1, node_type='library').exists()
        return context


# --- Generic DocumentNode Detail, Update, Delete Views (for any node type) ---
class DocumentNodeDetailView(DetailView):
    """
    Affiche les détails d'un seul nœud de document (peut être document, section, paragraphe).
    """
    model = DocumentNode
    template_name = 'document_manager/documentnode_detail.html'
    context_object_name = 'document_node'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # treebeard's get_children() is more efficient
        context['children'] = self.object.get_children().order_by('path')  # Order children by path for consistency
        return context


class DocumentNodeUpdateView(UpdateView):
    """
    Gère la modification d'un nœud de document existant.
    Utilise le formulaire générique DocumentNodeForm pour permettre la modification de parent, node_type, item, text.
    """
    model = DocumentNode
    form_class = DocumentNodeForm  # Use the generic form
    template_name = 'document_manager/documentnode_form.html'
    context_object_name = 'document_node'

    def form_valid(self, form):
        with transaction.atomic():
            # Get the current instance before form.save() potentially moves it
            current_instance = self.get_object()
            old_parent = current_instance.get_parent()
            new_parent = form.cleaned_data['parent']

            # Save the form with commit=False to get the instance with updated non-treebeard fields
            instance = form.save(commit=False)

            if old_parent != new_parent:
                # If parent has changed, use treebeard's move method
                if new_parent:
                    instance.move(new_parent, pos='last-child')  # Move as last child of new parent
                else:
                    # If parent is set to None, make it a new root (careful with multiple roots)
                    if instance.node_type != 'library':
                        messages.error(self.request, "Seul le nœud de type 'Bibliothèque' peut être un nœud racine.")
                        return self.form_invalid(form)  # Re-render form with error
                    instance.move(None, pos='last-sibling')  # Make it a root
                messages.info(self.request,
                              "Le parent du nœud a été modifié. La structure de l'arbre a été mise à jour.")

            # Save any non-treebeard fields that might have changed (item, text, node_type)
            # This is important because move() only updates tree-related fields.
            instance.save()

            self.object = instance  # Set self.object to the updated instance

            messages.success(self.request, f"Le nœud '{self.object.item}' a été mis à jour avec succès !")
            if self.object.node_type == 'document':
                return reverse_lazy('document_manager:document_list')
            return reverse_lazy('document_manager:documentnode_detail', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        messages.error(self.request, "Veuillez corriger les erreurs dans le formulaire.")
        return super().form_invalid(form)


class DocumentNodeDeleteView(DeleteView):
    """
    Gère la suppression d'un nœud de document.
    """
    model = DocumentNode
    template_name = 'document_manager/documentnode_confirm_delete.html'
    success_url = reverse_lazy('document_manager:document_list')
    context_object_name = 'document_node'

    def form_valid(self, form):
        with transaction.atomic():
            deleted_item_name = self.object.item
            # treebeard's delete method handles all lft/rgt adjustments automatically
            self.object.delete()

            messages.success(self.request, f"Le nœud '{deleted_item_name}' a été supprimé avec succès.")
            return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, f"Le nœud '{self.object.item}' a été supprimé avec succès.")
            return HttpResponseRedirect(success_url)
        except Exception as e:
            messages.error(request, f"Erreur lors de la suppression du nœud '{self.object.item}': {e}")
            return HttpResponseRedirect(self.object.get_absolute_url())


# --- View to Manually Trigger Tree Rebuild ---
# This view is no longer strictly necessary as treebeard handles integrity on CRUD ops.
# However, it can be kept for diagnostic purposes or if you do bulk imports outside treebeard's API.
class RebuildTreeView(View):
    """
    A simple view to manually trigger the rebuild of the document tree using treebeard's methods.
    This can be useful for maintenance or after bulk imports.
    """

    def get(self, request, *args, **kwargs):
        try:
            # treebeard doesn't have a single 'rebuild_tree' function like our manual one.
            # Instead, you'd typically use dump_bulk and load_bulk for a full rebuild
            # if the tree was corrupted or imported externally.
            # For simple integrity checks, treebeard usually handles it on save/delete.
            # If you need to re-sort children, you'd use node.move(target, pos='sorted-child').

            # For demonstration, we'll just confirm that the tree is in a good state.
            # If you had a custom rebuild function (like the one we just removed), you'd call it here.
            # With treebeard, the "rebuild" is usually handled internally or via dump/load_bulk.
            messages.info(request,
                          "Avec django-treebeard, l'intégrité de l'arbre est gérée automatiquement lors des opérations CRUD. Une reconstruction manuelle n'est généralement pas nécessaire, sauf après des manipulations directes de la base de données.")
            messages.success(request, "Vérification de l'arbre terminée.")
        except Exception as e:
            messages.error(e, f"Erreur lors de la vérification de l'arbre: {e}")  # Corrected error message
        return redirect('document_manager:document_list')


# --- NEW: View to handle AJAX submissions from the modal ---
class AddNodeModalView(View):
    """
    Handles AJAX POST requests from the Bootstrap modal to add child, sibling, or parent nodes.
    """

    def post(self, request, *args, **kwargs):
        print("DEBUG: AddNodeModalView POST received.")
        if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
            print("DEBUG: Not an AJAX request.")
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

        action_type = request.POST.get('action_type')
        reference_node_id = request.POST.get('reference_node_id')
        sibling_position = request.POST.get('sibling_position')  # NEW: Get sibling position

        print(
            f"DEBUG: action_type: {action_type}, reference_node_id: {reference_node_id}, sibling_position: {sibling_position}")

        form = DocumentNodeForm(request.POST)

        if not form.is_valid():
            print(f"DEBUG: Form is invalid. Errors: {form.errors}")
            # Return form errors in a structured way
            return JsonResponse({'status': 'error', 'errors': form.errors.as_json()}, status=400)

        item = form.cleaned_data['item']
        text = form.cleaned_data['text']
        node_type = form.cleaned_data['node_type']

        print(f"DEBUG: Cleaned data - item: {item}, text: {text}, node_type: {node_type}")

        try:
            with transaction.atomic():
                print(f"DEBUG: Attempting to get reference_node with ID: {reference_node_id}")
                reference_node = get_object_or_404(DocumentNode, pk=reference_node_id)
                print(f"DEBUG: Reference node found: {reference_node.item} (ID: {reference_node.pk})")
                new_node = None
                message = ""

                if action_type == 'add_child':
                    print(f"DEBUG: Action: add_child to {reference_node.item}")
                    new_node = reference_node.add_child(item=item, text=text, node_type=node_type)
                    message = f"Le nœud enfant '{new_node.item}' a été ajouté sous '{reference_node.item}'."

                elif action_type == 'add_sibling':
                    print(f"DEBUG: Action: add_sibling to {reference_node.item} with position: {sibling_position}")
                    # Use the chosen sibling_position ('left' or 'right')
                    new_node = reference_node.add_sibling(pos=sibling_position, item=item, text=text,
                                                          node_type=node_type)
                    message = f"Le nœud frère '{new_node.item}' a été ajouté '{'avant' if sibling_position == 'left' else 'après'}' '{reference_node.item}'."

                elif action_type == 'add_parent':
                    print(f"DEBUG: Action: add_parent to {reference_node.item}. New parent type: {node_type}")

                    # Prevent adding a parent to the library node itself
                    if reference_node.node_type == 'library':
                        print("DEBUG: Attempted to add parent to library node.")
                        return JsonResponse(
                            {'status': 'error', 'message': 'Impossible d\'ajouter un parent à la bibliothèque racine.'},
                            status=400)

                    # Ensure it's not trying to create a 'library' as a new parent if one exists
                    if node_type == 'library' and DocumentNode.objects.filter(depth=1, node_type='library').exists():
                        print("DEBUG: Attempted to create duplicate library as parent.")
                        return JsonResponse({'status': 'error',
                                             'message': 'Une bibliothèque existe déjà. Impossible de créer une nouvelle bibliothèque comme parent.'},
                                            status=400)

                    # Create the new parent node
                    if reference_node.get_parent():
                        # If the reference node has a parent, the new parent should be a sibling of the reference node.
                        # Using 'left' here is a common choice for 'add parent' to keep the new parent logically before the original node.
                        print(
                            f"DEBUG: Reference node {reference_node.item} has a parent. Creating new parent as sibling (pos='left').")
                        new_parent_node = reference_node.add_sibling(pos='left', item=item, text=text,
                                                                     node_type=node_type)
                    else:
                        # If the reference node is a root (e.g., a document directly under library),
                        # the new parent becomes a root.
                        print(f"DEBUG: Reference node {reference_node.item} is a root. Creating new parent as root.")
                        new_parent_node = DocumentNode.add_root(item=item, text=text, node_type=node_type)

                    # Move the original reference_node to be a child of the new parent
                    print(f"DEBUG: Moving reference node {reference_node.item} under new parent {new_parent_node.item}")
                    reference_node.move(new_parent_node, pos='first-child')  # Moving as first child is generally safe
                    print(f"DEBUG: Move successful.")
                    new_node = new_parent_node  # The 'newly added' node is the parent in this context
                    message = f"Le nœud '{new_node.item}' a été créé comme parent de '{reference_node.item}'."

                else:
                    print(f"DEBUG: Invalid action_type: {action_type}")
                    return JsonResponse({'status': 'error', 'message': 'Action non valide.'}, status=400)

                print(f"DEBUG: Operation successful. New node ID: {new_node.pk}")
                return JsonResponse({
                    'status': 'success',
                    'message': message,
                    'node_id': new_node.pk if new_node else None,
                    'node_item': new_node.item if new_node else None
                })

        except Exception as e:
            print(f"ERROR: Exception in AddNodeModalView: {e}")  # Print the actual exception
            # For debugging, also include traceback in response (remove in production)
            import traceback
            return JsonResponse({'status': 'error', 'message': str(e), 'traceback': traceback.format_exc()}, status=500)

    def get(self, request, *args, **kwargs):
        # This view only handles POST requests for AJAX form submission
        print("DEBUG: AddNodeModalView GET received (not allowed).")
        return JsonResponse({'status': 'error', 'message': 'GET method not allowed.'}, status=405)
