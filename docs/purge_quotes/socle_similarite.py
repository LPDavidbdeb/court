#!/usr/bin/env python
"""
Socle élargi : appariement par SIMILARITÉ plutôt que par égalité stricte.

    .venv/bin/python docs/purge_quotes/socle_similarite.py

Produit docs/purge_quotes/socle_similarite.md.

`socle_citations.py` répond à « ce texte apparaît-il mot pour mot dans un .md ? ».
Il rate donc les citations que l'analyse a reprises en les tronquant, en les
paraphrasant autour d'un noyau, ou en n'en gardant qu'un fragment.

Méthode : n-grammes de mots (n=4). Pour chaque citation, on mesure la part de ses
4-grammes présents dans un même fichier .md — c'est le TAUX DE REPRISE. Un taux de
1.0 signifie que toute la citation se retrouve, dans l'ordre local, dans ce fichier ;
0.5 qu'une moitié y est. Le meilleur fichier et l'extrait correspondant sont reportés
pour que la décision reste vérifiable à l'œil.

Paliers retenus :
    >= 0.85  reprise quasi intégrale (édition mineure)
    >= 0.60  largement reprise            -> socle élargi
    >= 0.35  noyau repris, reste absent   -> à trancher
    >= 0.15  écho faible                  -> probablement fortuit
    <  0.15  absente

Lecture seule sur la base et sur le corpus.
"""
import os
import re
import sys
import unicodedata
from collections import defaultdict, Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
LEGAL_DIR = BASE_DIR / "legal"
OUT_PATH = Path(__file__).resolve().parent / "socle_similarite.md"
sys.path.insert(0, str(BASE_DIR))
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django  # noqa: E402
django.setup()

from email_manager.models import Quote as EmailQuote  # noqa: E402
from pdf_manager.models import Quote as PDFQuote  # noqa: E402

ELISION = re.compile(r"\[\s*\.\.\.\s*\]|\(\s*\.\.\.\s*\)|\[\s*…\s*\]|\(\s*…\s*\)")
N = 4              # taille du n-gramme, en mots
MIN_WORDS = 6      # en deçà, la mesure n'a pas de sens
MIN_LEN = 25
SEUILS = [(0.85, "reprise quasi intégrale"), (0.60, "largement reprise"),
          (0.35, "noyau repris"), (0.15, "écho faible"), (0.0, "absente")]


def norm(s):
    s = unicodedata.normalize("NFKC", s or "")
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'),
                 ("«", '"'), ("»", '"'), ("–", "-"), ("—", "-"), (" ", " ")):
        s = s.replace(a, b)
    s = ELISION.sub(" ", s)
    s = re.sub(r"[^\w\s'-]", " ", s, flags=re.UNICODE)
    return re.sub(r"\s+", " ", s).strip().lower()


def grams(words, n=N):
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def palier(score):
    for seuil, nom in SEUILS:
        if score >= seuil:
            return nom
    return "absente"


# ---------------------------------------------------------------- citations
print("Chargement des citations ...")
cands = []
for q in PDFQuote.objects.select_related("pdf_document").all():
    w = norm(q.quote_text).split()
    if len(w) < MIN_WORDS:
        continue
    cands.append({"id": f"pq-{q.pk}", "pk": q.pk, "kind": "pdf", "obj": q, "words": w,
                  "grams": grams(w), "raw": q.quote_text,
                  "src": f"pdf-{q.pdf_document_id} p.{q.page_number}",
                  "titre": q.pdf_document.title if q.pdf_document else "",
                  "trames": sorted(t.pk for t in q.trames_narratives.all())})
for q in EmailQuote.objects.select_related("email").all():
    w = norm(q.quote_text).split()
    if len(w) < MIN_WORDS:
        continue
    e = q.email
    cands.append({"id": f"eq-{q.pk}", "pk": q.pk, "kind": "email", "obj": q, "words": w,
                  "grams": grams(w), "raw": q.quote_text,
                  "src": f"email-{q.email_id}",
                  "titre": (e.subject or "(sans objet)") if e else "",
                  "trames": sorted(t.pk for t in q.trames_narratives.all())})
print(f"  {len(cands)} citations mesurables (>= {MIN_WORDS} mots)")

# strict : le texte apparaît mot pour mot
print("Calcul du socle strict (pour comparaison) ...")
raw_corpus = []
for f in sorted(LEGAL_DIR.rglob("*.md")):
    try:
        raw_corpus.append(re.sub(r"\s+", " ", unicodedata.normalize("NFKC",
                          f.read_text(encoding="utf-8", errors="replace"))
                          .replace("’", "'").replace("«", '"').replace("»", '"')).strip().lower())
    except Exception:
        pass
strict = set()
for c in cands:
    t = re.sub(r"\s+", " ", unicodedata.normalize("NFKC", c["raw"])
               .replace("’", "'").replace("«", '"').replace("»", '"')).strip().lower()
    if len(t) >= MIN_LEN and any(t in b for b in raw_corpus):
        strict.add(c["id"])
print(f"  socle strict : {len(strict)}")

# ---------------------------------------------------------------- balayage
print("Balayage du corpus par n-grammes ...")
best = {c["id"]: {"score": 0.0, "file": None, "hits": 0, "excerpt": ""} for c in cands}
files = sorted(LEGAL_DIR.rglob("*.md"))
for k, f in enumerate(files, 1):
    if k % 100 == 0:
        print(f"  {k}/{len(files)}")
    try:
        words = norm(f.read_text(encoding="utf-8", errors="replace")).split()
    except Exception:
        continue
    if len(words) < N:
        continue
    index = defaultdict(list)
    for i in range(len(words) - N + 1):
        index[" ".join(words[i:i + N])].append(i)
    rel = str(f.relative_to(BASE_DIR))
    for c in cands:
        positions = [index[g][0] for g in c["grams"] if g in index]
        if not positions:
            continue
        score = len(positions) / len(c["grams"])
        if score > best[c["id"]]["score"]:
            lo, hi = min(positions), max(positions) + N
            span = words[max(0, lo - 3):min(len(words), hi + 3)]
            if len(span) > 60:
                span = span[:30] + ["[…]"] + span[-30:]
            best[c["id"]] = {"score": score, "file": rel,
                             "hits": len(positions), "excerpt": " ".join(span)}

# ---------------------------------------------------------------- rapport
for c in cands:
    b = best[c["id"]]
    c["score"] = b["score"]
    c["file"] = b["file"]
    c["excerpt"] = b["excerpt"]
    c["palier"] = palier(b["score"])
    c["strict"] = c["id"] in strict

cands.sort(key=lambda c: -c["score"])

par_palier = Counter(c["palier"] for c in cands)
nouveaux = [c for c in cands if not c["strict"] and c["score"] >= 0.60]
a_trancher = [c for c in cands if not c["strict"] and 0.35 <= c["score"] < 0.60]

L = []
add = L.append
add("# Socle élargi — appariement par similarité")
add("")
add("Généré par `docs/purge_quotes/socle_similarite.py`. Lecture seule.")
add("")
add(f"Mesure : part des **{N}-grammes de mots** d'une citation retrouvés dans un même "
    "fichier `legal/**/*.md` (*taux de reprise*). Contrairement au socle strict, cette "
    "mesure attrape les citations tronquées, remaniées, ou dont l'analyse n'a gardé qu'un "
    "noyau. Les citations de moins de "
    f"{MIN_WORDS} mots sont écartées : la mesure n'y a pas de sens.")
add("")
add("| Palier | Taux | Citations |")
add("|---|---|---|")
for seuil, nom in SEUILS:
    add(f"| {nom} | ≥ {seuil:.2f} | {par_palier.get(nom, 0)} |")
add(f"| **total mesurable** | | **{len(cands)}** |")
add("")
add(f"- socle **strict** (texte mot pour mot) : **{len(strict)}** citations ;")
add(f"- **+{len(nouveaux)}** citations atteignent un taux ≥ 0,60 sans être dans le socle "
    "strict → **socle élargi** ;")
add(f"- **{len(a_trancher)}** citations entre 0,35 et 0,60 → à trancher à l'œil.")
add("")
add("---")
add("")

add(f"## 1. Nouvelles entrées du socle ({len(nouveaux)}) — taux ≥ 0,60, absentes du socle strict")
add("")
add("Ces citations ont bel et bien servi à l'analyse : leur texte y figure remanié, tronqué "
    "ou fondu dans la phrase. L'égalité stricte les manquait.")
add("")
add("| id | source | taux | trames | fichier .md | passage en base |")
add("|---|---|---|---|---|---|")
for c in nouveaux:
    txt = " ".join(c["words"])[:95].replace("|", "\\|")
    tr = ",".join(str(t) for t in c["trames"]) or "—"
    add(f"| `{c['id']}` | {c['src']} | **{c['score']:.2f}** | {tr} | `{c['file']}` | {txt}… |")
add("")
add("### Détail (citation en base vs extrait du .md)")
add("")
for c in nouveaux:
    add(f"#### `{c['id']}` — {c['src']} — taux {c['score']:.2f} — `{c['file']}`")
    add("")
    add("- **en base :**")
    add("")
    add("  ```text")
    for line in c["raw"].splitlines() or [""]:
        add(f"  {line}")
    add("  ```")
    add("")
    add("- **dans le `.md` :**")
    add("")
    add("  ```text")
    add(f"  {c['excerpt']}")
    add("  ```")
    add("")

add("---")
add("")
add(f"## 2. À trancher ({len(a_trancher)}) — taux entre 0,35 et 0,60")
add("")
add("Un noyau de la citation se retrouve dans le `.md`, le reste non. Soit l'analyse n'a "
    "retenu qu'une partie du passage — auquel cas **c'est cette partie qui est le bloc "
    "atomique** —, soit la correspondance est fortuite.")
add("")
add("| id | source | taux | trames | fichier .md | passage en base | extrait .md |")
add("|---|---|---|---|---|---|---|")
for c in a_trancher:
    txt = " ".join(c["words"])[:70].replace("|", "\\|")
    exc = c["excerpt"][:70].replace("|", "\\|")
    tr = ",".join(str(t) for t in c["trames"]) or "—"
    add(f"| `{c['id']}` | {c['src']} | {c['score']:.2f} | {tr} | `{c['file']}` | {txt}… | {exc}… |")
add("")

add("---")
add("")
add("## 3. Tableau complet, par taux décroissant")
add("")
add("| id | source | taux | palier | strict | trames | meilleur fichier .md |")
add("|---|---|---|---|---|---|---|")
for c in cands:
    tr = ",".join(str(t) for t in c["trames"]) or "—"
    add(f"| `{c['id']}` | {c['src']} | {c['score']:.2f} | {c['palier']} | "
        f"{'oui' if c['strict'] else '—'} | {tr} | "
        f"{('`' + c['file'] + '`') if c['file'] else '—'} |")
add("")

OUT_PATH.write_text("\n".join(L), encoding="utf-8")

print()
print("=" * 78)
print(f"Ecrit : {OUT_PATH}")
print("=" * 78)
for seuil, nom in SEUILS:
    print(f"  {nom:<28} (>= {seuil:.2f}) : {par_palier.get(nom, 0):>4}")
print(f"  socle strict                     : {len(strict)}")
print(f"  nouvelles entrees (>= 0.60)      : {len(nouveaux)}")
print(f"  a trancher (0.35 - 0.60)         : {len(a_trancher)}")
print(f"  socle elargi                     : {len(strict) + len(nouveaux)}")
