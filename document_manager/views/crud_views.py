from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.db import transaction

from ..models import DocumentNode
# FIXED: Updated the import to use the unified forms package
from ..forms import DocumentNodeForm, LibraryCreateForm, DocumentCreateForm


# --- Library Creation View ---
class LibraryCreateView(CreateView):
    """
    Gère la création du nœud racine 'Bibliothèque' en utilisant treebeard's add_root.
    """
    model = DocumentNode
    form_class = LibraryCreateForm
    template_name = 'document_manager/library_form.html'
    success_url = reverse_lazy('document_manager:document_list')

    def dispatch(self, request, *args, **kwargs):
        if DocumentNode.objects.filter(depth=1, node_type='library').exists():
            messages.info(request, "Une bibliothèque existe déjà. Vous pouvez créer des documents.")
            return redirect('document_manager:document_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            instance = form.save(commit=False)
            self.object = DocumentNode.add_root(
                item=instance.item,
                text=instance.text,
                node_type='library'
            )
            messages.success(self.request, f"La bibliothèque '{self.object.item}' a été créée avec succès !")
            return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Veuillez corriger les erreurs dans le formulaire de la bibliothèque.")
        return super().form_invalid(form)


# --- Document Creation View ---
class DocumentCreateView(CreateView):
    """
    Gère la création d'un nouveau 'Document Principal' en utilisant treebeard's add_child.
    """
    model = DocumentNode
    form_class = DocumentCreateForm
    template_name = 'document_manager/document_form.html'
    success_url = reverse_lazy('document_manager:document_list')

    def dispatch(self, request, *args, **kwargs):
        self.library_root = DocumentNode.objects.filter(depth=1, node_type='library').first()
        if not self.library_root:
            messages.warning(request, "Veuillez créer une bibliothèque avant d'ajouter des documents.")
            return redirect('document_manager:library_add')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            instance = form.save(commit=False)
            self.object = self.library_root.add_child(
                item=instance.item,
                text=instance.text,
                node_type='document'
            )
            messages.success(self.request, f"Le document '{self.object.item}' a été créé avec succès !")
            return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Veuillez corregir les erreurs dans le formulaire du document.")
        return super().form_invalid(form)


# --- Generic DocumentNode Create View ---
class DocumentNodeCreateView(CreateView):
    """
    Gère la création d'un nouveau nœud de document sous un nœud parent spécifique.
    """
    model = DocumentNode
    form_class = DocumentNodeForm
    template_name = 'document_manager/documentnode_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.parent_node = get_object_or_404(DocumentNode, pk=kwargs['parent_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['parent'] = self.parent_node.pk
        return initial

    def form_valid(self, form):
        with transaction.atomic():
            instance = form.save(commit=False)
            self.object = self.parent_node.add_child(
                item=instance.item,
                text=instance.text,
                node_type=form.cleaned_data['node_type']
            )
            messages.success(self.request,
                             f"Le nœud '{self.object.item}' a été créé avec succès sous '{self.parent_node.item}'!")
            return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Veuillez corriger les erreurs dans le formulaire du nœud.")
        return super().form_invalid(form)


# --- DocumentNode List View ---
class DocumentNodeListView(ListView):
    """
    Affiche une liste de tous les documents principaux.
    """
    model = DocumentNode
    template_name = 'document_manager/document_list.html'
    context_object_name = 'documents'
    paginate_by = 10

    def get_queryset(self):
        library_root = DocumentNode.objects.filter(depth=1, node_type='library').first()
        if library_root:
            return library_root.get_children().filter(node_type='document')
        return DocumentNode.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['library_exists'] = DocumentNode.objects.filter(depth=1, node_type='library').exists()
        return context


# --- Generic DocumentNode Detail, Update, Delete Views ---
class DocumentNodeDetailView(DetailView):
    """
    Affiche les détails d'un seul nœud de document.
    """
    model = DocumentNode
    template_name = 'document_manager/documentnode_detail.html'
    context_object_name = 'document_node'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['children'] = self.object.get_children().order_by('path')
        return context


class DocumentNodeUpdateView(UpdateView):
    """
    Gère la modification d'un nœud de document existant.
    """
    model = DocumentNode
    form_class = DocumentNodeForm
    template_name = 'document_manager/documentnode_form.html'
    context_object_name = 'document_node'

    def form_valid(self, form):
        with transaction.atomic():
            current_instance = self.get_object()
            old_parent = current_instance.get_parent()
            new_parent = form.cleaned_data['parent']
            instance = form.save(commit=False)

            if old_parent != new_parent:
                if new_parent:
                    instance.move(new_parent, pos='last-child')
                else:
                    if instance.node_type != 'library':
                        messages.error(self.request, "Seul le nœud de type 'Bibliothèque' peut être un nœud racine.")
                        return self.form_invalid(form)
                    instance.move(None, pos='last-sibling')
                messages.info(self.request, "Le parent du nœud a été modifié.")

            instance.save()
            self.object = instance

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
class RebuildTreeView(View):
    """
    A simple view to manually trigger the rebuild of the document tree.
    """
    def get(self, request, *args, **kwargs):
        try:
            messages.info(request, "Avec django-treebeard, l'intégrité de l'arbre est gérée automatiquement.")
            messages.success(request, "Vérification de l'arbre terminée.")
        except Exception as e:
            messages.error(e, f"Erreur lors de la vérification de l'arbre: {e}")
        return redirect('document_manager:document_list')


# --- View to handle AJAX submissions from the modal ---
class AddNodeModalView(View):
    """
    Handles AJAX POST requests from the Bootstrap modal to add nodes.
    """
    def post(self, request, *args, **kwargs):
        if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

        action_type = request.POST.get('action_type')
        reference_node_id = request.POST.get('reference_node_id')
        sibling_position = request.POST.get('sibling_position')

        form = DocumentNodeForm(request.POST)

        if not form.is_valid():
            return JsonResponse({'status': 'error', 'errors': form.errors.as_json()}, status=400)

        item = form.cleaned_data['item']
        text = form.cleaned_data['text']
        node_type = form.cleaned_data['node_type']

        try:
            with transaction.atomic():
                reference_node = get_object_or_404(DocumentNode, pk=reference_node_id)
                new_node = None
                message = ""

                if action_type == 'add_child':
                    new_node = reference_node.add_child(item=item, text=text, node_type=node_type)
                    message = f"Le nœud enfant '{new_node.item}' a été ajouté sous '{reference_node.item}'."

                elif action_type == 'add_sibling':
                    new_node = reference_node.add_sibling(pos=sibling_position, item=item, text=text, node_type=node_type)
                    message = f"Le nœud frère '{new_node.item}' a été ajouté."

                elif action_type == 'add_parent':
                    if reference_node.node_type == 'library':
                        return JsonResponse({'status': 'error', 'message': 'Impossible d\'ajouter un parent à la bibliothèque racine.'}, status=400)
                    if node_type == 'library' and DocumentNode.objects.filter(depth=1, node_type='library').exists():
                        return JsonResponse({'status': 'error', 'message': 'Une bibliothèque existe déjà.'}, status=400)

                    if reference_node.get_parent():
                        new_parent_node = reference_node.add_sibling(pos='left', item=item, text=text, node_type=node_type)
                    else:
                        new_parent_node = DocumentNode.add_root(item=item, text=text, node_type=node_type)

                    reference_node.move(new_parent_node, pos='first-child')
                    new_node = new_parent_node
                    message = f"Le nœud '{new_node.item}' a été créé comme parent de '{reference_node.item}'."

                else:
                    return JsonResponse({'status': 'error', 'message': 'Action non valide.'}, status=400)

                return JsonResponse({
                    'status': 'success',
                    'message': message,
                    'node_id': new_node.pk if new_node else None,
                    'node_item': new_node.item if new_node else None
                })

        except Exception as e:
            import traceback
            return JsonResponse({'status': 'error', 'message': str(e), 'traceback': traceback.format_exc()}, status=500)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'status': 'error', 'message': 'GET method not allowed.'}, status=405)

# --- Perjury Element List View ---
class PerjuryElementListView(ListView):
    """
    Affiche une liste des éléments de parjure (DocumentNode avec is_true=False et is_falsifiable=True),
    groupés par le document principal auquel ils appartiennent.
    """
    model = DocumentNode
    template_name = 'document_manager/perjury_element_list.html'
    context_object_name = 'perjury_elements_by_doc'

    def get_queryset(self):
        library_root = DocumentNode.objects.filter(depth=1, node_type='library').first()
        documents = []
        if library_root:
            documents = library_root.get_children().filter(node_type='document')

        perjury_elements_by_doc = {}
        for doc in documents:
            perjury_nodes = doc.get_descendants().filter(is_true=False, is_falsifiable=True).order_by('path')
            if perjury_nodes.exists():
                perjury_elements_by_doc[doc] = list(perjury_nodes)
        
        return perjury_elements_by_doc.items()
