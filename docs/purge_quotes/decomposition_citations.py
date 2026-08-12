#!/usr/bin/env python
"""
Pour chaque citation : est-elle ATOMIQUE ou COMPOSÉE ? Si composée, ses parties
atomiques existent-elles en base, et peut-elle être reconstruite à partir d'elles ?

    .venv/bin/python docs/purge_quotes/decomposition_citations.py

Produit docs/purge_quotes/decomposition_citations.md.

Aucun embedding, aucune similarité : la question est exacte, la réponse aussi.

MÉTHODE

  Le texte de la citation examinée sert de repère. Toute autre citation de la même
  source qui s'y trouve littéralement occupe un intervalle [début, fin). L'union de
  ces intervalles, comparée à la longueur totale, donne le TAUX DE COUVERTURE.

  - couverture 100 %  -> la composition se reconstruit exactement à partir de blocs
                         qui existent déjà : elle est redondante, on peut la supprimer.
  - couverture < 100 % -> les portions non couvertes sont des passages qui n'existent
                         dans aucun bloc. Elles sont rendues verbatim : ce sont
                         exactement les blocs à créer pour rendre la composition
                         reconstructible.

  Deux couvertures sont calculées :
    · par TOUTES les sous-citations, y compris celles qui sont elles-mêmes composées ;
    · par les seules citations ATOMIQUES (celles qui ne contiennent rien d'autre).
  C'est la seconde qui répond à « reconstructible à partir de blocs simples ».

  La comparaison est insensible à la casse, aux apostrophes, guillemets, tirets et
  espaces multiples — mais les extraits affichés sont le texte ORIGINAL, pour être
  copiables tels quels.

Lecture seule.
"""
import os
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
OUT_PATH = Path(__file__).resolve().parent / "decomposition_citations.md"
sys.path.insert(0, str(BASE_DIR))
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django  # noqa: E402
django.setup()

from email_manager.models import Quote as EmailQuote  # noqa: E402
from pdf_manager.models import Quote as PDFQuote  # noqa: E402

TRIVIAL = 12          # une lacune plus courte n'est que ponctuation ou liaison
SUBST = {"’": "'", "‘": "'", "“": '"', "”": '"',
         "«": '"', "»": '"', "–": "-", "—": "-", " ": " "}


def canon(s):
    """Forme canonique + table de correspondance vers les positions d'origine."""
    out, idx, prev_space = [], [], True
    for i, ch in enumerate(s or ""):
        c = SUBST.get(ch, ch)
        c = unicodedata.normalize("NFKC", c)
        if c.isspace():
            if prev_space:
                continue
            out.append(" ")
            idx.append(i)
            prev_space = True
        else:
            out.append(c.lower())
            idx.append(i)
            prev_space = False
    return "".join(out), idx


def union(intervals):
    """Fusionne des intervalles [a,b) en une liste triée et disjointe."""
    if not intervals:
        return []
    intervals = sorted(intervals)
    merged = [list(intervals[0])]
    for a, b in intervals[1:]:
        if a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return [tuple(x) for x in merged]


def complement(spans, n):
    """Ce qui, dans [0,n), n'est couvert par aucun intervalle."""
    trous, curseur = [], 0
    for a, b in spans:
        if a > curseur:
            trous.append((curseur, a))
        curseur = max(curseur, b)
    if curseur < n:
        trous.append((curseur, n))
    return trous


def occurrences(hay, needle):
    """Toutes les positions de needle dans hay."""
    res, i = [], hay.find(needle)
    while i >= 0:
        res.append((i, i + len(needle)))
        i = hay.find(needle, i + 1)
    return res


# ------------------------------------------------------------------ chargement
print("Chargement ...")
groupes = defaultdict(list)          # (corpus, id_source) -> [citation, ...]
for q in PDFQuote.objects.select_related("pdf_document").all():
    groupes[("pdf", q.pdf_document_id)].append({
        "id": f"pq-{q.pk}", "pk": q.pk, "raw": q.quote_text or "",
        "src": f"pdf-{q.pdf_document_id} p.{q.page_number}",
        "titre": (q.pdf_document.title if q.pdf_document else ""),
        "trames": sorted(t.pk for t in q.trames_narratives.all())})
for q in EmailQuote.objects.select_related("email").all():
    e = q.email
    groupes[("email", q.email_id)].append({
        "id": f"eq-{q.pk}", "pk": q.pk, "raw": q.quote_text or "",
        "src": f"email-{q.email_id}",
        "titre": ((e.subject or "(sans objet)") if e else ""),
        "trames": sorted(t.pk for t in q.trames_narratives.all())})

toutes = [c for lst in groupes.values() for c in lst]
for c in toutes:
    c["canon"], c["map"] = canon(c["raw"])
print(f"  {len(toutes)} citations réparties sur {len(groupes)} sources")

# ------------------------------------------------------------------ inclusions
print("Recherche des inclusions ...")
for cle, lst in groupes.items():
    for c in lst:
        c["contient"] = []           # (autre, [intervalles dans c])
        c["incluse_dans"] = []
    for c in lst:
        if not c["canon"]:
            continue
        for autre in lst:
            if autre is c or not autre["canon"]:
                continue
            if len(autre["canon"]) >= len(c["canon"]):
                continue             # ne peut pas être une partie stricte
            occ = occurrences(c["canon"], autre["canon"])
            if occ:
                c["contient"].append((autre, occ))
                autre["incluse_dans"].append(c)

# ------------------------------------------------------------------ classement
for c in toutes:
    c["atomique"] = not c["contient"]

for c in toutes:
    n = len(c["canon"])
    # couverture par toutes les sous-citations
    spans_all = union([iv for _, occ in c["contient"] for iv in occ])
    # couverture par les seules sous-citations atomiques
    spans_at = union([iv for autre, occ in c["contient"] if autre["atomique"] for iv in occ])
    c["cov_all"] = (sum(b - a for a, b in spans_all) / n) if n else 0.0
    c["cov_at"] = (sum(b - a for a, b in spans_at) / n) if n else 0.0
    c["spans_at"] = spans_at
    trous = complement(spans_at, n)
    c["trous"] = []
    for a, b in trous:
        if b - a <= TRIVIAL:
            continue
        deb = c["map"][a] if a < len(c["map"]) else len(c["raw"])
        fin = c["map"][b - 1] + 1 if b - 1 < len(c["map"]) else len(c["raw"])
        frag = c["raw"][deb:fin].strip()
        if len(frag) > TRIVIAL:
            c["trous"].append(frag)

composees = [c for c in toutes if not c["atomique"]]
atomiques = [c for c in toutes if c["atomique"]]
# Le critere n'est pas un pourcentage mais l'existence de texte reellement absent :
# une composition couverte a 99 % dont le manque est une virgule ou un « et » se
# reconstruit sans rien creer. Seules les lacunes de plus de TRIVIAL caracteres
# comptent.
exactes = [c for c in composees if not c["trous"]]
partielles = [c for c in composees if c["trous"]]
premisses = [c for c in atomiques if c["incluse_dans"]]

print(f"  atomiques : {len(atomiques)}  (dont {len(premisses)} servent de prémisse)")
print(f"  composées : {len(composees)}  (dont {len(exactes)} reconstructibles à 100 %)")

# ------------------------------------------------------------------ rapport
L = []
add = L.append
add("# Citations atomiques et compositions — reconstructibilité")
add("")
add("Généré par `docs/purge_quotes/decomposition_citations.py`. Lecture seule.")
add("")
add("Une citation est **atomique** si aucune autre citation de la même source ne s'y trouve "
    "incluse. Elle est **composée** sinon. Pour chaque composition, on mesure quelle part de "
    "son texte est déjà couverte par des blocs atomiques existants : c'est le taux qui dit "
    "si elle peut être reconstruite sans rien créer.")
add("")
add("| | |")
add("|---|---|")
add(f"| citations examinées | {len(toutes)} |")
add(f"| **atomiques** | **{len(atomiques)}** |")
add(f"| — dont reprises comme prémisse d'une composition | {len(premisses)} |")
add(f"| **composées** | **{len(composees)}** |")
add(f"| — **reconstructibles sans rien créer** | **{len(exactes)}** |")
add(f"| — exigeant la création d\'au moins un bloc | {len(partielles)} |")
add("")
add("Une composition est dite **reconstructible sans rien créer** quand tout son texte se "
    f"retrouve dans des blocs atomiques existants, aux liaisons près (moins de {TRIVIAL} "
    "caractères : ponctuation, conjonction, marqueur d\'élision). Ce n\'est pas un seuil de "
    "pourcentage, c\'est l\'absence de passage réellement manquant.")
add("")
add(f"Les {len(exactes)} compositions ainsi couvertes sont **redondantes** : leur contenu "
    "existe déjà, réparti en blocs simples. Elles peuvent disparaître sans perte. Les "
    f"{len(partielles)} autres contiennent des passages qui ne sont dans aucun bloc — rendus "
    "verbatim ci-dessous, ce sont exactement les blocs à créer.")
add("")
add("---")
add("")

add(f"## 1. Compositions reconstructibles sans rien créer ({len(exactes)})")
add("")
add("Supprimer ces compositions ne fait perdre aucun texte : tout leur contenu existe "
    "déjà en blocs atomiques.")
add("")
add("| id | source | longueur | couverture | parties atomiques | trames |")
add("|---|---|---|---|---|---|")
for c in sorted(exactes, key=lambda x: -len(x["canon"])):
    parts = ", ".join(f"`{a['id']}`" for a, _ in sorted(c["contient"], key=lambda t: t[1][0][0])
                      if a["atomique"])
    add(f"| `{c['id']}` | {c['src']} | {len(c['raw'])} car. | {c['cov_at']:.0%} | {parts} | "
        f"{','.join(str(t) for t in c['trames']) or '—'} |")
add("")

add(f"## 2. Compositions incomplètes ({len(partielles)})")
add("")
add("Chacune porte un ou plusieurs passages absents de tout bloc atomique. Le texte de ces "
    "manques est donné tel quel : c'est le contenu des blocs à créer pour rendre la "
    "composition reconstructible — après quoi elle devient elle aussi supprimable.")
add("")
for c in sorted(partielles, key=lambda x: (-x["cov_at"], -len(x["canon"]))):
    add(f"### `{c['id']}` — {c['src']} — couverture atomique **{c['cov_at']:.0%}**")
    add("")
    add(f"- **{len(c['raw'])} caractères**, trames "
        f"{', '.join(str(t) for t in c['trames']) or '—'}")
    if c["cov_all"] > c["cov_at"] + 0.005:
        add(f"- couverture par *toutes* les sous-citations : {c['cov_all']:.0%} — l'écart "
            "vient de sous-citations elles-mêmes composées")
    parts = [a for a, _ in sorted(c["contient"], key=lambda t: t[1][0][0])]
    if parts:
        add("- **parties déjà en base** : " + ", ".join(
            f"`{a['id']}`" + ("" if a["atomique"] else " *(composée)*") for a in parts))
    else:
        add("- **aucune partie en base**")
    add("")
    add(f"- **{len(c['trous'])} passage(s) à créer** :")
    add("")
    for frag in c["trous"]:
        add("```text")
        add(frag)
        add("```")
        add("")

add("---")
add("")
add(f"## 3. Blocs atomiques servant de prémisse ({len(premisses)})")
add("")
add("Ces blocs sont corrects tels quels. Ils sont listés parce qu'une ou plusieurs "
    "compositions les répètent — c'est la redondance à supprimer.")
add("")
add("| id | source | longueur | repris dans | trames |")
add("|---|---|---|---|---|")
for c in sorted(premisses, key=lambda x: -len(x["incluse_dans"])):
    dans = ", ".join(f"`{p['id']}`" for p in c["incluse_dans"])
    add(f"| `{c['id']}` | {c['src']} | {len(c['raw'])} car. | {dans} | "
        f"{','.join(str(t) for t in c['trames']) or '—'} |")
add("")

isoles = [c for c in atomiques if not c["incluse_dans"]]
add(f"## 4. Blocs atomiques isolés ({len(isoles)})")
add("")
add("Atomiques et repris par aucune composition : rien à faire.")
add("")

OUT_PATH.write_text("\n".join(L), encoding="utf-8")
print(f"\nEcrit : {OUT_PATH}")
print(f"  atomiques isoles          : {len(isoles)}")
print(f"  atomiques premisses       : {len(premisses)}")
print(f"  composees exactes         : {len(exactes)}")
print(f"  composees incompletes     : {len(partielles)}")
print(f"  passages a creer au total : {sum(len(c['trous']) for c in partielles)}")
