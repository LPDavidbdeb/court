"""
Crée les trois schémas de niveaux tirés des documents existants, et les rattache.

    python manage.py init_schemas_niveaux --dry-run
    python manage.py init_schemas_niveaux

Les schémas DÉCRIVENT ce que les documents sont déjà. Aucun arbre n'est modifié :
rattacher un schéma ne fait qu'énoncer comment lire les profondeurs. Les écarts
entre ce que le schéma affirme et ce que l'arbre contient sont le travail de
`verifier_schemas`, qui rapporte sans corriger.
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from document_manager.models import (
    Document, FormatNumero, Niveau, PorteeNumero, RoleNiveau, SchemaNiveaux,
)

R, F, P = RoleNiveau, FormatNumero, PorteeNumero

SCHEMAS = {
    "Acte de procédure assermenté": {
        "description":
            "Requête, dénonciation, déclaration assermentée. Les paragraphes sont "
            "numérotés en continu sur tout l'acte, et c'est par ce numéro qu'ils "
            "sont cités. Le numéro n'est pas stocké : il EST la position du nœud "
            "parmi ses pairs de profondeur 2.",
        "niveaux": [
            (1, R.RACINE, F.AUCUN, P.AUCUNE, "Titre de l'acte"),
            (2, R.PARAGRAPHE, F.DECIMAL, P.DOCUMENT, "Paragraphe numéroté"),
            (3, R.SOUS_ITEM, F.LETTRE_MIN, P.PARENT, "Sous-item — a), b), c)"),
            (4, R.ENUMERATION, F.AUCUN, P.AUCUNE, "Élément d'énumération"),
        ],
        "documents": [1, 2, 3],
    },
    "Correspondance reproduite": {
        "description":
            "Courriel ou échange reproduit. Aucun niveau n'est numéroté : un "
            "courriel n'a pas de paragraphes cotés et n'est jamais cité par numéro "
            "de paragraphe. L'arbre n'encode qu'une imbrication rhétorique. Ce "
            "schéma existe pour dire explicitement qu'il n'y a rien à numéroter — "
            "sans lui, on serait tenté d'appliquer la règle des actes.",
        "niveaux": [
            (1, R.RACINE, F.AUCUN, P.AUCUNE, "Objet du courriel"),
            (2, R.LIBRE, F.AUCUN, P.AUCUNE, "Passage"),
            (3, R.LIBRE, F.AUCUN, P.AUCUNE, "Passage imbriqué"),
            (4, R.LIBRE, F.AUCUN, P.AUCUNE, "Passage imbriqué"),
            (5, R.LIBRE, F.AUCUN, P.AUCUNE, "Passage imbriqué"),
        ],
        "documents": [4],
    },
    "Demande introductive normalisée": {
        "description":
            "Acte produit dont l'arbre est régularisé : tout paragraphe vit à la "
            "profondeur 6, sans exception, les niveaux absents étant comblés par "
            "des nœuds transparents (content_type NULL). Le rôle se déduit donc de "
            "la seule profondeur, et la numérotation continue est un parcours de "
            "l'arbre — jamais un compteur stocké.",
        "niveaux": [
            (1, R.RACINE, F.AUCUN, P.AUCUNE, "Racine"),
            (2, R.SECTION, F.ROMAIN_MAJ, P.DOCUMENT, "§ I, § II, …"),
            (3, R.SOUS_SECTION, F.LETTRE_MAJ, P.PARENT, "A., B., C."),
            (4, R.THEME, F.AUCUN, P.AUCUNE, "Thème"),
            (5, R.SOUS_THEME, F.AUCUN, P.AUCUNE, "Sous-thème"),
            (6, R.PARAGRAPHE, F.DECIMAL, P.DOCUMENT, "Paragraphe numéroté"),
        ],
        "documents": [9],
    },
}


class Command(BaseCommand):
    help = "Crée les schémas de niveaux et les rattache aux documents."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        dry = options["dry_run"]

        for nom, spec in SCHEMAS.items():
            self.stdout.write("")
            self.stdout.write(self.style.MIGRATE_HEADING(nom))
            for prof, role, fmt, portee, libelle in spec["niveaux"]:
                num = "—" if fmt == F.AUCUN else f"{fmt} / {portee}"
                self.stdout.write(f"    profondeur {prof} : {role:<13} {num:<24} {libelle}")
            cibles = []
            for pk in spec["documents"]:
                d = Document.objects.filter(pk=pk).first()
                cibles.append(f"doc {pk} « {d.title[:40]} »" if d
                              else f"doc {pk} INTROUVABLE")
            self.stdout.write(f"    rattaché à : {'; '.join(cibles)}")

        sans = Document.objects.exclude(
            pk__in=[pk for s in SCHEMAS.values() for pk in s["documents"]])
        if sans.exists():
            self.stdout.write("")
            self.stdout.write(self.style.WARNING(
                "  Documents laissés SANS schéma (volontairement) :"))
            for d in sans:
                self.stdout.write(f"    doc {d.pk} [{d.source_type}] « {d.title[:46]} »")
            self.stdout.write("    Un document sans schéma reste stockable ; il n'est "
                              "simplement pas numérotable.")

        if dry:
            self.stdout.write("")
            self.stdout.write("--dry-run : rien n'a été écrit.")
            return

        with transaction.atomic():
            for nom, spec in SCHEMAS.items():
                schema, _ = SchemaNiveaux.objects.update_or_create(
                    nom=nom, defaults={"description": spec["description"]})
                schema.niveaux.all().delete()
                Niveau.objects.bulk_create([
                    Niveau(schema=schema, profondeur=p, role=r,
                           format_numero=f, portee=po, libelle=lib)
                    for p, r, f, po, lib in spec["niveaux"]
                ])
                Document.objects.filter(pk__in=spec["documents"]).update(schema=schema)

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"{SchemaNiveaux.objects.count()} schémas, "
            f"{Niveau.objects.count()} niveaux, "
            f"{Document.objects.exclude(schema=None).count()} documents rattachés."))
