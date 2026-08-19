"""
Traduit la cotation déposée en une cotation chronologique.

    python manage.py traduire_cotes
    python manage.py traduire_cotes --limite 40

Le bordereau du dépôt est IMMUABLE : il a été déposé. Ce qui est figé, c'est la
correspondance entre une pièce (modèle + PK) et la cote qu'elle a reçue. Cette
table sert donc de traducteur : elle donne la pièce, la pièce donne sa date, la
date donne le rang, et le rang donne la nouvelle cote. Rien n'est stocké — la
nouvelle cotation est une FONCTION du contenu, recalculable à volonté.

Le tri réutilise `case_manager.exhibit_service.get_datetime_for_sorting`, le
moteur déjà employé par `rebuild_produced_exhibits` (la vue
« generate-production »), plutôt qu'une logique parallèle qui divergerait :
`ExhibitableMixin.get_exhibit_date()` en premier, normalisation du fuseau,
repli sur `created_at`, cas particulier des séquences de clavardage.

Le tri porte sur l'horodatage complet. Un courriel de 9 h 14 se range donc après
un document daté du même jour sans heure, celui-ci valant minuit.
"""
import datetime

from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from case_manager.cotation_service import (PLANCHER, cotation_chronologique,
                                            horodatage)
from case_manager.models import BordereauDepotJuillet

# Le plancher, la fonction d'horodatage et l'ordre de tri vivent dans
# `case_manager.cotation_service`, partagés avec la vue du tableau des cotes.
# Deux implémentations parallèles finiraient par diverger, et le dossier
# aurait alors deux ordres différents pour la même preuve.


class Command(BaseCommand):
    help = "Traduit les cotes déposées en cotes chronologiques."

    def add_arguments(self, parser):
        parser.add_argument("--limite", type=int, default=20,
                            help="nombre de lignes montrées dans l'extrait")
        parser.add_argument("--liasse", default=None,
                            help="détailler la dispersion d'une cote racine, ex. P-43")
        parser.add_argument("--plancher", type=int, default=PLANCHER.year,
                            help="année sous laquelle un horodatage est tenu pour absent")

    def handle(self, *args, **options):
        # L'ordre vient du service, partagé avec la vue. La commande ne
        # recalcule rien : elle met en forme.
        traduction = cotation_chronologique(plancher_annee=options["plancher"])
        entrees   = [t for t in traduction if t[3] == 'datee']
        sans_date = [t for t in traduction if t[3] == 'a_dater']
        atemporelles = [t for t in traduction if t[3] == 'atemporelle']

        inchangees = sum(1 for i, e, _, _g in traduction if e.cote == f"P-{i}")
        ajoutees = sum(1 for _r, e, _d, _g in traduction if e.cote is None)
        self.stdout.write("=" * 76)
        self.stdout.write("TRADUCTION — cote déposée → cote chronologique")
        self.stdout.write("=" * 76)
        self.stdout.write(f"  pièces traduites : {len(traduction)}")
        self.stdout.write(f"    cote inchangée : {inchangees}")
        self.stdout.write(f"    cote modifiée  : {len(traduction) - inchangees}")
        self.stdout.write(f"  dont versées après le dépôt (sans cote de juillet) : "
                          f"{ajoutees}")
        if sans_date:
            self.stdout.write("")
            self.stdout.write(self.style.WARNING(
                f"  À DATER — {len(sans_date)} pièce(s) rangée(s) en fin de tableau"))
            self.stdout.write("    Elles reprendront leur place d'elles-mêmes une fois "
                              "la date saisie : rien n'est stocké, il suffit de relancer.")
            for n, (rang, e, _d, _g) in enumerate(sans_date):
                origine = e.cote or "(non déposée)"
                self.stdout.write(f"      {origine:<14} → P-{rang:<6} {e.description[:44]}")

        if atemporelles:
            self.stdout.write("")
            self.stdout.write(f"  ATEMPORELLES — {len(atemporelles)} pièce(s), "
                              f"rangée(s) en fin de façon permanente")
            self.stdout.write("    Sans date PAR NATURE : rien à corriger.")
            for n, (rang, e, _d, _g) in enumerate(atemporelles):
                origine = e.cote or "(non déposée)"
                self.stdout.write(f"      {origine:<14} → P-{rang:<6} {e.description[:50]}")

        self.stdout.write("")
        self.stdout.write(f"  EXTRAIT — les {options['limite']} premières, "
                          f"par ordre chronologique")
        self.stdout.write(f"    {'nouvelle':<10}{'déposée':<11}{'horodatage':<18}"
                          f"{'type':<13}description")
        for i, e, d, _g in traduction[:options["limite"]]:
            ds = f"{d:%Y-%m-%d %H:%M}" if d else "—"
            origine = e.cote or "(ajoutée)"
            self.stdout.write(f"    P-{i:<8}{origine:<12}{ds:<18}"
                              f"{e.source_type:<15}{e.description[:38]}")

        if options["liasse"]:
            racine = options["liasse"]
            self.stdout.write("")
            self.stdout.write(f"  DISPERSION DE {racine}")
            for i, e, d, _g in traduction:
                if e.cote_racine == racine:
                    self.stdout.write(f"    {e.cote:<11} → P-{i:<7} {d:%Y-%m-%d %H:%M}")

        self.stdout.write("")
        self.stdout.write("Rien n'a été écrit : la nouvelle cotation est une fonction, "
                          "pas une donnée.")
