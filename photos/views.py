from django.shortcuts import render

# Create your views here.
# your_project_root/photos/email_manager_1.py

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
from .models import Photo

class PhotoListView(ListView):
    """
    Displays a list of all Photo instances.
    """
    model = Photo
    template_name = 'photos/photo_list.html'
    context_object_name = 'photos'
    paginate_by = 25 # Optional: Add pagination

class PhotoDetailView(DetailView):
    """
    Displays the details of a single Photo instance.
    """
    model = Photo
    template_name = 'photos/photo_detail.html'
    context_object_name = 'photo'

class PhotoCreateView(CreateView):
    """
    Allows creation of a new Photo instance.
    """
    model = Photo
    # Use '__all__' for now, but consider specifying fields explicitly later
    fields = '__all__'
    template_name = 'photos/photo_form.html'
    success_url = reverse_lazy('photos:list') # Redirect to photo list after creation

class PhotoUpdateView(UpdateView):
    """
    Allows updating an existing Photo instance.
    """
    model = Photo
    fields = '__all__' # Consider specifying fields explicitly
    template_name = 'photos/photo_form.html'
    success_url = reverse_lazy('photos:list') # Redirect to photo list after update

class PhotoDeleteView(DeleteView):
    """
    Allows deletion of a Photo instance.
    """
    model = Photo
    template_name = 'photos/photo_confirm_delete.html'
    context_object_name = 'photo'
    success_url = reverse_lazy('photos:list') # Redirect to photo list after deletion