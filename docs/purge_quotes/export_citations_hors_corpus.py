#!/usr/bin/env python
"""
Inventorie les citations qui n'existent QUE dans la base : leur texte n'apparait
nulle part dans legal/**/*.md.

    .venv/bin/python docs/purge_quotes/export_citations_hors_corpus.py

Produit docs/purge_quotes/citations_hors_corpus.md.

C'est la SEULE chose qui merite d'etre sauvegardee avant la purge : le cablage
trame<->citation et les noeuds LibraryNode des documents PRODUCED sont jetables,
mais le CHOIX du passage (et, pour les PDF, sa page) ne se regenere pas.

Lecture seule sur la base.
"""
import os
import re
import sys
import unicodedata
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
LEGAL_DIR = BASE_DIR / "legal"
OUT_PATH = Path(__file__).resolve().parent / "citations_hors_corpus.md"
sys.path.insert(0, str(BASE_DIR))
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django  # noqa: E402
django.setup()

from email_manager.models import Quote as EmailQuote  # noqa: E402
from pdf_manager.models import Quote as PDFQuote  # noqa: E402

MIN_LEN = 25  # en deca, le texte est trop court pour qu'une correspondance prouve quoi que ce soit


def norm(s):
    """Normalisation tolerante : casse, apostrophes, guillemets, tirets, espaces."""
    s = unicodedata.normalize("NFKC", s or "")
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'),
                 ("«", '"'), ("»", '"'), ("–", "-"), ("—", "-"),
                 (" ", " ")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip().lower()


print("Lecture de legal/**/*.md ...")
md_files = sorted(LEGAL_DIR.rglob("*.md"))
corpus = "\n".join(norm(f.read_text(encoding="utf-8", errors="replace")) for f in md_files)
print(f"  {len(md_files)} fichiers, {len(corpus):,} caracteres normalises")

fiche_emails = {int(m.group(1)) for f in LEGAL_DIR.rglob("piece_*email-*.md")
                if (m := re.search(r"email-(\d+)", f.name))}
fiche_pdfs = {int(m.group(1)) for f in LEGAL_DIR.rglob("piece_pdf-*.md")
              if (m := re.search(r"pdf-(\d+)", f.name))}

rows_email, rows_pdf = [], []
stats = {"email": [0, 0, 0], "pdf": [0, 0, 0]}  # present, absent, trop court

for q in EmailQuote.objects.select_related("email", "email__thread", "email__sender_protagonist").order_by("email_id", "pk"):
    t = norm(q.quote_text)
    if len(t) < MIN_LEN:
        stats["email"][2] += 1
        continue
    if t in corpus:
        stats["email"][0] += 1
        continue
    stats["email"][1] += 1
    e = q.email
    rows_email.append({
        "pk": q.pk,
        "email_pk": q.email_id,
        "thread_id": e.thread.thread_id if e and e.thread else "",
        "message_id": e.message_id if e else "",
        "date": e.date_sent.strftime("%Y-%m-%d %H:%M") if e and e.date_sent else "",
        "sender": (e.sender_protagonist.get_full_name() if e and e.sender_protagonist else (e.sender if e else "")),
        "subject": (e.subject or "") if e else "",
        "fiche": "oui" if q.email_id in fiche_emails else "NON",
        "text": q.quote_text,
    })

for q in PDFQuote.objects.select_related("pdf_document", "pdf_document__author").order_by("pdf_document_id", "page_number", "pk"):
    t = norm(q.quote_text)
    if len(t) < MIN_LEN:
        stats["pdf"][2] += 1
        continue
    if t in corpus:
        stats["pdf"][0] += 1
        continue
    stats["pdf"][1] += 1
    d = q.pdf_document
    rows_pdf.append({
        "pk": q.pk,
        "doc_pk": q.pdf_document_id,
        "title": d.title if d else "",
        "author": d.author.get_full_name() if d and d.author else "",
        "date": d.document_date.isoformat() if d and d.document_date else "",
        "page": q.page_number,
        "location": q.quote_location_details or "",
        "fiche": "oui" if q.pdf_document_id in fiche_pdfs else "NON",
        "text": q.quote_text,
    })

lines = []
add = lines.append
add("# Citations présentes uniquement en base")
add("")
add("Généré par `docs/purge_quotes/export_citations_hors_corpus.py`.")
add("")
add("Chaque passage ci-dessous a été **sélectionné à la main** dans une source, et son texte "
    "n'apparaît nulle part dans `legal/**/*.md`. La source, elle, survit à la purge : ce qui "
    "disparaît est le **choix du passage** — et, pour les PDF, sa **page**.")
add("")
add("| Corpus | Total | Déjà dans le .md | Uniquement en base | Trop court pour trancher |")
add("|---|---|---|---|---|")
add(f"| courriels | {EmailQuote.objects.count()} | {stats['email'][0]} | **{stats['email'][1]}** | {stats['email'][2]} |")
add(f"| PDF | {PDFQuote.objects.count()} | {stats['pdf'][0]} | **{stats['pdf'][1]}** | {stats['pdf'][2]} |")
add("")
add("La colonne `fiche` indique si la source possède déjà une fiche `piece_*.md` : "
    "`oui` = il suffit de reporter le passage dans la fiche existante ; "
    "`NON` = la source elle-même n'a pas encore de fiche.")
add("")
add("---")
add("")
add(f"## Citations de courriels ({len(rows_email)})")
add("")
for r in rows_email:
    add(f"### eq-{r['pk']} — email-{r['email_pk']} — {r['date']}")
    add("")
    add(f"- **Expéditeur :** {r['sender']}")
    add(f"- **Objet :** {r['subject']}")
    add(f"- **thread_id :** `{r['thread_id']}` — **message_id :** `{r['message_id']}`")
    add(f"- **Fiche existante :** {r['fiche']}")
    add("")
    add("```text")
    add(r["text"])
    add("```")
    add("")
add("---")
add("")
add(f"## Citations de PDF ({len(rows_pdf)})")
add("")
for r in rows_pdf:
    add(f"### pq-{r['pk']} — pdf-{r['doc_pk']} — p. {r['page']}")
    add("")
    add(f"- **Document :** {r['title']}")
    add(f"- **Auteur :** {r['author']} — **Date :** {r['date']}")
    if r["location"]:
        add(f"- **Localisation :** {r['location']}")
    add(f"- **Fiche existante :** {r['fiche']}")
    add("")
    add("```text")
    add(r["text"])
    add("```")
    add("")

OUT_PATH.write_text("\n".join(lines), encoding="utf-8")

print()
print(f"Ecrit : {OUT_PATH}")
print(f"  courriels : {stats['email'][0]} deja dans le .md | {stats['email'][1]} uniquement en base | {stats['email'][2]} trop courtes")
print(f"  pdf       : {stats['pdf'][0]} deja dans le .md | {stats['pdf'][1]} uniquement en base | {stats['pdf'][2]} trop courtes")
print(f"  sans fiche : {sum(1 for r in rows_email if r['fiche'] == 'NON')} courriels, "
      f"{sum(1 for r in rows_pdf if r['fiche'] == 'NON')} pdf")
