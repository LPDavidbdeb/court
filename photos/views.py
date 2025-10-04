import os
import sys
import json
from django.db import transaction
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
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from django.utils import timezone
from itertools import groupby
from datetime import datetime, timedelta

from .models import Photo, PhotoType
from .forms import PhotoForm, PhotoProcessingForm
from .management.commands.process_photos import Command as ProcessPhotosCommand
from events.models import Event  # MODIFIED
from .services import PhotoProcessingService

# ==============================================================================
# Photo Processing and Interactive Import
# ==============================================================================
def photo_processing_view(request):
    """
    Handles the UI and streaming for the photo processing task.
    """
    if request.method == 'GET':
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
        
        else:
            form = PhotoProcessingForm()
            return render(request, 'photos/photo_processing_form.html', {'form': form})

    if request.method == 'POST':
        form = PhotoProcessingForm(request.POST)
        if form.is_valid():
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
            return render(request, 'photos/photo_processing_form.html', {'form': form})

@csrf_exempt
@require_POST
def import_single_photo_view(request):
    """
    Imports a single photo, processes it, and intelligently clusters it 
    with existing Events based on timestamp proximity.
    """
    try:
        data = json.loads(request.body)
        file_path = data.get('file_path')
        datetime_str = data.get('datetime_original')
        photo_type_id = data.get('photo_type_id')

        if not file_path or not datetime_str:
            return JsonResponse({'status': 'error', 'message': 'File path and datetime are required.'}, status=400)

        if not os.path.exists(file_path):
            return JsonResponse({'status': 'error', 'message': 'File does not exist on the server.'}, status=400)

        dt_obj = datetime.fromisoformat(datetime_str)
        dt_aware = timezone.make_aware(dt_obj)

        # --- Validation Checks ---
        dt_truncated = dt_aware.replace(second=0, microsecond=0)
        if Photo.objects.filter(datetime_original__year=dt_truncated.year,
                                datetime_original__month=dt_truncated.month,
                                datetime_original__day=dt_truncated.day,
                                datetime_original__hour=dt_truncated.hour,
                                datetime_original__minute=dt_truncated.minute).exists():
            return JsonResponse({
                'status': 'error',
                'message': f'A photo with the exact timestamp (to the minute) already exists.'
            }, status=400)
        
        if Photo.objects.filter(file_path=file_path).exists():
            return JsonResponse({
                'status': 'error',
                'message': f'A photo with this file path already exists.'
            }, status=400)

        photo_type = PhotoType.objects.get(pk=photo_type_id) if photo_type_id else None

        with transaction.atomic():
            # --- Photo Creation ---
            service = PhotoProcessingService()
            photo = service.create_and_process_photo(
                source_path=file_path,
                datetime_original=dt_aware,
                photo_type=photo_type
            )
            if not photo:
                return JsonResponse({'status': 'error', 'message': 'Photo processing failed.'}, status=500)

            # --- Smart Clustering Logic ---
            event_break_threshold = timedelta(hours=2)
            evidence_date = dt_aware.date()
            
            potential_clusters = Event.objects.filter(date=evidence_date) # MODIFIED
            closest_cluster = None
            min_delta = event_break_threshold

            for cluster in potential_clusters:
                if not cluster.linked_photos.exists():
                    continue
                
                first_photo = cluster.linked_photos.order_by('datetime_original').first()
                last_photo = cluster.linked_photos.order_by('-datetime_original').first()
                
                delta_to_start = abs(dt_aware - first_photo.datetime_original)
                delta_to_end = abs(dt_aware - last_photo.datetime_original)
                
                # Check if the new photo is within the threshold of the cluster's bounds
                if delta_to_start < event_break_threshold or delta_to_end < event_break_threshold:
                    # Find the smaller of the two deltas to see how close it is
                    effective_delta = min(delta_to_start, delta_to_end)
                    if effective_delta < min_delta:
                        min_delta = effective_delta
                        closest_cluster = cluster

            if closest_cluster:
                # Add to the found cluster
                evidence = closest_cluster
                evidence.linked_photos.add(photo)
            else:
                # Create a new cluster
                evidence = Event.objects.create(date=evidence_date) # MODIFIED
                evidence.linked_photos.add(photo)

            # --- Update Explanation ---
            all_photos = evidence.linked_photos.order_by('datetime_original')
            start_time = all_photos.first().datetime_original
            end_time = all_photos.last().datetime_original

            # Preserve existing explanation if it exists, otherwise create a new one
            base_explanation = evidence.explanation or ""
            time_range_str = f"On {evidence_date.strftime('%Y-%m-%d')} between {start_time.strftime('%H:%M')} and {end_time.strftime('%H:%M')}: "
            
            if "between" in base_explanation and "On" in base_explanation:
                # Find the colon and replace everything before it
                parts = base_explanation.split(':', 1)
                evidence.explanation = time_range_str + (parts[1].lstrip() if len(parts) > 1 else '')
            else:
                evidence.explanation = time_range_str + base_explanation

            evidence.save()

            return JsonResponse({
                'status': 'success',
                'message': f'Imported and clustered {photo.file_name}.',
                'photo_id': photo.pk,
                'evidence_id': evidence.pk
            })

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


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
