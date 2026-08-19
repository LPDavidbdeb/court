"""
Persiste le lien paragraphe ↔ pièce de la demande déposée le 24 juillet 2026.

    python manage.py persister_appuis_depot                # constat, n'écrit rien
    python manage.py persister_appuis_depot --ecrire
    python manage.py persister_appuis_depot --document 9 --limite 40

La demande allègue des faits ; chaque fait occupe un paragraphe et se trouve
appuyé par 0, 1 ou N pièces du bordereau, organisées en liasses lorsqu'elles
sont nombreuses. Cette relation est écrite dans le texte — « tel qu'il appert
des pièces P-49.1, P-49.2 et P-72 » — et nulle part ailleurs. La commande la
fait entrer en base, dans `AppuiDepotJuillet`.

PÉRIMÈTRE STRICT : la demande de juillet et son bordereau. La commande ne lit
ni n'écrit aucun `Fait`, aucun `Axe`, aucun `AppuiFait` — ces modèles portent
une exploration d'une présentation future, qui n'existait pas au dépôt. Un état
figé et un chantier ouvert n'ont pas à se rencontrer dans une même table.

RIEN N'EST ÉCRASÉ, rien n'est sauté. Un appui déjà présent est laissé tel quel,
note comprise ; la commande est donc rejouable et une correction manuelle
survit à la relance.

LES NUMÉROS SONT DONNÉS EN DOUBLE — « § 44 (dépôt 28) ». Le document en porte
deux, celui du schéma et celui du dépôt, et plus de deux cents paragraphes
diffèrent entre les deux ; n'en imprimer qu'un désigne un autre paragraphe que
celui que l'écran montre.
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from case_manager.appui_depot_service import lecture_prose
from case_manager.models import AppuiDepotJuillet
from document_manager.models import Document
from document_manager.numerotation import index_numeros


class Command(BaseCommand):
    help = ("Persiste les appuis documentaires cités dans la demande déposée "
            "en juillet.")

    def add_arguments(self, parser):
        parser.add_argument("--document", type=int, default=9,
                            help="pk de la demande déposée")
        parser.add_argument("--ecrire", action="store_true",
                            help="écrire en base ; sans ce drapeau, simple constat")
        parser.add_argument("--limite", type=int, default=25)

    def handle(self, *args, **options):
        doc = Document.objects.get(pk=options["document"])
        ecrire = options["ecrire"]
        numeros = index_numeros(doc)

        lecture = lecture_prose(doc.pk)
        existants = {(a.statement_id, a.entree_id)
                     for a in AppuiDepotJuillet.objects.all()}

        crees = deja = 0
        expansions = 0
        inconnues = []
        detail = []

        with transaction.atomic():
            for node, stmt, appuis, cotes_inconnues in lecture:
                libelle = numeros.get(stmt.pk, node.item or "?")
                if cotes_inconnues:
                    inconnues.append((libelle, cotes_inconnues))

                ajouts = 0
                for entree, cote, via_liasse in appuis:
                    if (stmt.pk, entree.pk) in existants:
                        deja += 1
                        continue
                    ajouts += 1
                    crees += 1
                    if via_liasse:
                        expansions += 1
                    if ecrire:
                        AppuiDepotJuillet.objects.create(
                            statement=stmt, entree=entree,
                            cote_citee=cote, via_liasse=via_liasse,
                        )
                if appuis:
                    detail.append((libelle, ajouts, len(appuis)))

            if not ecrire:
                transaction.set_rollback(True)

        w = self.stdout.write
        w("=" * 76)
        w(f"APPUIS DU DÉPÔT — {doc.title[:54]}")
        w("=" * 76)
        w(f"  paragraphes invoquant au moins une pièce : {len(lecture)}")
        w(f"  appuis à créer{'  (créés)' if ecrire else ''}                : {crees}")
        w(f"    dont issus du développement d'une liasse : {expansions}")
        w(f"  appuis déjà en base, inchangés           : {deja}")

        if inconnues:
            w("")
            w(self.style.ERROR(
                f"  COTES FANTÔMES — {len(inconnues)} paragraphe(s) citent une cote "
                f"absente du bordereau"))
            w("    À corriger dans le TEXTE : la prose est ce que le tribunal lit.")
            for libelle, cotes in inconnues[:options["limite"]]:
                w(f"      § {libelle:<16} {', '.join(cotes)}")

        if detail:
            w("")
            w(f"  EXTRAIT — {min(len(detail), options['limite'])} premiers paragraphes")
            for libelle, ajouts, total in detail[:options["limite"]]:
                w(f"      § {libelle:<16} +{ajouts} appui(s) / {total} pièce(s) invoquée(s)")

        w("")
        if ecrire:
            w(self.style.SUCCESS("  ÉCRIT."))
        else:
            w(self.style.WARNING("  CONSTAT SEULEMENT — rien n'a été écrit. "
                                 "Relancer avec --ecrire."))
