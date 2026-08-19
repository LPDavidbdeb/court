"""
Ce que la demande de juillet plaide, ce que la base sait, et ce qui n'appuie rien.

    python manage.py verifier_appuis_depot
    python manage.py verifier_appuis_depot --orphelines
    python manage.py verifier_appuis_depot --paragraphe 45

La commande ne corrige rien, sur le modèle de `verifier_schemas` : une fois
`persister_appuis_depot` passé, la base et la prose concordent ; à la première
réécriture d'un paragraphe elles recommencent à diverger sans que rien ne le
signale. C'est cette dérive que la commande rend visible.

Trois écarts, de natures différentes :

  NON PERSISTÉ   la prose invoque une pièce qu'aucun appui ne porte. Relancer
                 `persister_appuis_depot --ecrire`.
  NON CITÉ       un appui porte une pièce que le paragraphe n'invoque plus. Le
                 lien est réputé établi alors que le texte ne le dit pas : à
                 trancher dans le TEXTE.
  ORPHELINE      une pièce du bordereau qu'aucun paragraphe n'invoque. Ce n'est
                 pas une erreur — une pièce peut être versée sans être plaidée.
                 C'est une liste de travail.

Le périmètre est celui du dépôt seul. Les axes n'y entrent pas : ils explorent
une présentation future et invoquent des pièces versées après le dépôt, qui ne
pourraient par construction jamais être citées dans la demande de juillet. Les
mêler produirait des écarts impossibles à résorber.
"""
from collections import defaultdict

from django.core.management.base import BaseCommand

from case_manager.appui_depot_service import lecture_prose
from case_manager.models import AppuiDepotJuillet, BordereauDepotJuillet
from document_manager.models import Document
from document_manager.numerotation import index_numeros


class Command(BaseCommand):
    help = "Compare les appuis persistés du dépôt aux cotes citées dans la demande."

    def add_arguments(self, parser):
        parser.add_argument("--document", type=int, default=9)
        parser.add_argument("--limite", type=int, default=25)
        parser.add_argument("--orphelines", action="store_true",
                            help="lister les pièces qu'aucun paragraphe n'invoque")
        parser.add_argument("--paragraphe", default=None,
                            help="détailler un paragraphe, par son numéro d'écran")

    def handle(self, *args, **options):
        doc = Document.objects.get(pk=options["document"])
        limite = options["limite"]
        numeros = index_numeros(doc)
        w = self.stdout.write

        lecture = lecture_prose(doc.pk)
        prose = {stmt.pk: {e.pk for e, _c, _v in appuis}
                 for _n, stmt, appuis, _i in lecture}
        fantomes = [(numeros.get(stmt.pk, "?"), inc)
                    for _n, stmt, _a, inc in lecture if inc]

        base = defaultdict(set)
        invoquees = set()
        for a in AppuiDepotJuillet.objects.all():
            base[a.statement_id].add(a.entree_id)
            invoquees.add(a.entree_id)

        entrees = list(BordereauDepotJuillet.objects.all())
        orphelines = [e for e in entrees if e.pk not in invoquees]
        deposees = [e for e in entrees if e.cote]

        non_persiste = {s: v for s in prose
                        if (v := prose[s] - base.get(s, set()))}
        non_cite = {s: v for s in base
                    if (v := base[s] - prose.get(s, set()))}

        # --- détail d'un paragraphe, si demandé ---
        if options["paragraphe"]:
            cible = options["paragraphe"]
            trouve = [s for s, lib in numeros.items() if lib.split(" ")[0] == cible]
            for s in trouve:
                w(f"§ {numeros[s]}")
                for a in AppuiDepotJuillet.objects.filter(statement_id=s).select_related('entree'):
                    marque = " (via liasse)" if a.via_liasse else ""
                    w(f"    {a.cote_citee:<10}→ {a.entree.cote:<10} "
                      f"{a.entree.source_type:<14}{a.entree.description[:38]}{marque}")
            if not trouve:
                w(self.style.ERROR(f"  Aucun paragraphe « {cible} »."))
            return

        w("=" * 76)
        w(f"VÉRIFICATION — {doc.title[:56]}")
        w("=" * 76)
        w(f"  paragraphes invoquant au moins une pièce : {len(prose)}")
        w(f"  paragraphes portant au moins un appui    : {len(base)}")
        w(f"  pièces au bordereau                      : {len(entrees)}"
          f"  (cotées en juillet : {len(deposees)})")
        w(f"  pièces invoquées par au moins un paragraphe : "
          f"{len(entrees) - len(orphelines)}")

        if non_persiste:
            total = sum(len(v) for v in non_persiste.values())
            w("")
            w(self.style.WARNING(
                f"  NON PERSISTÉ — {total} lien(s) sur {len(non_persiste)} paragraphe(s)"))
            for s, v in list(non_persiste.items())[:limite]:
                w(f"      § {numeros.get(s, s):<16} {len(v)} pièce(s)")

        if non_cite:
            total = sum(len(v) for v in non_cite.values())
            w("")
            w(self.style.ERROR(
                f"  NON CITÉ — {total} appui(s) sur {len(non_cite)} paragraphe(s)"))
            w("    Persisté en base, absent du texte déposé. À trancher dans le TEXTE.")
            par_pk = {e.pk: e for e in entrees}
            for s, v in list(non_cite.items())[:limite]:
                cotes = ", ".join(sorted(par_pk[k].cote or "(sans cote)" for k in v))
                w(f"      § {numeros.get(s, s):<16} {cotes[:52]}")

        if fantomes:
            w("")
            w(self.style.ERROR(
                f"  COTES FANTÔMES — {len(fantomes)} paragraphe(s)"))
            for libelle, cotes in fantomes[:limite]:
                w(f"      § {libelle:<16} {', '.join(cotes)}")

        w("")
        w(f"  ORPHELINES — {len(orphelines)} pièce(s) qu'aucun paragraphe n'invoque")
        w("    Ce n'est pas une erreur : une pièce peut être versée sans être plaidée.")
        if options["orphelines"]:
            for e in sorted(orphelines, key=lambda x: (x.rang or 0, x.sous_rang or 0)):
                w(f"      {(e.cote or '(non déposée)'):<14} {e.source_type:<14} "
                  f"{e.description[:42]}")
        else:
            w("    Ajouter --orphelines pour le détail.")

        w("")
        if not (non_persiste or non_cite or fantomes):
            w(self.style.SUCCESS(
                "  CONCORDANCE — la base dit exactement ce que la demande plaide."))
