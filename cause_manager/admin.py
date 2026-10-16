from django.contrib import admin

from .models import Cause, EtatCause, LienCause


class EtatCauseInline(admin.TabularInline):
    model = EtatCause
    fields = ['statut', 'date_effet', 'motif', 'consigne_le']
    readonly_fields = fields
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Cause)
class CauseAdmin(admin.ModelAdmin):
    list_display = ['numero_dossier', 'titre', 'tribunal', 'district_judiciaire', 'get_statut_display']
    search_fields = ['numero_dossier', 'titre', 'tribunal', 'district_judiciaire']
    list_filter = ['district_judiciaire']
    inlines = [EtatCauseInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('etats')


@admin.register(LienCause)
class LienCauseAdmin(admin.ModelAdmin):
    list_display = ['cause', 'cause_liee', 'description']
    autocomplete_fields = ['cause', 'cause_liee']
