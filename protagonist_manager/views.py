from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db import transaction
from django.urls import reverse_lazy

from .models import Protagonist
from document_manager.models import Document
from email_manager.models import Email
from pdf_manager.models import PDFDocument
from photos.models import PhotoDocument

class ProtagonistListView(ListView):
    model = Protagonist
    template_name = 'protagonist_manager/protagonist_list.html'
    context_object_name = 'protagonists'

class ProtagonistDetailView(DetailView):
    model = Protagonist
    template_name = 'protagonist_manager/protagonist_detail.html'
    context_object_name = 'protagonist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all other protagonists to be candidates for merging
        context['merge_candidates'] = Protagonist.objects.exclude(pk=self.object.pk)
        return context

class MergeProtagonistView(View):
    def post(self, request, *args, **kwargs):
        original_pk = request.POST.get('original_protagonist')
        duplicate_pk = request.POST.get('duplicate_protagonist')

        if not original_pk or not duplicate_pk:
            messages.error(request, "You must select a protagonist to merge.")
            # We don't know which detail page to return to, so we go to the list view
            return redirect('protagonist_manager:protagonist_list')

        original = get_object_or_404(Protagonist, pk=original_pk)
        duplicate = get_object_or_404(Protagonist, pk=duplicate_pk)

        try:
            with transaction.atomic():
                # 1. Re-assign Document authors
                Document.objects.filter(author=duplicate).update(author=original)

                # 2. Re-assign Email senders
                Email.objects.filter(sender_protagonist=duplicate).update(sender_protagonist=original)

                # 3. Re-assign Email recipients (ManyToManyField)
                for email in Email.objects.filter(recipient_protagonists=duplicate):
                    email.recipient_protagonists.add(original)
                    email.recipient_protagonists.remove(duplicate)

                # 4. Re-assign ProtagonistEmail objects
                duplicate.emails.all().update(protagonist=original)

                # 5. Re-assign PDFDocument authors
                PDFDocument.objects.filter(author=duplicate).update(author=original)
                
                # 6. Re-assign PhotoDocument authors
                PhotoDocument.objects.filter(author=duplicate).update(author=original)

                # 7. Delete the duplicate protagonist
                duplicate.delete()

                messages.success(request, f"Successfully merged '{duplicate.get_full_name()}' into '{original.get_full_name()}'.")

        except Exception as e:
            messages.error(request, f"An error occurred during the merge: {e}")

        return redirect('protagonist_manager:protagonist_detail', pk=original.pk)
