#!/usr/bin/env python
"""
Exporte le "carnet de rappel" des Quotes : tout ce qu'il faudra recabler apres la purge.

    .venv/bin/python docs/purge_quotes/export_quote_links.py

Produit docs/purge_quotes/quote_links_export.json.

Chaque quote est decrite par sa CLE NATURELLE (celle du parent + son texte normalise),
jamais par sa PK, puisque la PK ne survivra pas a la purge. Les PK d'origine sont
conservees a titre indicatif uniquement (tracabilite / diagnostic).

Lecture seule : ce script n'ecrit jamais en base.
"""
import json
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
OUT_PATH = Path(__file__).resolve().parent / "quote_links_export.json"
sys.path.insert(0, str(BASE_DIR))
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django  # noqa: E402
django.setup()

from django.contrib.contenttypes.models import ContentType  # noqa: E402

from document_manager.models import LibraryNode  # noqa: E402
from email_manager.models import Quote as EmailQuote  # noqa: E402
from pdf_manager.models import Quote as PDFQuote  # noqa: E402

EQ_CT = ContentType.objects.get_for_model(EmailQuote)
PQ_CT = ContentType.objects.get_for_model(PDFQuote)


def norm(text):
    """Normalisation de reference. Doit rester identique dans relink_quotes.py."""
    return " ".join((text or "").split())


def nodes_index(content_type):
    """{object_id: [ {node...}, ... ]} pour un content_type donne."""
    index = {}
    qs = LibraryNode.objects.filter(content_type=content_type).select_related("document")
    for node in qs:
        index.setdefault(node.object_id, []).append({
            "node_id": node.pk,
            "path": node.path,
            "depth": node.depth,
            "item": node.item,
            "is_evidence": node.is_evidence,
            "document_id": node.document_id,
            "document_title": node.document.title,
            "document_source_type": node.document.source_type,
        })
    return index


email_nodes = nodes_index(EQ_CT)
pdf_nodes = nodes_index(PQ_CT)

payload = {
    "_meta": {
        "note": "Cle de re-appariement = (natural_key du parent, quote_text_normalized).",
        "normalization": "' '.join(text.split())",
        "email_quote_count": EmailQuote.objects.count(),
        "pdf_quote_count": PDFQuote.objects.count(),
    },
    "email_quotes": [],
    "pdf_quotes": [],
}

for q in (EmailQuote.objects
          .select_related("email", "email__thread")
          .prefetch_related("trames_narratives")
          .order_by("email_id", "created_at", "pk")):
    email = q.email
    payload["email_quotes"].append({
        "old_pk": q.pk,
        "created_at": q.created_at.isoformat() if q.created_at else None,
        "quote_text": q.quote_text,
        "quote_text_normalized": norm(q.quote_text),
        "has_embedding": q.embedding is not None,
        "parent": {
            "model": "email_manager.Email",
            "old_pk": q.email_id,
            # CLE NATURELLE : message_id est unique et survit a la purge
            "natural_key": {"message_id": email.message_id if email else None},
            "thread_id": email.thread.thread_id if email and email.thread else None,
            "subject": email.subject if email else None,
            "date_sent": email.date_sent.isoformat() if email and email.date_sent else None,
        },
        "trame_ids": sorted(t.pk for t in q.trames_narratives.all()),
        "library_nodes": email_nodes.get(q.pk, []),
    })

for q in (PDFQuote.objects
          .select_related("pdf_document")
          .prefetch_related("trames_narratives")
          .order_by("pdf_document_id", "created_at", "pk")):
    doc = q.pdf_document
    payload["pdf_quotes"].append({
        "old_pk": q.pk,
        "created_at": q.created_at.isoformat() if q.created_at else None,
        "quote_text": q.quote_text,
        "quote_text_normalized": norm(q.quote_text),
        "page_number": q.page_number,
        "quote_location_details": q.quote_location_details,
        "has_embedding": q.embedding is not None,
        "parent": {
            "model": "pdf_manager.PDFDocument",
            # PDFDocument n'a pas de cle unique : on garde la PK (elle, n'est pas purgee)
            # + titre et fichier pour verification manuelle.
            "old_pk": q.pdf_document_id,
            "natural_key": {"pdf_document_id": q.pdf_document_id},
            "title": doc.title if doc else None,
            "file": doc.file.name if doc and doc.file else None,
            "document_date": doc.document_date.isoformat() if doc and doc.document_date else None,
        },
        "trame_ids": sorted(t.pk for t in q.trames_narratives.all()),
        "library_nodes": pdf_nodes.get(q.pk, []),
    })

OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

n_links_e = sum(len(q["trame_ids"]) for q in payload["email_quotes"])
n_links_p = sum(len(q["trame_ids"]) for q in payload["pdf_quotes"])
n_nodes_e = sum(len(q["library_nodes"]) for q in payload["email_quotes"])
n_nodes_p = sum(len(q["library_nodes"]) for q in payload["pdf_quotes"])
no_key = sum(1 for q in payload["email_quotes"] if not q["parent"]["natural_key"]["message_id"])

print(f"Ecrit : {OUT_PATH}")
print(f"  email quotes  : {len(payload['email_quotes']):>5}  liens trame {n_links_e:>5}  noeuds {n_nodes_e:>5}")
print(f"  pdf quotes    : {len(payload['pdf_quotes']):>5}  liens trame {n_links_p:>5}  noeuds {n_nodes_p:>5}")
if no_key:
    print(f"  ATTENTION : {no_key} quote(s) courriel sans message_id parent -> recablage manuel.")
print()
print("Commite ce fichier AVANT la purge. C'est le seul moyen de recabler sans restaurer le dump.")
