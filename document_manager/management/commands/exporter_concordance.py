"""
La concordance des paragraphes, en mode diagnostique ou strict.

Le diagnostique sort toujours : c'est lui qui nomme ce qui manque. Le strict
n'est permis que si EX01 à EX07 sont toutes satisfaites sur le même état.
"""
import json
import sys

from django.core.management.base import BaseCommand, CommandError

from document_manager.models import Document
from document_manager import export_concordance as ex
from document_manager import referent as referent_service


class Command(BaseCommand):
    help = "Produit la concordance paragraphes + cotes, en JSON et CSV."

    def add_arguments(self, parser):
        parser.add_argument("--source", type=int, required=True)
        parser.add_argument("--cible", type=int, required=True)
        parser.add_argument("--lock", default="legal/depots/2026-07-24_initial/cotes.lock.json")
        parser.add_argument("--strict", action="store_true")
        parser.add_argument("--json", default=None)
        parser.add_argument("--csv", default=None)
        parser.add_argument("--limite", type=int, default=10)
        parser.add_argument("--accepter-equivalences-contenant", action="store_true")

    def handle(self, *args, **o):
        w = self.stdout.write
        source = Document.objects.filter(pk=o["source"]).first()
        cible = Document.objects.filter(pk=o["cible"]).first()
        if source is None or cible is None:
            raise CommandError("Document source ou cible introuvable.")

        from case_manager import cotes_concordance as cc
        rapport_lock = None
        try:
            rapport_lock = cc.reconcilier(
                o["lock"],
                accepter_equivalences_contenant=o["accepter_equivalences_contenant"])
        except cc.LockIndisponible as e:
            w(self.style.WARNING(f"  Contrôle historique des cotes BLOQUÉ — {e}"))

        controle_ref = None
        ref = referent_service.referent_de(source)
        if ref is not None:
            inst = ref.instantanes.first()
            if inst is not None:
                ecarts = referent_service.comparer(inst)
                controle_ref = {
                    'instantane': inst.pk,
                    'empreinte': inst.empreinte_globale,
                    'intact': referent_service.contenu_intact(ecarts),
                    'ecarts': {k: len(v) for k, v in ecarts.items()
                               if isinstance(v, list)},
                }

        restitution = ex.construire(source, cible, rapport_lock, controle_ref)

        w("=" * 78)
        w("CONCORDANCE")
        w("=" * 78)
        p = restitution['perimetre']
        w(f"  source : {p['document_source']} — {p['titre_source'][:48]} "
          f"[{p['mode_source']}]")
        w(f"  cible  : {p['document_cible']} — {p['titre_cible'][:48]} "
          f"[{p['mode_cible']}]")
        w(f"  état de cotation : {p['empreinte_etat_cotation'][:16]}… "
          f"({p['entrees_au_registre']} entrées)")
        w(f"  contrôle du lock : {p['controle_lock']}")
        w(f"  contrôle référent: {(controle_ref or {}).get('intact')}")
        w(f"  lignes           : {len(restitution['lignes'])}")
        w("")
        w("  CONDITIONS DE L'EXPORT STRICT")
        for v in restitution['verdicts']:
            marque = self.style.SUCCESS("  OK  ") if v['satisfait'] \
                else self.style.ERROR("BLOQUE")
            w(f"    {marque} {v['condition']} — {v['libelle']}")
            if not v['satisfait']:
                w(f"           {v['nombre_de_motifs']} motif(s)")
                for m in v['motifs'][:o["limite"]]:
                    w(f"             · {m}")

        w("")
        if restitution['strict_possible']:
            w(self.style.SUCCESS("  EXPORT STRICT POSSIBLE."))
        else:
            w(self.style.WARNING(
                "  EXPORT STRICT REFUSÉ. La sortie diagnostique reste disponible."))

        try:
            contenu_json = ex.en_json(restitution, strict=o["strict"])
            contenu_csv = ex.en_csv(restitution, strict=o["strict"])
        except ex.ExportStrictRefuse as e:
            w(self.style.ERROR(f"\n  {e}"))
            sys.exit(1)

        if o["json"]:
            with open(o["json"], "w", encoding="utf-8") as f:
                f.write(contenu_json)
            w(f"\n  JSON écrit : {o['json']}")
        if o["csv"]:
            with open(o["csv"], "w", encoding="utf-8", newline="") as f:
                f.write(contenu_csv)
            w(f"  CSV écrit  : {o['csv']}")

        if not restitution['strict_possible'] and o["strict"]:
            sys.exit(1)
