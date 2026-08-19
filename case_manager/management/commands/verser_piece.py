"""
Verse au registre une pièce qui n'était pas au dépôt du 24 juillet 2026.

    python manage.py verser_piece --dry-run
    python manage.py verser_piece

Ces pièces entrent dans `BordereauDepotJuillet` avec `cote = NULL`. Ajouter ces
lignes ne modifie AUCUNE correspondance existante : ce qui est immuable, c'est
l'association (modèle + pk) -> cote de juillet, et une pièce non déposée n'en a
jamais eu. Elle prendra en revanche son rang à sa date dans la cotation
chronologique, comme n'importe quelle autre.

Les pièces à verser sont déclarées ci-dessous, avec le motif de leur entrée —
quel axe les invoque et à quel titre. Le motif n'est pas décoratif : c'est ce
qui permet, plus tard, de savoir pourquoi une pièce sans cote de dépôt figure
au dossier.
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from case_manager.models import BordereauDepotJuillet
from events.models import Event
from pdf_manager.models import PDFDocument
from photos.models import PhotoDocument

A_VERSER = [
    (Event, 220,
     "Cours de danse d'Alexia, 16 décembre 2012 — le défendeur présent, 7 photos.",
     "Axe « Cours de danse », fait 7 : exécution concrète de la prise en charge."),
    (PhotoDocument, 15,
     "Adresse de l'école de danse Hugo Depot.",
     "Axe « Cours de danse », fait 2 : situe le déplacement qu'impose le cours "
     "du soir. Rôle CADRE."),
    (PDFDocument, 91,
     "Soccer Saint-Lambert — dates de début et de fin de session.",
     "Axe « Soccer été 2013 », fait 3 : structure de la saison. Rôle ILLUSTRATION "
     "— document de 2026, ne date pas de 2013."),
    (PDFDocument, 90,
     "Horaire du soccer Saint-Lambert — deux séances hebdomadaires.",
     "Axe « Soccer été 2013 », fait 3 : fréquence des séances. Rôle ILLUSTRATION."),
]


class Command(BaseCommand):
    help = "Verse au registre les pièces produites après le dépôt."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        lignes, deja, absents = [], [], []

        for modele, pk, description, motif in A_VERSER:
            obj = modele.objects.filter(pk=pk).first()
            if obj is None:
                absents.append(f"{modele.__name__} {pk}")
                continue
            ct = ContentType.objects.get_for_model(modele)
            existante = BordereauDepotJuillet.objects.filter(
                content_type=ct, object_id=pk).first()
            if existante:
                # Une pièce déjà au registre ne se verse pas deux fois — et si
                # elle porte une cote, c'est qu'elle ÉTAIT au dépôt : la verser
                # comme ajout serait une erreur de fait.
                deja.append((existante, obj))
                continue
            lignes.append((ct, obj, pk, description, motif))

        self.stdout.write("=" * 78)
        self.stdout.write("VERSEMENT AU REGISTRE — pièces sans cote de dépôt")
        self.stdout.write("=" * 78)
        for ct, obj, pk, description, motif in lignes:
            d = obj.get_exhibit_date() if hasattr(obj, "get_exhibit_date") else None
            ds = f"{d:%Y-%m-%d}" if d else "SANS DATE"
            self.stdout.write(f"  {ct.model}-{pk:<5} {ds:<12} {description[:52]}")
            self.stdout.write(f"       motif : {motif[:88]}")

        if deja:
            self.stdout.write("")
            self.stdout.write(self.style.WARNING("  DÉJÀ AU REGISTRE — non versées :"))
            for e, obj in deja:
                etat = f"cote {e.cote}" if e.cote else "déjà versée sans cote"
                self.stdout.write(f"    {e.content_type.model}-{e.object_id} — {etat}")

        if absents:
            raise CommandError("Pièces introuvables : " + ", ".join(absents))

        self.stdout.write("")
        self.stdout.write(f"  à verser : {len(lignes)}")

        if options["dry_run"]:
            self.stdout.write("")
            self.stdout.write("--dry-run : rien n'a été écrit.")
            return

        with transaction.atomic():
            for ct, obj, pk, description, motif in lignes:
                BordereauDepotJuillet.objects.create(
                    cote=None, cote_racine=None, rang=None, sous_rang=None,
                    content_type=ct, object_id=pk,
                    source_type=ct.model,
                    source_ref="", date_libelle="",
                    description=description,
                    resolu=True, note=f"Versée après le dépôt. {motif}",
                )

        total = BordereauDepotJuillet.objects.count()
        sans = BordereauDepotJuillet.objects.filter(cote__isnull=True).count()
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"{len(lignes)} pièce(s) versée(s). Registre : {total} lignes, "
            f"dont {total - sans} cotées au dépôt et {sans} versées depuis."))
