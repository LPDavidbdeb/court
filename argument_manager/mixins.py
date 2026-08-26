from django.contrib import messages
from django.db import transaction


class EvidenceDeleteMixin:
    """
    Deletes a piece of evidence, and with it the narratives it alone held up.

    Mix into a DeleteView whose model is reachable from TrameNarrative through
    one of its evidence relations — an email quote, a PDF quote, a photo, an
    event, a chat sequence — that is, anything carrying a `trames_narratives`
    reverse accessor.

    Removing the last piece of evidence from a narrative leaves a title and a
    résumé asserting something nothing supports; such a narrative is deleted
    along with the evidence rather than left standing empty. Narratives that
    keep any other evidence, of any kind, simply lose this one.

    The narratives are read before the delete and re-tested at that moment
    rather than trusted from whatever the page showed, which may be minutes
    old; the whole thing runs in one transaction, so a narrative is never
    orphaned by a delete that then fails.
    """

    # Shown when nothing else was affected. Override per model.
    deleted_message = "The quote has been deleted successfully."

    def form_valid(self, form):
        evidence = self.object
        orphaned = [
            trame for trame in evidence.trames_narratives.all()
            if trame.is_supported_only_by(evidence)
        ]
        titles = [trame.titre for trame in orphaned]

        with transaction.atomic():
            response = super().form_valid(form)
            for trame in orphaned:
                trame.delete()

        messages.success(self.request, self.get_deleted_message(titles))
        return response

    def get_deleted_message(self, deleted_narrative_titles):
        if not deleted_narrative_titles:
            return self.deleted_message
        listed = ', '.join(f'"{title}"' for title in deleted_narrative_titles)
        return (
            f"{self.deleted_message.rstrip('.')}, along with "
            f"{len(deleted_narrative_titles)} narrative(s) it was the only "
            f"evidence of: {listed}."
        )
