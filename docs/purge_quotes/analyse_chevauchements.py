#!/usr/bin/env python
"""
Analyse du chevauchement des citations, et du contexte dans lequel elles servent.

    .venv/bin/python docs/purge_quotes/analyse_chevauchements.py

Produit docs/purge_quotes/analyse_chevauchements.md.

Objet : distinguer, dans les 314 citations en base, les BLOCS SIMPLES (un passage
atomique, non decomposable) des COMPOSITIONS (un passage qui en contient un ou
plusieurs autres, ou qui recolle des fragments non contigus). La purge n'a d'interet
que si la reconstruction repart de blocs simples uniquement ; encore faut-il savoir
lesquels le sont deja.

Methode :
  - courriels : chaque citation est localisee dans le corps du courriel par ses
    OFFSETS (une citation elidee `A [...] B` donne deux segments). Le chevauchement
    est alors une question d'intervalles, pas de ressemblance.
  - PDF : le texte source n'est pas en base ; on se rabat sur l'inclusion de chaines
    entre citations d'un meme document.
  - contexte d'usage : pour chaque citation, les fichiers `legal/**/*.md` qui la
    reprennent, et les trames qui la citent.

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
OUT_PATH = Path(__file__).resolve().parent / "analyse_chevauchements.md"
sys.path.insert(0, str(BASE_DIR))
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django  # noqa: E402
django.setup()

from email_manager.models import Quote as EmailQuote  # noqa: E402
from pdf_manager.models import Quote as PDFQuote  # noqa: E402

ELISION = re.compile(r"\[\s*\.\.\.\s*\]|\(\s*\.\.\.\s*\)|\[\s*…\s*\]|\(\s*…\s*\)")
MIN_FRAG = 12  # un fragment plus court n'est pas localisable de facon fiable


def norm(s):
    s = unicodedata.normalize("NFKC", s or "")
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'),
                 ("«", '"'), ("»", '"'), ("–", "-"), ("—", "-"), (" ", " ")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip().lower()


def fragments(text):
    """Decoupe une citation en segments selon ses marqueurs d'elision."""
    return [f for f in (norm(p) for p in ELISION.split(text or "")) if len(f) >= MIN_FRAG]


# ============================================================ corpus .md
print("Lecture de legal/**/*.md ...")
md_files = sorted(LEGAL_DIR.rglob("*.md"))
md_texts = {}
for f in md_files:
    try:
        md_texts[f.relative_to(BASE_DIR)] = norm(f.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        pass
print(f"  {len(md_texts)} fichiers")


def md_usage(text, min_len=25):
    """Fichiers .md qui reprennent ce texte."""
    t = norm(text)
    if len(t) < min_len:
        return None  # trop court pour conclure
    return [str(p) for p, body in md_texts.items() if t in body]


# ============================================================ localisation des courriels
print("Localisation des citations de courriels dans leur source ...")
email_quotes = list(EmailQuote.objects.select_related("email").order_by("email_id", "pk"))
by_email = defaultdict(list)
for q in email_quotes:
    by_email[q.email_id].append(q)

located = {}      # pk -> [(start, end), ...]
unlocated = {}    # pk -> motif
for email_id, quotes in by_email.items():
    body = norm(quotes[0].email.body_plain_text if quotes[0].email else "")
    for q in quotes:
        frags = fragments(q.quote_text)
        if not body:
            unlocated[q.pk] = "corps du courriel vide en base"
            continue
        if not frags:
            unlocated[q.pk] = "citation trop courte pour etre localisee"
            continue
        spans, missing = [], 0
        for fr in frags:
            i = body.find(fr)
            if i < 0:
                missing += 1
            else:
                spans.append((i, i + len(fr)))
        if not spans:
            unlocated[q.pk] = "aucun segment retrouve dans le corps (texte recompose)"
        elif missing:
            located[q.pk] = sorted(spans)
            unlocated[q.pk] = f"{missing} segment(s) sur {len(frags)} introuvable(s)"
        else:
            located[q.pk] = sorted(spans)


def overlap(a, b):
    """Longueur du recouvrement entre deux listes d'intervalles."""
    total = 0
    for s1, e1 in a:
        for s2, e2 in b:
            total += max(0, min(e1, e2) - max(s1, s2))
    return total


def length(spans):
    return sum(e - s for s, e in spans)


def covers(outer, inner, tol=0.98):
    """outer recouvre-t-il au moins `tol` de inner ?"""
    li = length(inner)
    return li > 0 and overlap(outer, inner) / li >= tol


# ============================================================ relations entre citations
print("Calcul des relations de chevauchement ...")
relations = defaultdict(list)   # pk -> [(type, autre_pk, detail)]
for email_id, quotes in by_email.items():
    pks = [q.pk for q in quotes if q.pk in located]
    for i, a in enumerate(pks):
        for b in pks[i + 1:]:
            sa, sb = located[a], located[b]
            ov = overlap(sa, sb)
            if ov == 0:
                continue
            a_in_b = covers(sb, sa)
            b_in_a = covers(sa, sb)
            if a_in_b and b_in_a:
                relations[a].append(("identique", b, ""))
                relations[b].append(("identique", a, ""))
            elif a_in_b:
                relations[a].append(("incluse dans", b, f"{length(sa)}/{length(sb)} car."))
                relations[b].append(("contient", a, f"{length(sa)}/{length(sb)} car."))
            elif b_in_a:
                relations[b].append(("incluse dans", a, f"{length(sb)}/{length(sa)} car."))
                relations[a].append(("contient", b, f"{length(sb)}/{length(sa)} car."))
            else:
                pct = 100 * ov / min(length(sa), length(sb))
                relations[a].append(("chevauche", b, f"{ov} car. ({pct:.0f}%)"))
                relations[b].append(("chevauche", a, f"{ov} car. ({pct:.0f}%)"))

# ============================================================ PDF : inclusion de chaines
print("Analyse des citations PDF (inclusion de chaines) ...")
pdf_quotes = list(PDFQuote.objects.select_related("pdf_document").order_by("pdf_document_id", "page_number", "pk"))
by_pdf = defaultdict(list)
for q in pdf_quotes:
    by_pdf[q.pdf_document_id].append(q)

pdf_rel = defaultdict(list)
for doc_id, quotes in by_pdf.items():
    for i, qa in enumerate(quotes):
        for qb in quotes[i + 1:]:
            ta, tb = norm(qa.quote_text), norm(qb.quote_text)
            if not ta or not tb:
                continue
            if ta == tb:
                pdf_rel[qa.pk].append(("identique", qb.pk, ""))
                pdf_rel[qb.pk].append(("identique", qa.pk, ""))
            elif ta in tb:
                pdf_rel[qa.pk].append(("incluse dans", qb.pk, f"{len(ta)}/{len(tb)} car."))
                pdf_rel[qb.pk].append(("contient", qa.pk, f"{len(ta)}/{len(tb)} car."))
            elif tb in ta:
                pdf_rel[qb.pk].append(("incluse dans", qa.pk, f"{len(tb)}/{len(ta)} car."))
                pdf_rel[qa.pk].append(("contient", qb.pk, f"{len(tb)}/{len(ta)} car."))


def classify(pk, rels):
    kinds = {r[0] for r in rels.get(pk, [])}
    if "contient" in kinds and "incluse dans" in kinds:
        return "COMPOSITION (et incluse ailleurs)"
    if "contient" in kinds:
        return "COMPOSITION"
    if "incluse dans" in kinds:
        return "bloc simple, repris dans une composition"
    if "identique" in kinds:
        return "DOUBLON"
    if "chevauche" in kinds:
        return "CHEVAUCHEMENT PARTIEL"
    return "bloc simple isole"


# ============================================================ rapport
print("Redaction du rapport ...")
lines = []
add = lines.append
add("# Chevauchement des citations et contexte d'usage")
add("")
add("Généré par `docs/purge_quotes/analyse_chevauchements.py`. Lecture seule.")
add("")
add("Objet : séparer les **blocs simples** (un passage atomique) des **compositions** "
    "(un passage qui en contient d'autres, ou qui recolle des fragments non contigus). "
    "Une composition réintroduit sa prémisse comme citation distincte : c'est la perte de "
    "rigueur à corriger avant de reconstruire.")
add("")

cls_email = {q.pk: classify(q.pk, relations) for q in email_quotes if q.pk in located}
cls_pdf = {q.pk: classify(q.pk, pdf_rel) for q in pdf_quotes}
counts_e, counts_p = defaultdict(int), defaultdict(int)
for v in cls_email.values():
    counts_e[v] += 1
for v in cls_pdf.values():
    counts_p[v] += 1

add("## 1. Répartition")
add("")
add("| Classe | Courriels | PDF |")
add("|---|---|---|")
for k in ["COMPOSITION", "COMPOSITION (et incluse ailleurs)", "bloc simple, repris dans une composition",
          "CHEVAUCHEMENT PARTIEL", "DOUBLON", "bloc simple isolé".replace("é", "e")]:
    add(f"| {k} | {counts_e.get(k, 0)} | {counts_p.get(k, 0)} |")
add(f"| *non localisable dans la source* | {len(unlocated)} | — |")
add(f"| **total** | **{len(email_quotes)}** | **{len(pdf_quotes)}** |")
add("")
impliquees_e = sum(v for k, v in counts_e.items() if k != "bloc simple isole")
impliquees_p = sum(v for k, v in counts_p.items() if k != "bloc simple isole")
add(f"Citations engagées dans au moins une relation de recouvrement : "
    f"**{impliquees_e}** courriels, **{impliquees_p}** PDF.")
add("")
add("## 1bis. Ce que le corpus `.md` cite réellement, par classe")
add("")
add("Pour chaque classe, le nombre de fichiers `legal/**/*.md` qui reprennent la citation. "
    "C'est la mesure qui tranche : elle dit lesquelles de ces citations ont effectivement "
    "servi à l'analyse.")
add("")

import statistics  # noqa: E402


def usage_table(quotes, classes, label):
    buckets, zero = defaultdict(list), defaultdict(int)
    for q in quotes:
        u = md_usage(q.quote_text)
        if u is None:
            continue
        c = classes.get(q.pk, "non localisable (recomposée)")
        buckets[c].append(len(u))
        zero[c] += (len(u) == 0)
    add(f"**{label}**")
    add("")
    add("| Classe | n | médiane | moyenne | max | jamais citée |")
    add("|---|---|---|---|---|---|")
    for c, v in sorted(buckets.items(), key=lambda x: -statistics.median(x[1])):
        add(f"| {c} | {len(v)} | {statistics.median(v):.1f} | {statistics.mean(v):.1f} "
            f"| {max(v)} | {zero[c]} ({100 * zero[c] / len(v):.0f} %) |")
    add("")
    return buckets


usage_table(pdf_quotes, cls_pdf, "Citations de PDF")
usage_table(email_quotes, cls_email, "Citations de courriels")

add("Lecture : plus une classe est haut placée, plus ses citations irriguent l'analyse. "
    "Les **compositions** et les citations **recomposées à la main** sont en bas — elles "
    "n'ont, pour l'essentiel, jamais servi. Les blocs atomiques qu'une composition a avalés "
    "sont, eux, les plus repris. Le corpus `.md` a donc déjà adopté la méthode par blocs "
    "simples ; c'est la base qui est restée en arrière.")
add("")
add("---")
add("")

add("## 2. Détail par source")
add("")
add("Chaque groupe ci-dessous rassemble les citations d'une même source qui se recouvrent. "
    "`⊃` = contient, `⊂` = incluse dans, `≈` = chevauchement partiel, `=` = identique. "
    "La colonne *usage* indique le nombre de fichiers `.md` qui reprennent la citation et "
    "les trames qui la citent.")
add("")

SYM = {"contient": "⊃", "incluse dans": "⊂", "chevauche": "≈", "identique": "="}

add("### Courriels")
add("")
any_group = False
for email_id, quotes in sorted(by_email.items()):
    impliques = [q for q in quotes if relations.get(q.pk)]
    if not impliques:
        continue
    any_group = True
    e = quotes[0].email
    add(f"#### email-{email_id} — {(e.subject or '(sans objet)')[:70] if e else ''} "
        f"— {e.date_sent:%Y-%m-%d} " if e and e.date_sent else f"#### email-{email_id}")
    add("")
    for q in sorted(impliques, key=lambda x: (located.get(x.pk, [(0, 0)])[0][0], x.pk)):
        spans = located.get(q.pk, [])
        span_txt = ", ".join(f"[{s}:{e_}]" for s, e_ in spans)
        used = md_usage(q.quote_text)
        used_txt = "texte trop court" if used is None else f"{len(used)} fichier(s) .md"
        trames = sorted(t.pk for t in q.trames_narratives.all())
        add(f"- **eq-{q.pk}** — {cls_email.get(q.pk, '?')} — {length(spans)} car. {span_txt} "
            f"— usage : {used_txt}, trames {trames or '—'}")
        for kind, other, detail in sorted(relations[q.pk]):
            add(f"    - {SYM[kind]} eq-{other} {detail}")
        add(f"    - > {norm(q.quote_text)[:150]}")
    add("")
if not any_group:
    add("*Aucun recouvrement détecté.*")
    add("")

add("### PDF")
add("")
for doc_id, quotes in sorted(by_pdf.items()):
    impliques = [q for q in quotes if pdf_rel.get(q.pk)]
    if not impliques:
        continue
    d = quotes[0].pdf_document
    add(f"#### pdf-{doc_id} — {(d.title if d else '')[:70]}")
    add("")
    for q in sorted(impliques, key=lambda x: (x.page_number, x.pk)):
        used = md_usage(q.quote_text)
        used_txt = "texte trop court" if used is None else f"{len(used)} fichier(s) .md"
        trames = sorted(t.pk for t in q.trames_narratives.all())
        add(f"- **pq-{q.pk}** (p. {q.page_number}) — {cls_pdf.get(q.pk, '?')} "
            f"— {len(norm(q.quote_text))} car. — usage : {used_txt}, trames {trames or '—'}")
        for kind, other, detail in sorted(pdf_rel[q.pk]):
            add(f"    - {SYM[kind]} pq-{other} {detail}")
        add(f"    - > {norm(q.quote_text)[:150]}")
    add("")

add("---")
add("")
add("## 3. Citations non localisables dans leur source")
add("")
add("Leur texte ne se retrouve pas (ou pas entièrement) dans le corps stocké : recomposition "
    "manuelle, bloc cité, message transféré, ou corps vide. Elles échappent à l'analyse "
    "d'intervalles et doivent être tranchées à l'œil.")
add("")
for pk, motif in sorted(unlocated.items()):
    q = next((x for x in email_quotes if x.pk == pk), None)
    if not q:
        continue
    add(f"- **eq-{pk}** (email-{q.email_id}) — {motif}")
    add(f"    - > {norm(q.quote_text)[:150]}")
add("")

OUT_PATH.write_text("\n".join(lines), encoding="utf-8")

print()
print("=" * 78)
print(f"Ecrit : {OUT_PATH}")
print("=" * 78)
print("  COURRIELS")
for k, v in sorted(counts_e.items(), key=lambda x: -x[1]):
    print(f"    {k:<48} {v:>4}")
print(f"    {'non localisable dans la source':<48} {len(unlocated):>4}")
print("  PDF")
for k, v in sorted(counts_p.items(), key=lambda x: -x[1]):
    print(f"    {k:<48} {v:>4}")
