import os
import sys
from django.shortcuts import redirect, render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST
from django.utils.dateparse import parse_date
from itertools import groupby
from datetime import datetime, timedelta
from django.http import StreamingHttpResponse

from .models import Photo, PhotoType
from .forms import PhotoForm, PhotoProcessingForm
from .management.commands.process_photos import Command as ProcessPhotosCommand

# ==============================================================================
# Photo Processing View (Corrected Handshake Logic)
# ==============================================================================
def photo_processing_view(request):
    """
    Handles the UI and streaming for the photo processing task.
    """
    # This is a GET request. It can either be the initial page load
    # or the EventSource connection.
    if request.method == 'GET':
        # Case 1: This is the EventSource connection, triggered by the JS
        if request.GET.get('start_stream') == 'true':
            mode = request.GET.get('mode')
            source_dir = request.GET.get('source_directory')
            photo_type_id = request.GET.get('photo_type_id')

            def event_stream():
                cmd = ProcessPhotosCommand()
                options = {
                    'mode': mode,
                    'source_directory': source_dir,
                    'photo_type_id': photo_type_id
                }
                yield from cmd.handle_streaming(**options)

            response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
            response['Cache-Control'] = 'no-cache'
            return response
        
        # Case 2: This is a standard initial page load
        else:
            form = PhotoProcessingForm()
            return render(request, 'photos/photo_processing_form.html', {'form': form})

    # This is a POST request from submitting the form
    if request.method == 'POST':
        form = PhotoProcessingForm(request.POST)
        if form.is_valid():
            # Re-render the page with the form data and a flag to start the JS
            cleaned_data = form.cleaned_data
            form_data_for_json = {
                'processing_mode': cleaned_data['processing_mode'],
                'source_directory': cleaned_data['source_directory'],
                'photo_type': cleaned_data['photo_type'].id if cleaned_data['photo_type'] else None
            }
            context = {
                'form': form,
                'form_data': form_data_for_json,
                'start_processing': True
            }
            return render(request, 'photos/photo_processing_form.html', context)
        else:
            # If form is not valid, re-render with errors
            return render(request, 'photos/photo_processing_form.html', {'form': form})


# ==============================================================================
# Timeline, Bulk Delete, and Standard Views
# ==============================================================================

def timeline_entry_view(request):
    latest_photo = Photo.objects.order_by('-datetime_original').first()
    if latest_photo and latest_photo.datetime_original:
        target_date = latest_photo.datetime_original.date()
        return redirect(reverse('photos:day_timeline', args=[target_date.year, target_date.month, target_date.day]))
    else:
        messages.info(request, "No photos with dates available to display in the timeline.")
        return redirect('photos:list')

class DayTimelineView(ListView):
    model = Photo
    template_name = 'photos/day_timeline.html'
    context_object_name = 'photos_in_day'

    def get_queryset(self):
        self.target_date = parse_date(f"{self.kwargs['year']}-{self.kwargs['month']}-{self.kwargs['day']}")
        return Photo.objects.filter(datetime_original__date=self.target_date).order_by('datetime_original')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photos_in_day = context['photos_in_day']
        grouped_photos = {k: list(g) for k, g in groupby(photos_in_day, key=lambda p: p.datetime_original)}
        next_day_start = self.target_date + timedelta(days=1)
        prev_day_start = self.target_date
        next_photo = Photo.objects.filter(datetime_original__gte=next_day_start).order_by('datetime_original').first()
        prev_photo = Photo.objects.filter(datetime_original__lt=prev_day_start).order_by('-datetime_original').first()
        context.update({
            'target_date': self.target_date,
            'grouped_photos': grouped_photos,
            'next_day': next_photo.datetime_original.date() if next_photo else None,
            'prev_day': prev_photo.datetime_original.date() if prev_photo else None,
        })
        return context

@require_POST
def bulk_delete_photos(request):
    photo_ids = request.POST.getlist('photo_ids')
    if not photo_ids:
        messages.warning(request, "You didn't select any photos to delete.")
        return redirect(request.META.get('HTTP_REFERER', reverse('photos:list')))
    Photo.objects.filter(pk__in=photo_ids).delete()
    messages.success(request, f"Successfully deleted {len(photo_ids)} photo(s).")
    return redirect(request.META.get('HTTP_REFERER', reverse('photos:list')))

class PhotoListView(ListView):
    model = Photo
    template_name = 'photos/photo_list.html'
    context_object_name = 'photos'
    paginate_by = 100

class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photos/photo_detail.html'
    context_object_name = 'photo'

class PhotoCreateView(CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photos/photo_form.html'
    success_url = reverse_lazy('photos:list')

class PhotoUpdateView(UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photos/photo_form.html'
    success_url = reverse_lazy('photos:list')

class PhotoDeleteView(DeleteView):
    model = Photo
    template_name = 'photos/photo_confirm_delete.html'
    context_object_name = 'photo'
    success_url = reverse_lazy('photos:list')
