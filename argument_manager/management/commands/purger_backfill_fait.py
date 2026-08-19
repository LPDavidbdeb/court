"""
Retire du chantier des axes ce qui relevait du dépôt.

    python manage.py purger_backfill_fait            # constat, n'efface rien
    python manage.py purger_backfill_fait --ecrire

Un premier backfill a écrit la relation paragraphe ↔ pièce de la demande de
juillet dans `Fait` et `AppuiFait`. C'était le mauvais endroit : ces modèles
portent les axes, une exploration d'une présentation FUTURE de la preuve, qui
n'existait pas au dépôt. La relation vit désormais dans
`case_manager.AppuiDepotJuillet`, et il faut rendre au chantier son état
antérieur.

DEUX DÉGÂTS, DE FORMES OPPOSÉES, à défaire tous les deux :

  LES FAITS DE PROSE   un `Fait` créé par paragraphe, sans axe. Ils se
                       suppriment avec leurs appuis.
  LES GREFFES          des appuis du dépôt ajoutés à un `Fait` D'AXE existant,
                       lorsque le paragraphe n'en portait qu'un seul. Ceux-là
                       se retirent un à un : le `Fait` qui les porte est à vous
                       et doit rester intact.

La reconnaissance se fait par la note apposée à l'écriture. Un appui dont la
note a été modifiée à la main n'est donc PAS touché — la commande ne peut plus
affirmer qu'il vient d'elle, et le silence vaut mieux qu'une suppression.
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from argument_manager.models import AppuiFait, Fait

MARQUE = "Rattachement automatique depuis la prose"


class Command(BaseCommand):
    help = "Supprime les Fait/AppuiFait écrits par l'ancien backfill du dépôt."

    def add_arguments(self, parser):
        parser.add_argument("--ecrire", action="store_true",
                            help="effacer ; sans ce drapeau, simple constat")

    def handle(self, *args, **options):
        ecrire = options["ecrire"]
        w = self.stdout.write

        appuis = AppuiFait.objects.filter(note__startswith=MARQUE)
        greffes = appuis.exclude(fait__axes=None).distinct()
        faits_prose = Fait.objects.filter(raison__startswith=MARQUE, axes=None)

        n_greffes = greffes.count()
        n_faits = faits_prose.count()
        n_appuis_prose = AppuiFait.objects.filter(fait__in=faits_prose).count()

        detail_greffes = [(a.fait_id, a.fait.statement_id,
                           [x.nom[:26] for x in a.fait.axes.all()])
                          for a in greffes.select_related('fait')]

        w("=" * 76)
        w("PURGE DU BACKFILL ÉCRIT DANS LES AXES")
        w("=" * 76)
        w(f"  Fait de prose à supprimer      : {n_faits}")
        w(f"    leurs appuis, supprimés avec : {n_appuis_prose}")
        w(f"  greffes sur un Fait d'axe à retirer : {n_greffes}")

        if detail_greffes:
            w("")
            w("  GREFFES — l'appui part, le Fait d'axe reste")
            vus = set()
            for fid, sid, axes in detail_greffes:
                if fid in vus:
                    continue
                vus.add(fid)
                n = sum(1 for f, _s, _a in detail_greffes if f == fid)
                w(f"      Fait {fid} (statement {sid}, {', '.join(axes)}) — "
                  f"{n} appui(s) retiré(s)")

        with transaction.atomic():
            greffes.delete()
            faits_prose.delete()      # les appuis suivent par CASCADE
            if not ecrire:
                transaction.set_rollback(True)

        restants = Fait.objects.count()
        w("")
        if ecrire:
            w(self.style.SUCCESS(
                f"  PURGÉ. Fait restants : {restants} — le chantier des axes seul."))
        else:
            w(self.style.WARNING("  CONSTAT SEULEMENT — rien n'a été effacé. "
                                 "Relancer avec --ecrire."))
