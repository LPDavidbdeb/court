#!/usr/bin/env python
"""
Recable les Quotes recreees a partir de docs/purge_quotes/quote_links_export.json.

    .venv/bin/python docs/purge_quotes/relink_quotes.py --dry-run   # rapport seul
    .venv/bin/python docs/purge_quotes/relink_quotes.py --apply     # ecrit en base

Ce que le script retablit :
  1. les M2M TrameNarrative.citations_courriel / .citations_pdf ;
  2. les LibraryNode.object_id des documents PRODUCED (doc 5 "Test", doc 6 "Affidavit").

Regle d'appariement (identique a celle de l'export) :
  - courriel : (email.message_id, ' '.join(quote_text.split()))
  - pdf      : (pdf_document_id, page_number, ' '.join(quote_text.split()))

Tout ce qui n'est pas apparie de facon UNIVOQUE est laisse intact et rapporte en fin
d'execution. Le script ne devine jamais, sauf si on lui demande explicitement :

    --resolve-duplicates-by-order

qui, pour un groupe de citations au texte STRICTEMENT identique sous le meme parent,
apparie ancien->nouveau par rang de created_at, a condition que les effectifs
correspondent. Heuristique assumee, a n'utiliser qu'apres lecture du rapport --dry-run.

--apply s'execute dans une transaction unique : en cas d'erreur, rien n'est ecrit.
"""
import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
EXPORT_PATH = Path(__file__).resolve().parent / "quote_links_export.json"
sys.path.insert(0, str(BASE_DIR))
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django  # noqa: E402
django.setup()

from django.contrib.contenttypes.models import ContentType  # noqa: E402
from django.db import transaction  # noqa: E402

from argument_manager.models import TrameNarrative  # noqa: E402
from document_manager.models import LibraryNode  # noqa: E402
from email_manager.models import Email, Quote as EmailQuote  # noqa: E402
from pdf_manager.models import Quote as PDFQuote  # noqa: E402


def norm(text):
    return " ".join((text or "").split())


parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--dry-run", action="store_true", help="rapport seul, aucune ecriture")
group.add_argument("--apply", action="store_true", help="ecrit en base (transaction unique)")
parser.add_argument("--resolve-duplicates-by-order", action="store_true",
                    help="apparie les textes strictement identiques par rang de created_at")
args = parser.parse_args()

if not EXPORT_PATH.exists():
    sys.exit(f"Introuvable : {EXPORT_PATH}\nLance d'abord export_quote_links.py (AVANT la purge).")

data = json.loads(EXPORT_PATH.read_text(encoding="utf-8"))

# --- Index des quotes ACTUELLES (celles qui viennent d'etre recreees) ------------------

email_pk_by_message_id = dict(Email.objects.values_list("message_id", "pk"))

created_at_by_pk = {"email": {}, "pdf": {}}

current_email = defaultdict(list)   # (email_id, texte_norm) -> [quote_pk, ...]
for pk, email_id, text, created in EmailQuote.objects.values_list("pk", "email_id", "quote_text", "created_at"):
    current_email[(email_id, norm(text))].append(pk)
    created_at_by_pk["email"][pk] = created

current_pdf = defaultdict(list)     # (pdf_id, page, texte_norm) -> [quote_pk, ...]
for pk, doc_id, page, text, created in PDFQuote.objects.values_list(
        "pk", "pdf_document_id", "page_number", "quote_text", "created_at"):
    current_pdf[(doc_id, page, norm(text))].append(pk)
    created_at_by_pk["pdf"][pk] = created

EQ_CT = ContentType.objects.get_for_model(EmailQuote)
PQ_CT = ContentType.objects.get_for_model(PDFQuote)

# --- Resolution -----------------------------------------------------------------------

trame_links = defaultdict(set)      # (kind, trame_id) -> {new_quote_pk}
node_updates = []                   # (node_id, content_type_id, new_quote_pk)
unmatched = []                      # entrees non resolues
ambiguous = []                      # entrees a appariement multiple

CT_ID = {"email": EQ_CT.id, "pdf": PQ_CT.id}


def bind(kind, entry, new_pk):
    for tid in entry["trame_ids"]:
        trame_links[(kind, tid)].add(new_pk)
    for node in entry["library_nodes"]:
        node_updates.append((node["node_id"], CT_ID[kind], new_pk))


for entry in data["email_quotes"]:
    message_id = entry["parent"]["natural_key"].get("message_id")
    email_pk = email_pk_by_message_id.get(message_id)
    if email_pk is None:
        unmatched.append(("email", entry, "courriel parent introuvable (message_id)"))
        continue
    key = (email_pk, entry["quote_text_normalized"])
    candidates = current_email.get(key, [])
    if len(candidates) == 0:
        unmatched.append(("email", entry, "aucune quote recreee avec ce texte"))
    elif len(candidates) > 1:
        ambiguous.append(("email", entry, candidates, key))
    else:
        bind("email", entry, candidates[0])

for entry in data["pdf_quotes"]:
    doc_pk = entry["parent"]["natural_key"].get("pdf_document_id")
    key = (doc_pk, entry["page_number"], entry["quote_text_normalized"])
    candidates = current_pdf.get(key, [])
    if len(candidates) == 0:
        unmatched.append(("pdf", entry, "aucune quote recreee avec ce (document, page, texte)"))
    elif len(candidates) > 1:
        ambiguous.append(("pdf", entry, candidates, key))
    else:
        bind("pdf", entry, candidates[0])

# --- Resolution optionnelle des groupes de textes strictement identiques ---------------

resolved = []
if args.resolve_duplicates_by_order:
    groups = defaultdict(list)
    for kind, entry, candidates, key in ambiguous:
        groups[(kind, key)].append((entry, candidates))
    still_ambiguous = []
    for (kind, key), items in groups.items():
        candidates = items[0][1]
        entries = sorted((e for e, _ in items), key=lambda e: (e["created_at"] or "", e["old_pk"]))
        news = sorted(candidates, key=lambda pk: (created_at_by_pk[kind].get(pk), pk))
        if len(entries) != len(news):
            for e in entries:
                still_ambiguous.append((kind, e, candidates, key))
            continue
        for e, new_pk in zip(entries, news):
            bind(kind, e, new_pk)
            resolved.append((kind, e["old_pk"], new_pk))
    ambiguous = still_ambiguous

# --- Rapport --------------------------------------------------------------------------

total_e = len(data["email_quotes"])
total_p = len(data["pdf_quotes"])
matched_e = total_e - sum(1 for r in unmatched if r[0] == "email") - sum(1 for r in ambiguous if r[0] == "email")
matched_p = total_p - sum(1 for r in unmatched if r[0] == "pdf") - sum(1 for r in ambiguous if r[0] == "pdf")
n_links = sum(len(v) for v in trame_links.values())

print("=" * 78)
print("APPARIEMENT")
print("=" * 78)
print(f"  quotes courriel : {matched_e}/{total_e} appariees")
print(f"  quotes pdf      : {matched_p}/{total_p} appariees")
print(f"  liens trame a retablir     : {n_links}")
print(f"  noeuds LibraryNode a repointer : {len(node_updates)}")

if resolved:
    print()
    print(f"RESOLUS PAR ORDRE created_at ({len(resolved)}) - heuristique explicite :")
    for kind, old_pk, new_pk in resolved:
        print(f"  [{kind}] old_pk={old_pk} -> new_pk={new_pk}")

if ambiguous:
    print()
    print("AMBIGUS (plusieurs quotes recreees portent le meme texte) - laisses intacts :")
    for kind, entry, cands, _key in ambiguous:
        print(f"  [{kind}] old_pk={entry['old_pk']} candidats={cands} texte={entry['quote_text_normalized'][:70]!r}")
    print("  -> relancer avec --resolve-duplicates-by-order, ou trancher a la main.")

if unmatched:
    print()
    print("NON APPARIES - a traiter a la main :")
    for kind, entry, reason in unmatched:
        parent = entry["parent"].get("subject") or entry["parent"].get("title") or ""
        print(f"  [{kind}] old_pk={entry['old_pk']} trames={entry['trame_ids']} "
              f"noeuds={[n['node_id'] for n in entry['library_nodes']]}")
        print(f"        motif : {reason}")
        print(f"        parent: {parent[:70]!r}")
        print(f"        texte : {entry['quote_text_normalized'][:100]!r}")

if args.dry_run:
    print()
    print("--dry-run : rien n'a ete ecrit.")
    sys.exit(0)

# --- Ecriture -------------------------------------------------------------------------

with transaction.atomic():
    n_added = 0
    for (kind, trame_id), quote_pks in trame_links.items():
        trame = TrameNarrative.objects.filter(pk=trame_id).first()
        if trame is None:
            print(f"  ATTENTION : TrameNarrative pk={trame_id} n'existe plus, {len(quote_pks)} lien(s) ignore(s).")
            continue
        field = trame.citations_courriel if kind == "email" else trame.citations_pdf
        field.add(*quote_pks)
        n_added += len(quote_pks)

    n_nodes = 0
    for node_id, ct_id, new_pk in node_updates:
        n_nodes += LibraryNode.objects.filter(pk=node_id, content_type_id=ct_id).update(object_id=new_pk)

print()
print("=" * 78)
print("ECRIT")
print("=" * 78)
print(f"  liens trame ajoutes        : {n_added}")
print(f"  noeuds LibraryNode repointes : {n_nodes}")
print()
print("Etape suivante :")
print("  .venv/bin/python manage.py backfill_embeddings")
print("  puis refresh_case_exhibits() + rebuild_produced_exhibits() pour chaque LegalCase")
print("  puis audit_quotes.py pour verifier que 'dangling' vaut 0 partout.")
