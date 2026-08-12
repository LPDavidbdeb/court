#!/usr/bin/env python
"""
Rend le corpus de citations purement atomique : crée les blocs manquants, puis
supprime les compositions devenues redondantes.

    .venv/bin/python docs/purge_quotes/appliquer_decomposition.py --dry-run
    .venv/bin/python docs/purge_quotes/appliquer_decomposition.py --apply

Reprend l'analyse de `decomposition_citations.py` — mêmes intervalles, mêmes seuils —
et en tire les écritures.

CE QUE FAIT --apply, dans une transaction unique :

  1. Crée un bloc par passage manquant. Le bloc est rattaché à la même source que la
     composition dont il comble le trou (même courriel, ou même PDF et même page).

  2. Reporte les liens vers les trames. Une composition qui étayait la trame T
     étayait tout son texte ; après décomposition, l'équivalent est que CHACUNE de
     ses parties étaye T. Sans ce report, supprimer la composition retirerait
     silencieusement une preuve à la trame.

  3. Traite les nœuds LibraryNode qui pointent sur une composition : leur cible va
     disparaître, ils seraient laissés à pointer dans le vide.

  4. Supprime les compositions.

L'opération est réversible par la sauvegarde `backup_avant_purge.py`.
"""
import argparse
import os
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django  # noqa: E402
django.setup()

from django.contrib.contenttypes.models import ContentType  # noqa: E402
from django.db import transaction  # noqa: E402

from case_manager.models import ProducedExhibit  # noqa: E402
from document_manager.models import LibraryNode  # noqa: E402
from email_manager.models import Quote as EmailQuote  # noqa: E402
from pdf_manager.models import Quote as PDFQuote  # noqa: E402

TRIVIAL = 12
SUBST = {"’": "'", "‘": "'", "“": '"', "”": '"',
         "«": '"', "»": '"', "–": "-", "—": "-", " ": " "}

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
g = ap.add_mutually_exclusive_group(required=True)
g.add_argument("--dry-run", action="store_true", help="rapport seul, aucune écriture")
g.add_argument("--apply", action="store_true", help="écrit en base (transaction unique)")
ap.add_argument("--noeuds", choices=["supprimer", "repointer", "garder"], default="repointer",
                help="sort des nœuds LibraryNode visant une composition supprimée "
                     "(défaut : repointer vers sa première partie atomique)")
args = ap.parse_args()


def canon(s):
    out, idx, prev = [], [], True
    for i, ch in enumerate(s or ""):
        c = unicodedata.normalize("NFKC", SUBST.get(ch, ch))
        if c.isspace():
            if prev:
                continue
            out.append(" "); idx.append(i); prev = True
        else:
            out.append(c.lower()); idx.append(i); prev = False
    return "".join(out), idx


def union(iv):
    if not iv:
        return []
    iv = sorted(iv)
    m = [list(iv[0])]
    for a, b in iv[1:]:
        if a <= m[-1][1]:
            m[-1][1] = max(m[-1][1], b)
        else:
            m.append([a, b])
    return [tuple(x) for x in m]


def complement(spans, n):
    out, cur = [], 0
    for a, b in spans:
        if a > cur:
            out.append((cur, a))
        cur = max(cur, b)
    if cur < n:
        out.append((cur, n))
    return out


def occurrences(hay, needle):
    res, i = [], hay.find(needle)
    while i >= 0:
        res.append((i, i + len(needle)))
        i = hay.find(needle, i + 1)
    return res


# ------------------------------------------------------------------ analyse
groupes = defaultdict(list)
for q in PDFQuote.objects.select_related("pdf_document").all():
    groupes[("pdf", q.pdf_document_id)].append(
        {"obj": q, "kind": "pdf", "id": f"pq-{q.pk}", "raw": q.quote_text or "",
         "src": f"pdf-{q.pdf_document_id} p.{q.page_number}"})
for q in EmailQuote.objects.select_related("email").all():
    groupes[("email", q.email_id)].append(
        {"obj": q, "kind": "email", "id": f"eq-{q.pk}", "raw": q.quote_text or "",
         "src": f"email-{q.email_id}"})

toutes = [c for lst in groupes.values() for c in lst]
for c in toutes:
    c["canon"], c["map"] = canon(c["raw"])
    c["trames"] = sorted(t.pk for t in c["obj"].trames_narratives.all())

for lst in groupes.values():
    for c in lst:
        c["contient"], c["incluse_dans"] = [], []
    for c in lst:
        if not c["canon"]:
            continue
        for a in lst:
            if a is c or not a["canon"] or len(a["canon"]) >= len(c["canon"]):
                continue
            occ = occurrences(c["canon"], a["canon"])
            if occ:
                c["contient"].append((a, occ))
                a["incluse_dans"].append(c)

for c in toutes:
    c["atomique"] = not c["contient"]
for c in toutes:
    n = len(c["canon"])
    spans = union([iv for a, occ in c["contient"] if a["atomique"] for iv in occ])
    c["cov"] = (sum(b - a for a, b in spans) / n) if n else 0.0
    c["trous"] = []
    for a, b in complement(spans, n):
        if b - a <= TRIVIAL:
            continue
        d = c["map"][a] if a < len(c["map"]) else len(c["raw"])
        f = c["map"][b - 1] + 1 if b - 1 < len(c["map"]) else len(c["raw"])
        frag = c["raw"][d:f].strip()
        if len(frag) > TRIVIAL:
            c["trous"].append(frag)

composees = [c for c in toutes if not c["atomique"]]
a_creer = [(c, frag) for c in composees for frag in c["trous"]]

EQ_CT = ContentType.objects.get_for_model(EmailQuote)
PQ_CT = ContentType.objects.get_for_model(PDFQuote)
comp_e = {c["obj"].pk for c in composees if c["kind"] == "email"}
comp_p = {c["obj"].pk for c in composees if c["kind"] == "pdf"}
noeuds = list(LibraryNode.objects.filter(content_type=EQ_CT, object_id__in=comp_e)) + \
         list(LibraryNode.objects.filter(content_type=PQ_CT, object_id__in=comp_p))
pe = (ProducedExhibit.objects.filter(content_type=EQ_CT, object_id__in=comp_e).count() +
      ProducedExhibit.objects.filter(content_type=PQ_CT, object_id__in=comp_p).count())

# report des trames : composition -> ses parties atomiques
reports = defaultdict(set)      # (kind, pk_partie) -> {trame_pk}
for c in composees:
    if not c["trames"]:
        continue
    for a, _ in c["contient"]:
        if a["atomique"]:
            reports[(a["kind"], a["obj"].pk)].update(c["trames"])
nouveaux_liens = 0
for (kind, pk), tr in reports.items():
    model = EmailQuote if kind == "email" else PDFQuote
    existant = set(model.objects.get(pk=pk).trames_narratives.values_list("pk", flat=True))
    nouveaux_liens += len(tr - existant)

# ------------------------------------------------------------------ rapport
print("=" * 78)
print("PLAN")
print("=" * 78)
print(f"  citations actuelles          : {len(toutes)}  ({len(toutes)-len(composees)} atomiques, "
      f"{len(composees)} composées)")
print(f"  blocs à CRÉER                : {len(a_creer)}")
print(f"  compositions à SUPPRIMER     : {len(composees)}")
print(f"  liens trame portés par elles : {sum(len(c['trames']) for c in composees)}")
print(f"  → nouveaux liens sur les parties atomiques (report) : {nouveaux_liens}")
print(f"  nœuds LibraryNode visant une composition : {len(noeuds)}  (action : {args.noeuds})")
for n in noeuds:
    print(f"      node {n.pk} — doc {n.document_id} [{n.document.source_type}] {n.document.title[:40]}")
print(f"  lignes ProducedExhibit à régénérer : {pe}")
print()
print("  Blocs à créer, par composition :")
for c in sorted(composees, key=lambda x: x["id"]):
    if c["trous"]:
        print(f"    {c['id']:<8} {c['src']:<22} couverture {c['cov']:>4.0%}  "
              f"{len(c['trous'])} bloc(s)  trames {c['trames'] or '—'}")
        for frag in c["trous"]:
            apercu = " ".join(frag.split())[:88]
            print(f"        + {apercu}{'…' if len(frag) > 88 else ''}")

if args.dry_run:
    print()
    print("--dry-run : rien n'a été écrit.")
    sys.exit(0)

# ------------------------------------------------------------------ écriture
print()
print("=" * 78)
print("ÉCRITURE")
print("=" * 78)
with transaction.atomic():
    crees = []
    for c, frag in a_creer:
        src = c["obj"]
        if c["kind"] == "email":
            nouveau = EmailQuote.objects.create(email=src.email, quote_text=frag)
        else:
            nouveau = PDFQuote.objects.create(
                pdf_document=src.pdf_document, quote_text=frag,
                page_number=src.page_number,
                quote_location_details=(src.quote_location_details or "")[:255])
        if c["trames"]:
            nouveau.trames_narratives.set(c["trames"])
        crees.append((c["id"], c["kind"], nouveau.pk, len(frag)))
    print(f"  {len(crees)} bloc(s) créé(s)")

    for (kind, pk), tr in reports.items():
        model = EmailQuote if kind == "email" else PDFQuote
        model.objects.get(pk=pk).trames_narratives.add(*tr)
    print(f"  liens reportés sur {len(reports)} partie(s) atomique(s)")

    if noeuds:
        if args.noeuds == "supprimer":
            for n in noeuds:
                n.delete()
            print(f"  {len(noeuds)} nœud(s) LibraryNode supprimé(s)")
        elif args.noeuds == "repointer":
            n_ok = 0
            for n in noeuds:
                cible = next((c for c in composees
                              if c["obj"].pk == n.object_id
                              and ((c["kind"] == "email") == (n.content_type_id == EQ_CT.id))), None)
                parts = [a for a, _ in sorted(cible["contient"], key=lambda t: t[1][0][0])
                         if a["atomique"]] if cible else []
                if parts:
                    n.object_id = parts[0]["obj"].pk
                    n.save(update_fields=["object_id"])
                    n_ok += 1
            print(f"  {n_ok}/{len(noeuds)} nœud(s) repointé(s) vers leur première partie atomique")
        else:
            print(f"  {len(noeuds)} nœud(s) laissé(s) tels quels — ils pointeront dans le vide")

    n_e = EmailQuote.objects.filter(pk__in=comp_e).delete()
    n_p = PDFQuote.objects.filter(pk__in=comp_p).delete()
    print(f"  compositions supprimées : {n_e} / {n_p}")

print()
print(f"  citations en base : {EmailQuote.objects.count()} courriel + {PDFQuote.objects.count()} pdf")
print()
print("Étapes suivantes :")
print("  .venv/bin/python manage.py backfill_embeddings        # vectorise les nouveaux blocs")
print("  puis refresh_case_exhibits + rebuild_produced_exhibits")
print("  puis relancer decomposition_citations.py : 0 composition attendue")
