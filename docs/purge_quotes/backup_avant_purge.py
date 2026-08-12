#!/usr/bin/env python
"""
Sauvegarde Django, à faire AVANT la purge des citations.

    .venv/bin/python docs/purge_quotes/backup_avant_purge.py
    .venv/bin/python docs/purge_quotes/backup_avant_purge.py --restore --dir <repertoire>

`pg_dump` n'est pas installé sur cette machine et le démon Docker est arrêté : pas de dump
du cluster. La sauvegarde passe donc par `dumpdata` / `loaddata`, qui suffisent ici parce
que la procédure ne touche qu'un ensemble de modèles connu et fermé.

Fidélité vérifiée : `VectorField` se sérialise en chaîne `"[0.0002,...]"` et se recharge
à l'identique (aller-retour testé sur `document_manager.Document`, écart nul).

DEUX GROUPES :

  A. Données détruites par la purge — irremplaçables, c'est le cœur de la sauvegarde.
       email_manager.Quote, pdf_manager.Quote        les 314 citations
       argument_manager.TrameNarrative               porte le câblage M2M vers les citations
       argument_manager.PerjuryArgument
       document_manager.LibraryNode                  dont les 80 nœuds supprimés
       case_manager.ExhibitRegistry                  doit rester inchangée : témoin de contrôle
       case_manager.ProducedExhibit                  dérivée, mais gratuite à sauvegarder

  B. Porteurs de vecteurs, dont la phase 4 vide la colonne `embedding`.
       Email, Event, PDFDocument, PhotoDocument, Document, Statement
     Ces vecteurs sont REGENERABLES (`manage.py backfill_embeddings`) et actuellement lus
     par personne. Le groupe est inclus par défaut malgré son poids ; `--sans-embeddings`
     le saute.

`loaddata` écrase par clé primaire : la restauration remet les objets sauvegardés tels
quels, mais ne supprime pas ceux créés depuis. Pour les tables de liaison M2M, en revanche,
`loaddata` réécrit l'ensemble des liens de chaque TrameNarrative restaurée.
"""
import argparse
import datetime as dt
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django  # noqa: E402
django.setup()

from django.apps import apps  # noqa: E402
from django.core.management import call_command  # noqa: E402

GROUPE_A = [
    "email_manager.Quote",
    "pdf_manager.Quote",
    "argument_manager.TrameNarrative",
    "argument_manager.PerjuryArgument",
    "document_manager.LibraryNode",
    "case_manager.ExhibitRegistry",
    "case_manager.ProducedExhibit",
]

GROUPE_B = [
    "email_manager.Email",
    "events.Event",
    "pdf_manager.PDFDocument",
    "photos.PhotoDocument",
    "document_manager.Document",
    "document_manager.Statement",
]

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--restore", action="store_true", help="recharge la sauvegarde")
ap.add_argument("--dir", default=None, help="répertoire (obligatoire pour --restore)")
ap.add_argument("--sans-embeddings", action="store_true",
                help="ne sauvegarde pas le groupe B (vecteurs régénérables)")
args = ap.parse_args()

labels = GROUPE_A + ([] if args.sans_embeddings else GROUPE_B)

if not args.restore:
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    out = Path(args.dir or (BASE_DIR / "backup_avant_purge_quotes" / stamp))
    out.mkdir(parents=True, exist_ok=True)
    print(f"Sauvegarde dans {out}\n")
    total = 0
    for label in labels:
        model = apps.get_model(label)
        n = model.objects.count()
        path = out / f"{label}.json"
        with open(path, "w", encoding="utf-8") as fh:
            call_command("dumpdata", label, stdout=fh)
        total += n
        groupe = "A" if label in GROUPE_A else "B"
        print(f"  [{groupe}] {label:<38} {n:>6} objets  {path.stat().st_size/1024/1024:>6.1f} Mo")

    (out / "MANIFEST.txt").write_text(
        f"Sauvegarde Django avant purge des citations\n"
        f"date    : {dt.datetime.now().isoformat()}\n"
        f"modeles : {len(labels)}\n"
        f"objets  : {total}\n\n"
        f"Restauration :\n"
        f"  .venv/bin/python docs/purge_quotes/backup_avant_purge.py --restore --dir {out}\n\n"
        f"Ce n'est pas un dump complet du cluster (pg_dump absent de la machine), mais la\n"
        f"totalite de ce que la procedure de purge modifie.\n"
        + "\n".join(f"  - {l}" for l in labels) + "\n",
        encoding="utf-8")

    print(f"\n  TOTAL {total} objets")
    print(f"\nRestauration :\n"
          f"  .venv/bin/python docs/purge_quotes/backup_avant_purge.py --restore --dir {out}")

else:
    if not args.dir:
        sys.exit("--restore exige --dir <repertoire>")
    src = Path(args.dir)
    if not src.exists():
        sys.exit(f"Introuvable : {src}")
    print(f"RESTAURATION depuis {src}\n")
    # Les cibles avant les objets qui les référencent : les citations avant les trames
    # qui les citent, faute de quoi loaddata échoue sur une clé étrangère absente.
    for label in labels:
        path = src / f"{label}.json"
        if not path.exists():
            print(f"  {label}: absent de la sauvegarde, ignoré")
            continue
        call_command("loaddata", str(path), verbosity=0)
        model = apps.get_model(label)
        print(f"  {label:<38} {model.objects.count():>6} objets en base")
    print("\nRestauration terminée.")
    print("Relancer ensuite : refresh_case_exhibits + rebuild_produced_exhibits.")
