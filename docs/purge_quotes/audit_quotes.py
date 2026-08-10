#!/usr/bin/env python
"""
Audit de l'etat des Quotes et de tout ce qui en depend.

A lancer AVANT et APRES la purge, puis comparer :

    .venv/bin/python docs/purge_quotes/audit_quotes.py > docs/purge_quotes/audit_avant.txt
    ...
    .venv/bin/python docs/purge_quotes/audit_quotes.py > docs/purge_quotes/audit_apres.txt
    diff docs/purge_quotes/audit_avant.txt docs/purge_quotes/audit_apres.txt

Lecture seule : ce script n'ecrit jamais en base.
"""
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django  # noqa: E402
django.setup()

from django.contrib.contenttypes.models import ContentType  # noqa: E402
from django.db import connection  # noqa: E402
from django.db.models import Count  # noqa: E402

from argument_manager.models import TrameNarrative  # noqa: E402
from case_manager.models import ExhibitRegistry, ProducedExhibit  # noqa: E402
from document_manager.models import LibraryNode  # noqa: E402
from email_manager.models import Email, Quote as EmailQuote  # noqa: E402
from pdf_manager.models import PDFDocument, Quote as PDFQuote  # noqa: E402

EQ_CT = ContentType.objects.get_for_model(EmailQuote)
PQ_CT = ContentType.objects.get_for_model(PDFQuote)


def section(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


section("1. VOLUMES")
print(f"  email_manager.Quote            {EmailQuote.objects.count():>6}")
print(f"  pdf_manager.Quote             {PDFQuote.objects.count():>6}")
print(f"  emails porteurs de citations  {Email.objects.filter(quotes__isnull=False).distinct().count():>6} / {Email.objects.count()}")
print(f"  pdf porteurs de citations     {PDFDocument.objects.filter(quotes__isnull=False).distinct().count():>6} / {PDFDocument.objects.count()}")
print(f"  embeddings email quotes       {EmailQuote.objects.exclude(embedding=None).count():>6} / {EmailQuote.objects.count()}")
print(f"  embeddings pdf quotes         {PDFQuote.objects.exclude(embedding=None).count():>6} / {PDFQuote.objects.count()}")


section("2. LIENS M2M (nettoyes automatiquement par l'ORM au delete)")
for field in ("citations_courriel", "citations_pdf"):
    through = TrameNarrative._meta.get_field(field).remote_field.through
    print(f"  {through._meta.db_table:<62} {through.objects.count():>6}")
print(f"  trames citant >=1 quote courriel  "
      f"{TrameNarrative.objects.filter(citations_courriel__isnull=False).distinct().count():>4} / {TrameNarrative.objects.count()}")
print(f"  trames citant >=1 quote pdf       "
      f"{TrameNarrative.objects.filter(citations_pdf__isnull=False).distinct().count():>4} / {TrameNarrative.objects.count()}")
print(f"  quotes courriel orphelines (aucune trame) "
      f"{EmailQuote.objects.filter(trames_narratives__isnull=True).count():>4}")
print(f"  quotes pdf orphelines (aucune trame)      "
      f"{PDFQuote.objects.filter(trames_narratives__isnull=True).count():>4}")


section("3. LIENS GENERIQUES (JAMAIS nettoyes : aucun GenericRelation declare)")
eq_ids = set(EmailQuote.objects.values_list("id", flat=True))
pq_ids = set(PDFQuote.objects.values_list("id", flat=True))

for label, manager in (("LibraryNode", LibraryNode.objects),
                       ("ProducedExhibit", ProducedExhibit.objects),
                       ("ExhibitRegistry", ExhibitRegistry.objects)):
    rows_e = list(manager.filter(content_type=EQ_CT).values_list("id", "object_id"))
    rows_p = list(manager.filter(content_type=PQ_CT).values_list("id", "object_id"))
    dang_e = [r for r in rows_e if r[1] is None or r[1] not in eq_ids]
    dang_p = [r for r in rows_p if r[1] is None or r[1] not in pq_ids]
    print(f"  {label:<18} ->EmailQuote {len(rows_e):>5}  dangling {len(dang_e):>5}"
          f"   ->PDFQuote {len(rows_p):>5}  dangling {len(dang_p):>5}")
    for pk, oid in (dang_e + dang_p)[:15]:
        print(f"       dangling {label} pk={pk} object_id={oid}")

print()
print("  Repartition des noeuds-quotes par document :")
nodes = LibraryNode.objects.filter(content_type__in=[EQ_CT, PQ_CT]).select_related("document")
per_doc = {}
for n in nodes:
    key = (n.document_id, n.document.source_type, n.document.title[:45])
    per_doc.setdefault(key, [0, 0])
    per_doc[key][0 if n.content_type_id == EQ_CT.id else 1] += 1
for (doc_id, src, title), (ne, np_) in sorted(per_doc.items()):
    print(f"    doc {doc_id:<3} [{src:<10}] email={ne:<4} pdf={np_:<4} {title}")


section("4. TABLE DERIVEE ProducedExhibit (regeneree, pas a sauvegarder)")
for row in ProducedExhibit.objects.values("content_type").annotate(n=Count("id")).order_by("-n"):
    ct = ContentType.objects.filter(id=row["content_type"]).first()
    flag = "  <-- quote" if row["content_type"] in (EQ_CT.id, PQ_CT.id) else ""
    print(f"    {str(ct):<42} {row['n']:>6}{flag}")


section("5. ExhibitRegistry (attribue les cotes P-n : doit rester intact)")
print(f"  total {ExhibitRegistry.objects.count()}")
for row in ExhibitRegistry.objects.values("content_type").annotate(n=Count("id")).order_by("-n"):
    ct = ContentType.objects.filter(id=row["content_type"]).first()
    print(f"    {str(ct):<42} {row['n']:>6}")


section("6. CLES PRIMAIRES ET SEQUENCES")
with connection.cursor() as cur:
    for model in (EmailQuote, PDFQuote):
        table = model._meta.db_table
        cur.execute(f'SELECT MIN(id), MAX(id), COUNT(*) FROM "{table}"')
        mn, mx, count = cur.fetchone()
        cur.execute("SELECT pg_get_serial_sequence(%s, 'id')", [table])
        seq = cur.fetchone()[0]
        last = None
        if seq:
            cur.execute(f"SELECT last_value, is_called FROM {seq}")
            last = cur.fetchone()
        holes = (mx - mn + 1 - count) if mn is not None else 0
        print(f"  {model._meta.label:<24} min={mn} max={mx} count={count} trous={holes}")
        print(f"  {'':<24} sequence={seq} last_value={last}")


section("7. RE-ANCRAGE DU TEXTE DANS LA SOURCE (fiabilite du recablage)")
miss_e = []
for q in EmailQuote.objects.select_related("email").iterator():
    body = " ".join(((q.email.body_plain_text or "") if q.email else "").split())
    txt = " ".join((q.quote_text or "").split())
    if txt and txt not in body:
        miss_e.append(q.pk)
print(f"  quotes courriel dont le texte n'est PAS une sous-chaine exacte du corps : "
      f"{len(miss_e)} / {EmailQuote.objects.count()}")
print(f"    pk : {miss_e[:40]}{' ...' if len(miss_e) > 40 else ''}")
print("  -> ces citations ne seront pas re-extractibles automatiquement.")


section("8. DOUBLONS DE TEXTE (ambiguite au recablage)")
def dup_report(model, parent_field, label):
    seen = {}
    for q in model.objects.all().iterator():
        key = (getattr(q, parent_field), " ".join((q.quote_text or "").split()))
        seen.setdefault(key, []).append(q.pk)
    dups = {k: v for k, v in seen.items() if len(v) > 1}
    print(f"  {label} : {len(dups)} couple(s) (parent, texte) portes par plusieurs quotes")
    for (parent, txt), pks in list(dups.items())[:10]:
        print(f"    parent={parent} pks={pks} texte={txt[:60]!r}")

dup_report(EmailQuote, "email_id", "email_manager.Quote")
dup_report(PDFQuote, "pdf_document_id", "pdf_manager.Quote")
print("  -> tout doublon devra etre tranche a la main lors du recablage.")

print()
print("Fin de l'audit.")
