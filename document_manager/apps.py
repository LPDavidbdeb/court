from django.apps import AppConfig


class DocumentManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'document_manager'

    def ready(self):
        # Les gardes de suppression et d'écriture doivent être enregistrées
        # AVANT la première opération, faute de quoi elles ne protègent rien —
        # et, pour les suppressions en lot, c'est l'enregistrement même du
        # receveur qui désactive le « fast delete ». Voir protection.py.
        from document_manager import protection  # noqa: F401
