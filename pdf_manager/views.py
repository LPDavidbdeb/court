import os
from collections import OrderedDict
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import PDFDocument, PDFDocumentType
from .forms import PDFDocumentForm

# ==============================================================================
# List and Create Views
# ==============================================================================

def pdf_document_list(request):
    """
    Displays a list of all uploaded PDF documents, grouped by type into tabs.
    """
    # 1. Get all document types to create the tabs
    doc_types = PDFDocumentType.objects.all()

    # 2. Get all documents, ordered by date
    all_documents = PDFDocument.objects.order_by('-document_date')

    # 3. Group documents by type
    grouped_documents = OrderedDict()
    for doc_type in doc_types:
        grouped_documents[doc_type] = []

    # Handle uncategorized documents
    uncategorized_documents = []

    for doc in all_documents:
        if doc.document_type:
            if doc.document_type in grouped_documents:
                grouped_documents[doc.document_type].append(doc)
        else:
            uncategorized_documents.append(doc)
    
    # Add uncategorized documents to the dictionary if they exist
    if uncategorized_documents:
        grouped_documents['Uncategorized'] = uncategorized_documents

    context = {
        'grouped_documents': grouped_documents,
    }
    return render(request, 'pdf_manager/pdf_list.html', context)

def upload_pdf_document(request):
    """
    Handles the upload of a new PDF document.
    """
    if request.method == 'POST':
        form = PDFDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"PDF document '{form.cleaned_data['title']}' uploaded successfully.")
            return redirect('pdf_manager:pdf_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PDFDocumentForm()
    
    return render(request, 'pdf_manager/upload_pdf.html', {'form': form})

# ==============================================================================
# Detail, Update, and Delete Views
# ==============================================================================

class PDFDocumentDetailView(DetailView):
    """
    Displays the details of a single PDF document.
    """
    model = PDFDocument
    template_name = 'pdf_manager/pdf_detail.html'
    context_object_name = 'document'

class PDFDocumentUpdateView(UpdateView):
    """
    Allows editing the details of a PDF document.
    """
    model = PDFDocument
    form_class = PDFDocumentForm
    template_name = 'pdf_manager/pdf_form.html'
    context_object_name = 'document'

    def get_success_url(self):
        messages.success(self.request, "PDF document details updated successfully.")
        return reverse_lazy('pdf_manager:pdf_detail', kwargs={'pk': self.object.pk})

class PDFDocumentDeleteView(DeleteView):
    """
    Handles the deletion of a PDF document and its associated file.
    """
    model = PDFDocument
    template_name = 'pdf_manager/pdf_confirm_delete.html'
    context_object_name = 'document'
    success_url = reverse_lazy('pdf_manager:pdf_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.file and os.path.isfile(self.object.file.path):
            os.remove(self.object.file.path)
        messages.success(request, f"PDF document '{self.object.title}' deleted successfully.")
        return super().post(request, *args, **kwargs)
