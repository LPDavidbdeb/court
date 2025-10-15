import json
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
)
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.db.models import Q

from ..models import Photo, PhotoDocument, PhotoType
from ..forms import PhotoDocumentForm, PhotoDocumentSingleUploadForm
from ..services import PhotoProcessingService
from protagonist_manager.forms import ProtagonistForm
from protagonist_manager.models import Protagonist


class PhotoDocumentSingleUploadView(FormView):
    template_name = 'photos/photodocument/single_upload.html'
    form_class = PhotoDocumentSingleUploadForm

    def form_valid(self, form):
        uploaded_file = form.cleaned_data['file']
        title = form.cleaned_data['title']
        description = form.cleaned_data.get('description', '')

        try:
            with transaction.atomic():
                doc_type, _ = PhotoType.objects.get_or_create(name='Document')
                service = PhotoProcessingService()
                photo = service.create_photo_from_upload(
                    uploaded_file=uploaded_file,
                    photo_type=doc_type
                )
                photo_document = PhotoDocument.objects.create(
                    title=title,
                    description=description
                )
                photo_document.photos.add(photo)

            messages.success(self.request, f"Successfully created document '{title}' from uploaded photo.")
            self.success_url = reverse('photos:document_detail', kwargs={'pk': photo_document.pk})
            return super().form_valid(form)

        except Exception as e:
            messages.error(self.request, f"An error occurred: {e}")
            return self.form_invalid(form)


class PhotoDocumentListView(ListView):
    model = PhotoDocument
    template_name = 'photos/photodocument/list.html'
    context_object_name = 'documents'


class PhotoDocumentDetailView(DetailView):
    model = PhotoDocument
    template_name = 'photos/photodocument/detail.html'
    context_object_name = 'document'


class PhotoDocumentCreateView(CreateView):
    model = PhotoDocument
    form_class = PhotoDocumentForm
    template_name = 'photos/photodocument/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protagonist_form'] = ProtagonistForm()
        try:
            document_photo_type = PhotoType.objects.get(name='Document')
            available_photos = Photo.objects.filter(photo_type=document_photo_type)
            context['available_photos_json'] = json.dumps(
                [{ 'id': photo.id, 'url': photo.file.url } for photo in available_photos]
            )
        except PhotoType.DoesNotExist:
            context['available_photos_json'] = '[]'
        return context

    def form_valid(self, form):
        messages.success(self.request, f"Photo document '{form.cleaned_data['title']}' created successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('photos:document_detail', kwargs={'pk': self.object.pk})


class PhotoDocumentUpdateView(UpdateView):
    model = PhotoDocument
    form_class = PhotoDocumentForm
    template_name = 'photos/photodocument/form.html'
    context_object_name = 'document'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protagonist_form'] = ProtagonistForm()
        try:
            document_photo_type = PhotoType.objects.get(name='Document')
            available_photos = Photo.objects.filter(photo_type=document_photo_type)
            context['available_photos_json'] = json.dumps(
                [{ 'id': photo.id, 'url': photo.file.url } for photo in available_photos]
            )
        except PhotoType.DoesNotExist:
            context['available_photos_json'] = '[]'
        return context

    def form_valid(self, form):
        messages.success(self.request, f"Photo document '{form.cleaned_data['title']}' updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('photos:document_detail', kwargs={'pk': self.object.pk})


class PhotoDocumentDeleteView(DeleteView):
    model = PhotoDocument
    template_name = 'photos/photodocument/confirm_delete.html'
    context_object_name = 'document'
    success_url = reverse_lazy('photos:document_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, f"Photo document '{self.object.title}' deleted successfully.")
        return super().post(request, *args, **kwargs)


# ==============================================================================
# AJAX Views
# ==============================================================================

def author_search_view(request):
    term = request.GET.get('term', '')
    protagonists = Protagonist.objects.filter(
        Q(first_name__icontains=term) | Q(last_name__icontains=term)
    )[:10]  # Limit results
    results = [
        {
            'id': p.id,
            'text': p.get_full_name()
        }
        for p in protagonists
    ]
    return JsonResponse(results, safe=False)

def add_protagonist_view(request):
    if request.method == 'POST':
        form = ProtagonistForm(request.POST)
        if form.is_valid():
            protagonist = form.save()
            return JsonResponse({'success': True, 'id': protagonist.id, 'name': protagonist.get_full_name()})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request'})
