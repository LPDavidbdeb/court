"""
Créer une citation du régime PHRASE par le point d'entrée applicatif normal.

    python manage.py create_phrase_quote --email 100 --start 0 --end 62 --derived-from 40 --dry-run
    python manage.py create_phrase_quote --email 100 --start 0 --end 62 --derived-from 40
    python manage.py create_phrase_quote --pdf 3 --start 812 --end 870 [--page 2]

Passe par `create_phrase_quote` (core.quote_regime) : bornes vérifiées sur le
texte de référence, empreintes calculées, `full_clean()`, garde de `save()`. Un
courriel est certifié dans le même geste ; un PDF ne l'est pas (la
certification d'un scan suit la lecture du scan : `certify_phrase_quote`).

`--dry-run` fait tout dans une transaction annulée : on voit la tranche, les
empreintes et la certification qui seraient enregistrées, sans rien écrire.

Plan : docs/modele_preuve/PLAN_REGIME_CITATIONS.md, § 4.
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.quote_regime import create_phrase_quote
from email_manager.models import Email
from email_manager.models import Quote as EmailQuote
from pdf_manager.models import PDFDocument
from pdf_manager.models import Quote as PDFQuote


class _Annulation(Exception):
    pass


class Command(BaseCommand):
    help = "Crée une citation PHRASE ancrée dans le texte de référence d'un courriel ou d'un PDF."

    def add_arguments(self, parser):
        source = parser.add_mutually_exclusive_group(required=True)
        source.add_argument("--email", type=int, help="PK du courriel source")
        source.add_argument("--pdf", type=int, help="PK du document PDF source")
        parser.add_argument("--start", type=int, required=True, help="borne de début, incluse")
        parser.add_argument("--end", type=int, required=True, help="borne de fin, exclue")
        parser.add_argument("--derived-from", type=int, help="PK de la citation de l'ancien régime dont elle procède")
        parser.add_argument("--page", type=int, help="page (PDF seulement), si le texte n'a pas de marque de page")
        parser.add_argument("--dry-run", action="store_true", help="tout vérifier dans une transaction annulée")

    def handle(self, *args, **o):
        if o["email"] is not None:
            source, modele = Email.objects.get(pk=o["email"]), EmailQuote
        else:
            source, modele = PDFDocument.objects.get(pk=o["pdf"]), PDFQuote
        antecedent = modele.all_objects.get(pk=o["derived_from"]) if o["derived_from"] is not None else None
        try:
            with transaction.atomic():
                citation = create_phrase_quote(source, o["start"], o["end"], derived_from=antecedent,
                                               page_number=o["page"])
                self._decrire(citation)
                if o["dry_run"]:
                    raise _Annulation
        except _Annulation:
            self.stdout.write("ESSAI À BLANC : transaction annulée, rien n'est enregistré")
            return
        except Exception as e:  # noqa: BLE001
            raise CommandError(f"citation refusée : {e}") from e
        self.stdout.write(f"CRÉÉE   {modele._meta.label} {citation.pk}")

    def _decrire(self, c):
        source = f"courriel {c.email_id}" if isinstance(c, EmailQuote) else f"PDF {c.pdf_document_id}, page {c.page_number}"
        self.stdout.write(f"source        : {source} ({len(c.reference_text)} caractères)")
        self.stdout.write(f"bornes        : [{c.start}, {c.end})")
        self.stdout.write(f"tranche       : {c.quote_text!r}")
        self.stdout.write(f"source_text_sha256    : {c.source_text_sha256}")
        self.stdout.write(f"anchored_text_sha256  : {c.anchored_text_sha256}")
        self.stdout.write(f"certified_text_sha256 : {c.certified_text_sha256 or '(vide)'}")
        self.stdout.write(f"derived_from  : {c.derived_from_id}")
        self.stdout.write(f"certification effective : {c.effective_certification}")
