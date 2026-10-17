from django.contrib import admin
from .models import PDFDocument, PDFDocumentType, Quote

@admin.register(PDFDocumentType)
class PDFDocumentTypeAdmin(admin.ModelAdmin):
    """
    Admin view for PDF Document Types.
    """
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(PDFDocument)
class PDFDocumentAdmin(admin.ModelAdmin):
    """
    Admin view for PDF Documents.
    """
    list_display = ('title', 'document_type', 'document_date', 'uploaded_at')
    list_filter = ('document_type', 'document_date')
    search_fields = ('title',)
    date_hierarchy = 'document_date'


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    """
    Les citations de PDF, des deux régimes.

    L'ancien système ne voit que l'ancien régime ; l'administration voit tout,
    pour qu'une citation du nouveau régime reste diagnosticable. Le régime ne
    s'y change pas : une citation du nouveau régime naît par son propre point
    d'entrée, pas par une bascule ici.
    """
    list_display = ('pk', 'regime', 'pdf_document', 'page_number', 'quote_text', 'updated_at')
    list_filter = ('regime',)
    search_fields = ('quote_text',)
    raw_id_fields = ('pdf_document',)
    readonly_fields = ('regime', 'created_at', 'updated_at')
    exclude = ('embedding',)

    def get_queryset(self, request):
        return Quote.all_objects.select_related('pdf_document')
