from django.contrib import admin

from .models import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    """
    Les citations de courriel, des deux régimes.

    L'ancien système ne voit que l'ancien régime ; l'administration voit tout,
    pour qu'une citation du nouveau régime reste diagnosticable. Le régime ne
    s'y change pas : une citation du nouveau régime naît par son propre point
    d'entrée, pas par une bascule ici.
    """
    list_display = ('pk', 'regime', 'email', 'quote_text', 'updated_at')
    list_filter = ('regime',)
    search_fields = ('quote_text',)
    raw_id_fields = ('email',)
    readonly_fields = ('regime', 'created_at', 'updated_at')
    exclude = ('embedding',)

    def get_queryset(self, request):
        return Quote.all_objects.select_related('email')
