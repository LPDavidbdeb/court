from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.db import transaction
from django.db.models import Prefetch
from datetime import datetime, date
from django.utils import timezone

# Imports for the new evidence logic
from argument_manager.models import TrameNarrative
from email_manager.models import Quote as EmailQuote, Email
from pdf_manager.models import Quote as PDFQuote, PDFDocument
from events.models import Event
from photos.models import PhotoDocument, Photo

from ..models import DocumentNode
from ..forms import DocumentNodeForm, LibraryCreateForm, DocumentCreateForm


# --- Library Creation View ---
class LibraryCreateView(CreateView):
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
    model = DocumentNode
    template_name = 'document_manager/documentnode_detail.html'
    context_object_name = 'document_node'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['children'] = self.object.get_children().order_by('path')
        return context


class DocumentNodeUpdateView(UpdateView):
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
    def get(self, request, *args, **kwargs):
        try:
            messages.info(request, "Avec django-treebeard, l'intégrité de l'arbre est gérée automatiquement.")
            messages.success(request, "Vérification de l'arbre terminée.")
        except Exception as e:
            messages.error(e, f"Erreur lors de la vérification de l'arbre: {e}")
        return redirect('document_manager:document_list')


# --- View to handle AJAX submissions from the modal ---
class AddNodeModalView(View):
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


# --- Perjury Element List View (REFERENCE VERSION) ---
class PerjuryElementListView(ListView):
    model = DocumentNode
    template_name = 'document_manager/perjury_element_list.html'
    context_object_name = 'perjury_elements_by_doc'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 1. Get all perjury nodes with prefetched related data
        prefetch_trames = Prefetch(
            'trames_narratives',
            queryset=TrameNarrative.objects.prefetch_related(
                'evenements',
                'citations_courriel__email',
                'citations_pdf__pdf_document',
                'photo_documents__photos'
            )
        )
        all_perjury_nodes = DocumentNode.objects.filter(
            is_true=False, is_falsifiable=True
        ).prefetch_related(prefetch_trames)

        # 2. Collect all unique source documents and individual evidence items
        source_doc_set = set()
        node_evidence_map = {node.pk: [] for node in all_perjury_nodes}
        used_items_set = set()

        for node in all_perjury_nodes:
            evidence_for_node = []
            for trame in node.trames_narratives.all():
                for eq in trame.citations_courriel.all():
                    source_doc_set.add(eq.email)
                    evidence_for_node.append(eq)
                    used_items_set.add(eq)
                for pq in trame.citations_pdf.all():
                    source_doc_set.add(pq.pdf_document)
                    evidence_for_node.append(pq)
                    used_items_set.add(pq)
                for event in trame.evenements.all():
                    source_doc_set.add(event)
                    evidence_for_node.append(event)
                for photo_doc in trame.photo_documents.all():
                    source_doc_set.add(photo_doc)
                    evidence_for_node.append(photo_doc)
                    used_items_set.update(photo_doc.photos.all())
            
            node_evidence_map[node.pk] = list(set(evidence_for_node))

        # 3. Sort source documents by date
        def get_date(obj):
            dt = None
            if isinstance(obj, Email):
                dt = obj.date_sent
            elif isinstance(obj, PDFDocument):
                dt = obj.uploaded_at
            elif isinstance(obj, PhotoDocument):
                dt = obj.created_at
            elif isinstance(obj, Event):
                dt = obj.date

            if not dt:
                return None

            if isinstance(dt, date) and not isinstance(dt, datetime):
                dt = datetime.combine(dt, datetime.min.time())

            if timezone.is_naive(dt):
                return timezone.make_aware(dt)
            
            return dt

        sorted_source_docs = sorted([d for d in source_doc_set if get_date(d)], key=get_date)
        
        # 4. Create the main exhibit map (P-X)
        exhibit_map = {doc: f"P-{i+1}" for i, doc in enumerate(sorted_source_docs)}

        # 5. Create the item map (P-X.Y)
        item_map = {}
        for doc, p_id in exhibit_map.items():
            items_in_doc = []
            if isinstance(doc, Email): items_in_doc = sorted(list(doc.quotes.all()), key=lambda x: x.pk)
            elif isinstance(doc, PDFDocument): items_in_doc = sorted(list(doc.quotes.all()), key=lambda x: x.pk)
            elif isinstance(doc, PhotoDocument): items_in_doc = sorted(list(doc.photos.all()), key=lambda x: x.pk)
            
            item_counter = 1
            for item in items_in_doc:
                if item in used_items_set:
                    item_map[item] = f"{p_id}.{item_counter}"
                    item_counter += 1

        # 6. Structure the final data for the template
        perjury_elements_by_doc = {}
        library_root = DocumentNode.objects.filter(depth=1, node_type='library').first()
        if library_root:
            documents = library_root.get_children().filter(node_type='document')
            for doc in documents:
                nodes_in_doc = [n for n in all_perjury_nodes if n.path.startswith(doc.path) and n.depth > doc.depth]
                if nodes_in_doc:
                    for node in nodes_in_doc:
                        node.processed_evidence = self.process_evidence_for_node(
                            node_evidence_map.get(node.pk, []),
                            exhibit_map,
                            item_map,
                            sorted_source_docs
                        )
                    perjury_elements_by_doc[doc] = nodes_in_doc
        
        # 7. Create exhibits list for template
        exhibits_list = []
        for doc in sorted_source_docs:
            p_id = exhibit_map.get(doc)
            if not p_id:
                continue

            type_fr = ''
            title = ''
            if isinstance(doc, Email):
                type_fr = 'Courriel'
                title = doc.subject
            elif isinstance(doc, PDFDocument):
                type_fr = 'Document PDF'
                title = doc.title
            elif isinstance(doc, PhotoDocument):
                type_fr = 'Document Photo'
                title = doc.title
            elif isinstance(doc, Event):
                type_fr = 'Événement'
                title = f"Événement du {get_date(doc).strftime('%Y-%m-%d')}"

            exhibits_list.append({
                'main_id': p_id,
                'type_fr': type_fr,
                'title': title,
                'date': get_date(doc),
                'evidence_obj': doc,
                'type': doc.__class__.__name__
            })

        context['exhibits'] = exhibits_list
        context['item_map'] = item_map
        context['perjury_elements_by_doc'] = perjury_elements_by_doc.items()
        return context

    def process_evidence_for_node(self, raw_evidence, exhibit_map, item_map, sorted_source_docs):
        processed = []

        def get_source_doc(obj):
            if isinstance(obj, EmailQuote): return obj.email
            if isinstance(obj, PDFQuote): return obj.pdf_document
            if isinstance(obj, (Event, PhotoDocument)): return obj
            return None

        def get_sort_key(obj):
            source = get_source_doc(obj)
            if source in sorted_source_docs:
                return sorted_source_docs.index(source)
            return -1
        
        sorted_evidence = sorted(raw_evidence, key=get_sort_key)

        for obj in sorted_evidence:
            data = {'obj': obj}
            source_doc = get_source_doc(obj)
            data['p_id'] = exhibit_map.get(source_doc, '')

            if isinstance(obj, EmailQuote):
                data['type'] = 'EmailQuote'
                data['item_id'] = item_map.get(obj)
                data['content'] = obj.quote_text
                data['source_title'] = source_doc.subject
                data['date'] = source_doc.date_sent
            elif isinstance(obj, PDFQuote):
                data['type'] = 'PDFQuote'
                data['item_id'] = item_map.get(obj)
                data['content'] = obj.quote_text
                data['source_title'] = source_doc.title
                data['date'] = source_doc.uploaded_at
            elif isinstance(obj, Event):
                data['type'] = 'Event'
                data['item_id'] = None
                data['content'] = obj.explanation
                data['source_title'] = f"Événement du {obj.date.strftime('%Y-%m-%d')}"
                data['date'] = obj.date
            elif isinstance(obj, PhotoDocument):
                data['type'] = 'PhotoDocument'
                data['item_id'] = None
                data['content'] = obj.description
                data['source_title'] = obj.title
                data['date'] = obj.created_at
                data['photos'] = []
                for photo in sorted(list(obj.photos.all()), key=lambda p: p.pk):
                    if photo in item_map:
                        data['photos'].append({'obj': photo, 'item_id': item_map.get(photo)})
            
            processed.append(data)
        return processed

    def get_queryset(self):
        return DocumentNode.objects.none()


# --- Perjury Element List View with TrameNarrative (NEW VERSION) ---
class PerjuryElementWithTrameListView(ListView):
    model = DocumentNode
    template_name = 'document_manager/perjury_element_list_with_trame.html'
    context_object_name = 'data_by_document'

    def _get_paragraph_numbering_map(self, document_node):
        """
        Replicates the numbering logic from the clean_detail_view to create a 
        map of node PKs to their legal-style numbering string.
        """
        nodes = document_node.get_descendants().order_by('path')
        numbering_map = {}
        counters = {3: 0, 4: 0, 5: 0}

        for node in nodes:
            depth = node.get_depth()
            numbering = ""
            
            if depth == 3:
                counters[3] += 1
                counters[4] = 0
                counters[5] = 0
                numbering = f"{counters[3]}."
            elif depth == 4:
                counters[4] += 1
                counters[5] = 0
                # This will produce a, b, c, ...
                numbering = f"{chr(96 + counters[4])}."
            elif depth == 5:
                counters[5] += 1
                roman_map = {1: 'i', 2: 'ii', 3: 'iii', 4: 'iv', 5: 'v'}
                numbering = f"{roman_map.get(counters[5], counters[5])}."
            
            if numbering:
                numbering_map[node.pk] = numbering.rstrip('.') # Store without trailing dot

        return numbering_map

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 1. Get all perjury nodes
        prefetch_trames = Prefetch(
            'trames_narratives',
            queryset=TrameNarrative.objects.prefetch_related(
                'evenements', 'citations_courriel__email', 'citations_pdf__pdf_document', 'photo_documents__photos'
            )
        )
        all_perjury_nodes = DocumentNode.objects.filter(
            is_true=False, is_falsifiable=True
        ).prefetch_related(prefetch_trames).order_by('path')

        # 2. Collect unique items for global numbering
        source_doc_set, all_trames_set, used_items_set = set(), set(), set()
        for node in all_perjury_nodes:
            for trame in node.trames_narratives.all():
                all_trames_set.add(trame)
                for eq in trame.citations_courriel.all():
                    source_doc_set.add(eq.email)
                    used_items_set.add(eq)
                for pq in trame.citations_pdf.all():
                    source_doc_set.add(pq.pdf_document)
                    used_items_set.add(pq)
                for event in trame.evenements.all():
                    source_doc_set.add(event)
                for photo_doc in trame.photo_documents.all():
                    source_doc_set.add(photo_doc)
                    used_items_set.update(photo_doc.photos.all())

        # 3. Create global numbering maps (P-X, N-X, P-X.Y)
        def get_date(obj):
            dt = None
            if isinstance(obj, Email): dt = obj.date_sent
            elif isinstance(obj, PDFDocument): dt = obj.uploaded_at
            elif isinstance(obj, PhotoDocument): dt = obj.created_at
            elif isinstance(obj, Event): dt = obj.date
            if not dt: return None
            if isinstance(dt, date) and not isinstance(dt, datetime):
                dt = datetime.combine(dt, datetime.min.time())
            return timezone.make_aware(dt) if timezone.is_naive(dt) else dt

        sorted_source_docs = sorted([d for d in source_doc_set if get_date(d)], key=get_date)
        exhibit_map = {doc: f"P-{i+1}" for i, doc in enumerate(sorted_source_docs)}
        
        item_map = {}
        for doc, p_id in exhibit_map.items():
            items_in_doc = []
            if isinstance(doc, Email): items_in_doc = sorted(list(doc.quotes.all()), key=lambda x: x.pk)
            elif isinstance(doc, PDFDocument): items_in_doc = sorted(list(doc.quotes.all()), key=lambda x: x.pk)
            elif isinstance(doc, PhotoDocument): items_in_doc = sorted(list(doc.photos.all()), key=lambda x: x.pk)
            item_counter = 1
            for item in items_in_doc:
                if item in used_items_set:
                    item_map[item] = f"{p_id}.{item_counter}"
                    item_counter += 1

        sorted_trames = sorted(list(all_trames_set), key=lambda t: t.pk)
        trame_map = {trame: f"N-{i+1}" for i, trame in enumerate(sorted_trames)}

        # 4. Build the hierarchical structure, grouped by parent document
        data_by_document = []
        main_documents = DocumentNode.objects.filter(depth=2, node_type='document').order_by('path')
        doc_counter = 0

        for doc_node in main_documents:
            claims_in_doc = [n for n in all_perjury_nodes if n.path.startswith(doc_node.path)]
            if not claims_in_doc:
                continue

            doc_counter += 1
            doc_id = f"C-{doc_counter}"
            paragraph_number_map = self._get_paragraph_numbering_map(doc_node)

            doc_data = {'document': doc_node, 'doc_id': doc_id, 'claims': []}
            for claim_node in claims_in_doc:
                para_num = paragraph_number_map.get(claim_node.pk)
                claim_id = f"{doc_id}-{para_num}" if para_num else doc_id

                node_data = self._get_structured_data_for_node(
                    claim_node, trame_map, exhibit_map, item_map, sorted_source_docs, sorted_trames
                )
                node_data['claim_id'] = claim_id
                doc_data['claims'].append(node_data)
            
            data_by_document.append(doc_data)

        # 5. Prepare lists for the 'exhibits' section of the template
        exhibits_list = []
        for doc in sorted_source_docs:
            p_id = exhibit_map.get(doc)
            if not p_id: continue
            type_fr, title = '', ''
            if isinstance(doc, Email): type_fr, title = 'Courriel', doc.subject
            elif isinstance(doc, PDFDocument): type_fr, title = 'Document PDF', doc.title
            elif isinstance(doc, PhotoDocument): type_fr, title = 'Document Photo', doc.title
            elif isinstance(doc, Event): type_fr, title = 'Événement', f"Événement du {get_date(doc).strftime('%Y-%m-%d')}"
            exhibits_list.append({'main_id': p_id, 'type_fr': type_fr, 'title': title, 'date': get_date(doc)})

        narratives_list = [{'main_id': trame_map.get(t), 'title': t.titre, 'content': t.resume} for t in sorted_trames if trame_map.get(t)]

        context['data_by_document'] = data_by_document
        context['exhibits'] = exhibits_list
        context['narratives'] = narratives_list
        context['item_map'] = item_map
        context['trame_map'] = trame_map
        return context

    def _get_structured_data_for_node(self, node, trame_map, exhibit_map, item_map, sorted_source_docs, sorted_trames):
        node_data = {'node': node, 'trames': []}
        trames_for_node = sorted(node.trames_narratives.all(), key=lambda t: sorted_trames.index(t) if t in sorted_trames else -1)

        for trame in trames_for_node:
            evidence_for_trame = []
            evidence_for_trame.extend(trame.citations_courriel.all())
            evidence_for_trame.extend(trame.citations_pdf.all())
            evidence_for_trame.extend(trame.evenements.all())
            evidence_for_trame.extend(trame.photo_documents.all())

            trame_data = {
                'trame': trame,
                'id': trame_map.get(trame),
                'evidence': self.process_evidence_for_node(
                    evidence_for_trame, exhibit_map, item_map, sorted_source_docs
                )
            }
            node_data['trames'].append(trame_data)
        return node_data

    def process_evidence_for_node(self, raw_evidence, exhibit_map, item_map, sorted_source_docs):
        processed = []
        def get_source_doc(obj):
            if isinstance(obj, EmailQuote): return obj.email
            if isinstance(obj, PDFQuote): return obj.pdf_document
            if isinstance(obj, (Event, PhotoDocument)): return obj
            return None
        def get_sort_key(obj):
            source = get_source_doc(obj)
            return sorted_source_docs.index(source) if source in sorted_source_docs else -1
        
        for obj in sorted(raw_evidence, key=get_sort_key):
            data = {'obj': obj}
            source_doc = get_source_doc(obj)
            data['p_id'] = exhibit_map.get(source_doc, '')

            if isinstance(obj, EmailQuote):
                data.update({
                    'type': 'EmailQuote',
                    'short_type': 'Email',
                    'item_id': item_map.get(obj),
                    'content': obj.quote_text,
                    'source_title': source_doc.subject,
                    'date': source_doc.date_sent,
                    'detail_url': source_doc.get_absolute_url() # Add detail URL
                })
            elif isinstance(obj, PDFQuote):
                data.update({
                    'type': 'PDFQuote',
                    'short_type': 'PDF',
                    'item_id': item_map.get(obj),
                    'content': obj.quote_text,
                    'source_title': source_doc.title,
                    'date': source_doc.uploaded_at,
                    'detail_url': source_doc.get_absolute_url() # Add detail URL
                })
            elif isinstance(obj, Event):
                data.update({'type': 'Event', 'short_type': 'Événement', 'item_id': None, 'content': obj.explanation, 'source_title': f"Événement du {obj.date.strftime('%Y-%m-%d')}", 'date': obj.date})
            elif isinstance(obj, PhotoDocument):
                data.update({'type': 'PhotoDocument', 'short_type': 'Photo', 'item_id': None, 'content': obj.description, 'source_title': obj.title, 'date': obj.created_at})
                data['photos'] = [{'obj': p, 'item_id': item_map.get(p)} for p in sorted(list(obj.photos.all()), key=lambda p: p.pk) if p in item_map]
            
            processed.append(data)
        return processed

    def get_queryset(self):
        return DocumentNode.objects.none()
