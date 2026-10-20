"""
L'audit des citations du régime PHRASE.

    python manage.py audit_phrase_quotes

Relit toutes les citations PHRASE et signale celles qui violent un invariant
d'ancrage, ou dont la certification déclarée n'est plus effective. `update()` et
`bulk_create()` contournent la garde de `save()` : l'audit les rattrape. Il
détecte et sert à réparer ; ce qui protège, c'est la certification effective,
recalculée à chaque lecture (core.quote_regime).

Sortie : une ligne par citation, puis un bilan. Code non nul (CommandError) si
une citation est en défaut.

Plan : docs/modele_preuve/PLAN_REGIME_CITATIONS.md, § 4.
"""
from django.core.management.base import BaseCommand, CommandError

from email_manager.models import Quote as EmailQuote
from pdf_manager.models import Quote as PDFQuote


class Command(BaseCommand):
    help = "Signale les citations PHRASE dont un invariant est violé ou dont la certification n'est plus effective."

    def handle(self, *args, **options):
        total = defauts = 0
        for modele, relation in ((EmailQuote, "email"), (PDFQuote, "pdf_document")):
            for citation in modele.phrase_objects.select_related(relation).order_by("pk"):
                total += 1
                nom = f"{modele._meta.label} {citation.pk}"
                problemes = citation.audit_problems()
                if problemes:
                    defauts += 1
                    self.stdout.write(f"DÉFAUT  {nom} : {' ; '.join(problemes)}")
                elif citation.effective_certification:
                    self.stdout.write(f"OK      {nom} : certification effective")
                else:
                    self.stdout.write(f"OK      {nom} : ancrage valide, en attente de certification")
        self.stdout.write(f"{total} citation(s) PHRASE auditée(s), {defauts} en défaut")
        if defauts:
            raise CommandError(f"{defauts} citation(s) PHRASE en défaut")
