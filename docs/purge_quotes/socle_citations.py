#!/usr/bin/env python
"""
Liste le SOCLE : les citations dont le texte est effectivement repris dans
`legal/**/*.md`. Ce sont celles qui ont servi à l'analyse.

    .venv/bin/python docs/purge_quotes/socle_citations.py

Produit docs/purge_quotes/socle_citations.md.

Pour chaque citation : sa source, sa classe de chevauchement (bloc simple /
composition / doublon), le nombre et le nom des fichiers .md qui la reprennent,
les trames qui la citent, et son texte.

Les citations de moins de 25 caractères sont écartées : une correspondance sur
un texte aussi court ne prouve rien.

Lecture seule sur la base et sur le corpus.
"""
import os
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
LEGAL_DIR = BASE_DIR / "legal"
OUT_PATH = Path(__file__).resolve().parent / "socle_citations.md"
sys.path.insert(0, str(BASE_DIR))
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django  # noqa: E402
django.setup()

from email_manager.models import Quote as EmailQuote  # noqa: E402
from pdf_manager.models import Quote as PDFQuote  # noqa: E402

ELISION = re.compile(r"\[\s*\.\.\.\s*\]|\(\s*\.\.\.\s*\)|\[\s*…\s*\]|\(\s*…\s*\)")
MIN_LEN = 25
MIN_FRAG = 12


def norm(s):
    s = unicodedata.normalize("NFKC", s or "")
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'),
                 ("«", '"'), ("»", '"'), ("–", "-"), ("—", "-"), (" ", " ")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip().lower()


def fragments(text):
    return [f for f in (norm(p) for p in ELISION.split(text or "")) if len(f) >= MIN_FRAG]


print("Lecture de legal/**/*.md ...")
md = {}
for f in sorted(LEGAL_DIR.rglob("*.md")):
    try:
        md[str(f.relative_to(BASE_DIR))] = norm(f.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        pass
print(f"  {len(md)} fichiers")


def usage(text):
    t = norm(text)
    if len(t) < MIN_LEN:
        return None
    return sorted(p for p, body in md.items() if t in body)


# ---------------------------------------------------------------- classification
print("Classification des chevauchements ...")

email_quotes = list(EmailQuote.objects.select_related("email", "email__sender_protagonist").all())
by_email = defaultdict(list)
for q in email_quotes:
    by_email[q.email_id].append(q)

located, kinds_e = {}, defaultdict(set)
for eid, qs in by_email.items():
    body = norm(qs[0].email.body_plain_text if qs[0].email else "")
    for q in qs:
        fr = fragments(q.quote_text)
        if not body or not fr:
            continue
        spans = [(i, i + len(f)) for f in fr if (i := body.find(f)) >= 0]
        if spans:
            located[q.pk] = sorted(spans)

def _len(s):
    return sum(e - b for b, e in s)

def _ov(a, b):
    return sum(max(0, min(e1, e2) - max(s1, s2)) for s1, e1 in a for s2, e2 in b)

for eid, qs in by_email.items():
    pks = [q.pk for q in qs if q.pk in located]
    for i, a in enumerate(pks):
        for b in pks[i + 1:]:
            sa, sb = located[a], located[b]
            o = _ov(sa, sb)
            if not o:
                continue
            ain = _len(sa) and o / _len(sa) >= 0.98
            bin_ = _len(sb) and o / _len(sb) >= 0.98
            if ain and bin_:
                kinds_e[a].add("identique"); kinds_e[b].add("identique")
            elif ain:
                kinds_e[a].add("incluse"); kinds_e[b].add("contient")
            elif bin_:
                kinds_e[b].add("incluse"); kinds_e[a].add("contient")
            else:
                kinds_e[a].add("partiel"); kinds_e[b].add("partiel")

pdf_quotes = list(PDFQuote.objects.select_related("pdf_document", "pdf_document__author").all())
by_pdf = defaultdict(list)
for q in pdf_quotes:
    by_pdf[q.pdf_document_id].append(q)

kinds_p = defaultdict(set)
for did, qs in by_pdf.items():
    for i, qa in enumerate(qs):
        for qb in qs[i + 1:]:
            ta, tb = norm(qa.quote_text), norm(qb.quote_text)
            if not ta or not tb:
                continue
            if ta == tb:
                kinds_p[qa.pk].add("identique"); kinds_p[qb.pk].add("identique")
            elif ta in tb:
                kinds_p[qa.pk].add("incluse"); kinds_p[qb.pk].add("contient")
            elif tb in ta:
                kinds_p[qb.pk].add("incluse"); kinds_p[qa.pk].add("contient")


def label(pk, kinds, localisable=True):
    k = kinds.get(pk, set())
    if not localisable:
        return "recomposée"
    if "contient" in k and "incluse" in k:
        return "COMPOSITION (et incluse ailleurs)"
    if "contient" in k:
        return "COMPOSITION"
    if "incluse" in k:
        return "bloc simple (repris dans une composition)"
    if "identique" in k:
        return "doublon"
    if "partiel" in k:
        return "chevauchement partiel"
    return "bloc simple"


# ---------------------------------------------------------------- socle
rows_p, rows_e = [], []
for q in pdf_quotes:
    u = usage(q.quote_text)
    if not u:
        continue
    d = q.pdf_document
    rows_p.append({
        "id": f"pq-{q.pk}", "pk": q.pk, "n": len(u), "files": u,
        "src": f"pdf-{q.pdf_document_id} p.{q.page_number}",
        "titre": (d.title if d else ""), "auteur": (d.author.get_full_name() if d and d.author else ""),
        "date": (d.document_date.isoformat() if d and d.document_date else ""),
        "cls": label(q.pk, kinds_p),
        "trames": sorted(t.pk for t in q.trames_narratives.all()),
        "txt": norm(q.quote_text), "raw": q.quote_text,
    })

for q in email_quotes:
    u = usage(q.quote_text)
    if not u:
        continue
    e = q.email
    rows_e.append({
        "id": f"eq-{q.pk}", "pk": q.pk, "n": len(u), "files": u,
        "src": f"email-{q.email_id}",
        "titre": (e.subject or "(sans objet)") if e else "",
        "auteur": (e.sender_protagonist.get_full_name() if e and e.sender_protagonist else (e.sender if e else "")),
        "date": (e.date_sent.strftime("%Y-%m-%d") if e and e.date_sent else ""),
        "cls": label(q.pk, kinds_e, localisable=q.pk in located),
        "trames": sorted(t.pk for t in q.trames_narratives.all()),
        "txt": norm(q.quote_text), "raw": q.quote_text,
    })

rows_p.sort(key=lambda r: (-r["n"], r["pk"]))
rows_e.sort(key=lambda r: (-r["n"], r["pk"]))

# passages distincts (les doublons partagent un texte)
distinct_p = {r["txt"] for r in rows_p}
distinct_e = {r["txt"] for r in rows_e}

# ---------------------------------------------------------------- rapport
L = []
add = L.append
add("# Le socle — citations effectivement reprises dans `legal/**/*.md`")
add("")
add("Généré par `docs/purge_quotes/socle_citations.py`. Lecture seule.")
add("")
add("Une citation entre dans le socle si son texte normalisé (≥ 25 caractères) apparaît "
    "dans au moins un fichier `legal/**/*.md`. C'est le sous-ensemble qui a servi à "
    "l'analyse, et donc le point de départ de la reconstruction.")
add("")
add("| | lignes en base | **passages distincts** |")
add("|---|---|---|")
add(f"| PDF | {len(rows_p)} | **{len(distinct_p)}** |")
add(f"| courriels | {len(rows_e)} | **{len(distinct_e)}** |")
add(f"| **total** | **{len(rows_p) + len(rows_e)}** | **{len(distinct_p) + len(distinct_e)}** |")
add("")
add("L'écart entre les deux colonnes, ce sont les doublons exacts : le même passage saisi "
    "deux ou trois fois. À la reconstruction, un seul bloc par passage distinct.")
add("")

cnt = defaultdict(lambda: [0, 0])
for r in rows_p:
    cnt[r["cls"]][0] += 1
for r in rows_e:
    cnt[r["cls"]][1] += 1
add("| Classe dans le socle | PDF | courriels |")
add("|---|---|---|")
for k in sorted(cnt, key=lambda x: -(cnt[x][0] + cnt[x][1])):
    add(f"| {k} | {cnt[k][0]} | {cnt[k][1]} |")
add("")
comp = [r for r in rows_p + rows_e if r["cls"].startswith("COMPOSITION")]
add(f"**{len(comp)} compositions figurent dans le socle** — ce sont celles à décomposer en "
    "prémisses atomiques avant de reconstruire : "
    + ", ".join(r["id"] for r in comp) + ".")
add("")
add("---")
add("")


def table(rows, titre):
    add(f"## {titre}")
    add("")
    add("| # | id | source | date | .md | trames | classe | passage |")
    add("|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        txt = r["txt"].replace("|", "\\|")
        txt = txt[:110] + ("…" if len(r["txt"]) > 110 else "")
        tr = ",".join(str(t) for t in r["trames"]) or "—"
        add(f"| {i} | `{r['id']}` | {r['src']} | {r['date']} | **{r['n']}** | {tr} | {r['cls']} | {txt} |")
    add("")


table(rows_p, f"Citations de PDF ({len(rows_p)})")
table(rows_e, f"Citations de courriels ({len(rows_e)})")

add("---")
add("")
add("## Détail : où chaque citation est reprise")
add("")
for rows, t in ((rows_p, "PDF"), (rows_e, "Courriels")):
    add(f"### {t}")
    add("")
    for r in rows:
        add(f"#### `{r['id']}` — {r['src']} — {r['n']} fichier(s) — *{r['cls']}*")
        add("")
        add(f"- **Source :** {r['titre'][:80]} — {r['auteur']} — {r['date']}")
        add(f"- **Trames :** {', '.join(str(x) for x in r['trames']) or '—'}")
        add(f"- **Repris dans :** {', '.join('`' + f + '`' for f in r['files'])}")
        add("")
        add("```text")
        add(r["raw"])
        add("```")
        add("")

OUT_PATH.write_text("\n".join(L), encoding="utf-8")

print()
print(f"Ecrit : {OUT_PATH}")
print(f"  PDF       : {len(rows_p)} lignes / {len(distinct_p)} passages distincts")
print(f"  courriels : {len(rows_e)} lignes / {len(distinct_e)} passages distincts")
print(f"  TOTAL     : {len(rows_p) + len(rows_e)} lignes / {len(distinct_p) + len(distinct_e)} passages distincts")
print(f"  compositions dans le socle : {len(comp)} -> {[r['id'] for r in comp]}")
