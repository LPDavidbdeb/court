"""
« ancienne cote | nouvelle cote | source » — et le contrôle qui l'autorise à se
dire fidèle au dépôt.

La table se produit toujours. Ce qui dépend du contrôle, c'est la QUALIFICATION :
sans réconciliation réussie contre `cotes.lock.json`, elle reste une table
calculée, et le dit.
"""
import csv
import json
import sys

from django.core.management.base import BaseCommand

from case_manager import cotes_concordance as cc


class Command(BaseCommand):
    help = "Produit la table autonome des cotes et contrôle sa fidélité au dépôt."

    def add_arguments(self, parser):
        parser.add_argument("--lock", default="legal/depots/2026-07-24_initial/cotes.lock.json")
        parser.add_argument("--json", default=None, help="chemin de sortie JSON")
        parser.add_argument("--csv", default=None, help="chemin de sortie CSV")
        parser.add_argument("--liasses", action="store_true",
                            help="détailler la dispersion des liasses de juillet")
        parser.add_argument("--accepter-equivalences-contenant", action="store_true",
                            help="compter comme concordante une identité qui ne "
                                 "diffère que par le niveau de désignation "
                                 "(décision explicite, tracée dans la sortie)")
        parser.add_argument("--plancher-annee", type=int, default=None)
        parser.add_argument("--limite", type=int, default=12)

    def handle(self, *args, **o):
        w = self.stdout.write
        rapport = None
        try:
            rapport = cc.reconcilier(
                o["lock"],
                accepter_equivalences_contenant=o["accepter_equivalences_contenant"])
        except cc.LockIndisponible as e:
            w(self.style.ERROR(f"  CONTRÔLE HISTORIQUE BLOQUÉ — {e}"))

        w("=" * 78)
        w("CONTRÔLE HISTORIQUE  (lock → BordereauDepotJuillet)")
        w("=" * 78)
        if rapport is None:
            w("  NON EXÉCUTÉ. La table est produite, mais elle ne peut pas se")
            w("  dire fidèle au dépôt.")
        else:
            w(f"  lock                      : {rapport['lock']}")
            w(f"  sha256                    : {rapport['lock_sha256']}")
            w(f"  schéma / généré le        : {rapport['lock_schema']} / {rapport['lock_genere_le']}")
            w(f"  normalisation des identités: {rapport['normalisation']}")
            w(f"  cotes au lock             : {rapport['cotes_au_lock']}")
            w(f"  entrées au registre       : {rapport['entrees_au_registre']}")
            w(f"  ajouts sans cote de juillet: {rapport['ajouts_sans_cote_de_juillet']}")
            w(f"  contrôlées / concordantes : {rapport['controlees']} / {rapport['concordantes']}")
            for cle, libelle in (('manquantes', "cote du lock absente du registre"),
                                 ('divergentes', "sources divergentes"),
                                 ('ambigues', "identité illisible"),
                                 ('equivalences_contenant',
                                  "même matière, niveau de désignation différent")):
                n = len(rapport[cle])
                style = self.style.ERROR if (n and cle != 'equivalences_contenant') \
                    else (self.style.WARNING if n else (lambda x: x))
                w(style(f"  {libelle:<42}: {n}"))
                for d in rapport[cle][:o["limite"]]:
                    w(f"      {d.get('cote')}  {d.get('motif') or d.get('verdict','')}")
                    for eq in d.get('equivalences', []):
                        w(f"        {eq['au_registre']} ≡ {eq['au_lock']}  — {eq['preuve']}")
            verdict = (self.style.SUCCESS("CONFORME") if rapport['conforme']
                       else self.style.ERROR("NON CONFORME"))
            w(f"  verdict                   : {verdict}")
            if rapport['equivalences_contenant'] and not rapport['equivalences_acceptees']:
                w(self.style.WARNING(
                    "  Les équivalences de contenant ne sont PAS acceptées par "
                    "défaut :\n  elles comptent comme divergences. Aucune "
                    "correction n'est écrite."))

        table = cc.table_des_cotes(o["plancher_annee"], rapport)
        w("")
        w("=" * 78)
        w("TABLE DES COTES")
        w("=" * 78)
        w(f"  état de cotation (empreinte) : {table['empreinte_etat']}")
        w(f"  lignes                        : {table['nombre']}")
        w(f"  fidélité historique           : {table['fidelite_historique']}")
        w("")
        w(f"  {'ancienne':<22}{'nouvelle':<11}{'source':<22}{'groupe'}")
        w(f"  {'-'*21} {'-'*10} {'-'*21} {'-'*12}")
        for l in table['lignes'][:o["limite"]]:
            w(f"  {l['ancienne_cote']:<22}{l['nouvelle_cote']:<11}"
              f"{l['source']:<22}{l['groupe_de_classement']}")
        if table['nombre'] > o["limite"]:
            w(f"  … {table['nombre'] - o['limite']} autres")

        if o["liasses"]:
            w("")
            w("  DISPERSION DES LIASSES DE JUILLET")
            for d in cc.dispersion_des_liasses(table):
                w(f"    {d['cote_racine_juillet']} — {d['composants']} composants "
                  f"→ {d['nouvelles_cotes'][0]} … {d['nouvelles_cotes'][-1]}"
                  f"{'  (dispersée)' if d['dispersee'] else ''}")

        if o["json"]:
            with open(o["json"], "w", encoding="utf-8") as f:
                json.dump(table, f, ensure_ascii=False, indent=2, default=str)
            w(f"\n  JSON écrit : {o['json']}")
        if o["csv"]:
            with open(o["csv"], "w", encoding="utf-8", newline="") as f:
                cw = csv.DictWriter(f, fieldnames=list(table['lignes'][0].keys())
                                    if table['lignes'] else ['ancienne_cote'])
                cw.writeheader()
                for l in table['lignes']:
                    cw.writerow(l)
            w(f"  CSV écrit  : {o['csv']}")

        if rapport is None or not rapport['conforme']:
            sys.exit(1)
