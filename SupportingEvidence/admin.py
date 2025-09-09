from django.contrib import admin
from .models import SupportingEvidence

@admin.register(SupportingEvidence)
class SupportingEvidenceAdmin(admin.ModelAdmin):
    """
    Admin view for the SupportingEvidence model.
    """
    # UPDATED: Replaced 'start_date' with the new 'date' field
    list_display = ('__str__', 'date', 'parent', 'allegation')
    list_filter = ('allegation', 'parent', 'date')
    search_fields = ('explanation', 'email_quote')
    
    raw_id_fields = ('parent', 'allegation', 'linked_email')

    fieldsets = (
        ('Core Information', {
            'fields': ('parent', 'allegation', 'explanation')
        }),
        ('Date and Time', {
            'fields': ('date',)
        }),
        ('Linked Evidence', {
            'fields': ('linked_photos', 'linked_email', 'email_quote')
        }),
    )

    filter_horizontal = ('linked_photos',)
