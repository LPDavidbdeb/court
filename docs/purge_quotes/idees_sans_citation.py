#!/usr/bin/env python
"""
Détecte les IDÉES SANS CITATION : les passages de `legal/**/*.md` qui affirment
quelque chose sans l'étayer, alors qu'une citation existe en base pour le faire.

    .venv/bin/python docs/purge_quotes/idees_sans_citation.py
    .venv/bin/python docs/purge_quotes/idees_sans_citation.py --min-score 3.0 --top 400

Produit docs/purge_quotes/idees_sans_citation.md.

Méthode, en trois temps :

1. DÉCOUPAGE — le corpus est découpé en paragraphes. Les blocs verbatim
   (```text, citations `>`), les tableaux et les titres sont retirés : ce ne sont
   pas des idées, ce sont des supports ou de la structure.

2. ÉTAYAGE — un paragraphe est dit ÉTAYÉ s'il porte lui-même une marque de
   citation (« … », cote P-n, renvoi `piece_…`, `eq-`/`pq-`) ou s'il est
   immédiatement suivi d'un bloc verbatim. Il est en outre écarté du corpus des
   idées s'il REPRODUIT une citation (recouvrement de 4-grammes >= --repro) :
   dans ce cas ce n'est pas une idée, c'est le support lui-même — cas des fiches
   `piece_*.md` qui portent le verbatim intégral hors bloc de code.
   Le reste est NON ÉTAYÉ, et c'est un candidat.

3. APPARIEMENT — chaque paragraphe non étayé est confronté aux 314 citations de
   la base par recouvrement de TERMES DISTINCTIFS : les mots rares à l'échelle du
   corpus pèsent, les mots courants ne pèsent rien (pondération idf, seuils
   dérivés du corpus lui-même — aucune liste de mots-vides à maintenir).

Le score n'est pas une preuve de pertinence : c'est un ordre de lecture. Chaque
paire est rendue avec les termes qui l'ont déclenchée, pour que l'arbitrage reste
le vôtre.

Lecture seule sur la base et sur le corpus.
"""
import argparse
import math
import os
import re
import sys
import unicodedata
from collections import defaultdict, Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
LEGAL_DIR = BASE_DIR / "legal"
OUT_PATH = Path(__file__).resolve().parent / "idees_sans_citation.md"
sys.path.insert(0, str(BASE_DIR))
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django  # noqa: E402
django.setup()

from email_manager.models import Quote as EmailQuote  # noqa: E402
from pdf_manager.models import Quote as PDFQuote  # noqa: E402

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--min-score", type=float, default=3.0, help="score idf minimal pour retenir une paire")
ap.add_argument("--top", type=int, default=300, help="nombre de paires détaillées dans le rapport")
ap.add_argument("--min-words", type=int, default=15, help="longueur minimale d'un paragraphe-idée")
ap.add_argument("--max-df", type=float, default=0.25, help="un terme présent dans plus de X%% des fichiers est ignoré")
ap.add_argument("--repro", type=float, default=0.35,
                help="au-dessus de ce taux de reprise, le paragraphe reproduit la citation : ce n'est pas une idée")
ap.add_argument("--min-cov", type=float, default=0.25,
                help="part minimale du poids de la citation couverte par le paragraphe")
ap.add_argument("--semantique", action="store_true",
                help="ajoute un appariement par embeddings multilingues (rattrape les reformulations)")
ap.add_argument("--modele", default="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
                help="modèle sentence-transformers pour --semantique")
ap.add_argument("--min-cos", type=float, default=0.55, help="cosinus minimal pour une paire sémantique")
ap.add_argument("--min-z", type=float, default=4.0,
                help="distinction minimale : (cos - moyenne du paragraphe) / ecart-type. "
                     "Le corpus ne parle que d'un dossier : tout y est proche de tout, et un "
                     "seuil absolu de cosinus ne separe rien. Le z-score mesure si la citation "
                     "se detache du fond topique propre au paragraphe.")
ap.add_argument("--recompute", action="store_true", help="ignore le cache d'embeddings")
args = ap.parse_args()

FENCE = re.compile(r"```.*?```", re.S)
QUOTED = re.compile(r"[«\"]([^«»\"]{40,})[»\"]")
COTE = re.compile(r"\bP-\d+")
RENVOI = re.compile(r"piece_[\w-]+|\b(?:eq|pq)-\d+\b|email-\d+|pdf-\d+|events?-\d+")
WORD = re.compile(r"[a-zà-öø-ÿ']{3,}", re.I)


def norm(s):
    s = unicodedata.normalize("NFKC", s or "")
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-"), (" ", " ")):
        s = s.replace(a, b)
    return s


def terms(text):
    return {w.lower().strip("'") for w in WORD.findall(norm(text))}


# ------------------------------------------------------------------ 1. découpage
print("Découpage du corpus ...")
paragraphs = []          # {file, line, text, etaye}
files = sorted(LEGAL_DIR.rglob("*.md"))
df = Counter()           # document frequency des termes, par fichier

for f in files:
    try:
        raw = norm(f.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        continue
    df.update(terms(raw))

    # on retire les blocs verbatim mais on garde une trace de leur position
    fenced_at = set()
    stripped = []
    for i, chunk in enumerate(FENCE.split(raw)):
        stripped.append(chunk)
    body = FENCE.sub("\n@@FENCE@@\n", raw)

    line_no = 1
    for block in body.split("\n\n"):
        n_lines = block.count("\n") + 1
        start = line_no
        line_no += n_lines + 1
        t = block.strip()
        if not t:
            continue
        if t == "@@FENCE@@":
            if paragraphs and paragraphs[-1]["file"] == str(f.relative_to(BASE_DIR)):
                paragraphs[-1]["etaye"] = True          # bloc verbatim juste après
            continue
        if t.startswith("#") or t.startswith("|") or t.startswith(">"):
            continue                                     # titre, tableau, citation
        if t.startswith("---") or t.startswith("```"):
            continue
        words = WORD.findall(t)
        if len(words) < args.min_words:
            continue
        etaye = bool(QUOTED.search(t) or COTE.search(t) or RENVOI.search(t))
        paragraphs.append({
            "file": str(f.relative_to(BASE_DIR)), "line": start,
            "text": t, "etaye": etaye, "terms": terms(t),
        })

n_files = len(files)
etayes = sum(1 for p in paragraphs if p["etaye"])
candidats = [p for p in paragraphs if not p["etaye"]]
print(f"  {n_files} fichiers, {len(paragraphs)} paragraphes-idées")
print(f"    étayés     : {etayes}")
print(f"    NON étayés : {len(candidats)}")

# ------------------------------------------------------------------ 2. idf
idf = {}
for t, n in df.items():
    if n / n_files > args.max_df:
        continue                                          # terme trop courant
    idf[t] = math.log(n_files / n)
print(f"  {len(idf)} termes distinctifs retenus (df <= {args.max_df:.0%})")

# ------------------------------------------------------------------ 3. citations
print("Chargement des citations ...")
quotes = []
for q in PDFQuote.objects.select_related("pdf_document").all():
    tt = terms(q.quote_text) & idf.keys()
    if not tt:
        continue
    quotes.append({"id": f"pq-{q.pk}", "src": f"pdf-{q.pdf_document_id} p.{q.page_number}",
                   "titre": q.pdf_document.title if q.pdf_document else "",
                   "raw": q.quote_text, "terms": tt,
                   "trames": sorted(t.pk for t in q.trames_narratives.all())})
for q in EmailQuote.objects.select_related("email").all():
    tt = terms(q.quote_text) & idf.keys()
    if not tt:
        continue
    e = q.email
    quotes.append({"id": f"eq-{q.pk}", "src": f"email-{q.email_id}",
                   "titre": (e.subject or "(sans objet)") if e else "",
                   "raw": q.quote_text, "terms": tt,
                   "trames": sorted(t.pk for t in q.trames_narratives.all())})
print(f"  {len(quotes)} citations indexables")

# index inversé terme -> citations
inv = defaultdict(list)
for i, q in enumerate(quotes):
    for t in q["terms"]:
        inv[t].append(i)

# ------------------------------------------------------------------ 3bis. écarter les verbatim
# Un paragraphe qui reproduit une citation n'est pas une idée : c'est le support.
print("Élimination des paragraphes qui reproduisent une citation ...")


def wgrams(text, n=4):
    w = re.sub(r"[^\w\s']", " ", norm(text).lower()).split()
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


for q in quotes:
    q["grams"] = wgrams(q["raw"])
gram_inv = defaultdict(list)
for i, q in enumerate(quotes):
    for g in q["grams"]:
        gram_inv[g].append(i)

verbatim = 0
reste = []
for p in candidats:
    hits = Counter()
    for g in wgrams(p["text"]):
        for i in gram_inv.get(g, ()):
            hits[i] += 1
    reproduit = any(c / max(1, len(quotes[i]["grams"])) >= args.repro for i, c in hits.items())
    if reproduit:
        verbatim += 1
    else:
        reste.append(p)
candidats = reste
print(f"  {verbatim} paragraphe(s) écarté(s) comme verbatim — restent {len(candidats)} idées non étayées")

# ------------------------------------------------------------------ 4. appariement
print("Appariement ...")
paires = []
for k, p in enumerate(candidats):
    if k % 1000 == 0 and k:
        print(f"  {k}/{len(candidats)}")
    scores = defaultdict(float)
    shared = defaultdict(list)
    for t in p["terms"] & idf.keys():
        w = idf[t]
        for i in inv.get(t, ()):
            scores[i] += w
            shared[i].append(t)
    for i, s in scores.items():
        if s < args.min_score:
            continue
        q = quotes[i]
        # normalisation : on rapporte au poids total de la citation, pour ne pas
        # favoriser mecaniquement les longues citations
        denom = sum(idf[t] for t in q["terms"]) or 1.0
        cov = s / denom
        if cov < args.min_cov:
            continue
        paires.append({"p": p, "q": q, "score": s, "couverture": cov,
                       "rang": s * cov,
                       "termes": sorted(shared[i], key=lambda x: -idf[x])[:12]})

# Tri sur le PRODUIT score x couverture. Le score seul favorise les longs
# paragraphes ; la couverture seule favorise les citations courtes, qu'un
# paragraphe recouvre a 100 % avec deux ou trois mots. Le produit exige les deux :
# une citation substantielle, largement recouverte.
paires.sort(key=lambda x: -x["rang"])
print(f"  {len(paires)} paires au-dessus des seuils (score >= {args.min_score}, "
      f"couverture >= {args.min_cov:.0%})")

# une idée peut appeler plusieurs citations : on garde les meilleures par paragraphe
par_par = defaultdict(list)
for pr in paires:
    key = (pr["p"]["file"], pr["p"]["line"])
    if len(par_par[key]) < 3:
        par_par[key].append(pr)
retenues = [pr for lst in par_par.values() for pr in lst]
retenues.sort(key=lambda x: -x["rang"])

# ------------------------------------------------------------------ 4bis. sémantique
# L'appariement lexical ne voit que les mots partagés : une idée formulée
# autrement que sa citation d'appui lui échappe. Le passage par embeddings
# multilingues rattrape ces cas-là — au prix d'un signal moins explicable, d'où
# la présentation séparée.
sem_pairs = []
if args.semantique:
    print(f"Chargement du modèle {args.modele} ...")
    from sentence_transformers import SentenceTransformer
    import numpy as np

    model = SentenceTransformer(args.modele)
    dim = model.get_sentence_embedding_dimension()
    print(f"  {dim} dimensions, fenêtre {model.max_seq_length} tokens")

    # Les paragraphes longs dépassent la fenêtre du modèle : on les découpe en
    # fenêtres glissantes et on retient la meilleure similarité obtenue.
    WIN, STRIDE = 90, 45
    chunks, owner = [], []
    for k, p in enumerate(candidats):
        w = p["text"].split()
        if len(w) <= 110:
            chunks.append(p["text"]); owner.append(k)
        else:
            for i in range(0, len(w), STRIDE):
                seg = w[i:i + WIN]
                if len(seg) < 20:
                    break
                chunks.append(" ".join(seg)); owner.append(k)
    print(f"  {len(chunks)} fenêtres pour {len(candidats)} paragraphes")

    cache = Path(__file__).resolve().parent / ".cache_embeddings.npz"
    sig = f"{args.modele}|{len(quotes)}|{len(chunks)}"
    qv = pv = None
    if cache.exists() and not args.recompute:
        z = np.load(cache, allow_pickle=True)
        if str(z["sig"]) == sig:
            qv, pv = z["qv"], z["pv"]
            print(f"  embeddings relus du cache ({cache.name})")
    if qv is None:
        print("  encodage des citations ...")
        qv = model.encode([q["raw"] for q in quotes], batch_size=32,
                          show_progress_bar=False, normalize_embeddings=True)
        print("  encodage des paragraphes ...")
        pv = model.encode(chunks, batch_size=32, show_progress_bar=True,
                          normalize_embeddings=True)
        np.savez_compressed(cache, qv=qv, pv=pv, sig=sig)
        print(f"  embeddings mis en cache ({cache.name})")

    owner = np.array(owner)
    best = np.full((len(candidats), len(quotes)), -1.0, dtype="float32")
    STEP = 512
    for i in range(0, len(chunks), STEP):
        sims = pv[i:i + STEP] @ qv.T                      # vecteurs normalisés → cosinus
        for r, o in enumerate(owner[i:i + STEP]):
            np.maximum(best[o], sims[r], out=best[o])

    lex_keys = {(pr["p"]["file"], pr["p"]["line"], pr["q"]["id"]) for pr in paires}
    # Renvoi a la source deja present dans le paragraphe : la lacune n'est alors
    # pas l'identification de la piece mais l'absence du verbatim.
    RENVOI_LARGE = re.compile(
        r"\b(?:email|courriel|pdf(?:document)?|events?|photo(?:document)?|statement|document)\b"
        r"[\s:]*(?:id\s*=?\s*)?\d+", re.I)
    for k, p in enumerate(candidats):
        v = best[k]
        mu, sd = float(v.mean()), float(v.std()) or 1e-6
        order = np.argsort(-v)[:3]
        for i in order:
            cos = float(v[i])
            zsc = (cos - mu) / sd
            if cos < args.min_cos or zsc < args.min_z:
                continue
            q = quotes[i]
            sem_pairs.append({
                "p": p, "q": q, "cos": cos, "z": zsc,
                "renvoi": bool(RENVOI_LARGE.search(p["text"])),
                "aussi_lexical": (p["file"], p["line"], q["id"]) in lex_keys,
            })
    sem_pairs.sort(key=lambda x: -x["z"])
    n_new = sum(1 for s in sem_pairs if not s["aussi_lexical"])
    print(f"  {len(sem_pairs)} paires sémantiques (cos >= {args.min_cos}, z >= {args.min_z}) "
          f"— dont {n_new} invisibles à l'appariement lexical")

# ------------------------------------------------------------------ 5. rapport
L = []
add = L.append
add("# Idées sans citation — appariements candidats")
add("")
add("Généré par `docs/purge_quotes/idees_sans_citation.py`. Lecture seule.")
add("")
add("Objectif : ne pas laisser une idée non étayée quand une citation existe en base pour "
    "l'appuyer. Chaque entrée met un **paragraphe non étayé** du corpus en regard d'une "
    "**citation disponible**, avec les termes distinctifs qui les rapprochent.")
add("")
add("Le score n'établit pas la pertinence : c'est un **ordre de lecture**. Un terme rare "
    "partagé peut relever du hasard ; c'est à la lecture que se décide si la citation "
    "étaye vraiment l'idée.")
add("")
add("| | |")
add("|---|---|")
add(f"| fichiers `.md` parcourus | {n_files} |")
add(f"| paragraphes-idées (≥ {args.min_words} mots, hors verbatim/tableaux/titres) | {len(paragraphs)} |")
add(f"| dont **étayés** (citation, cote P-n, renvoi, ou bloc verbatim suivant) | {etayes} "
    f"({100 * etayes / max(1, len(paragraphs)):.0f} %) |")
add(f"| dont **verbatim** (le paragraphe reproduit une citation ≥ {args.repro:.0%}) | {verbatim} |")
add(f"| dont **idées non étayées** | **{len(candidats)}** "
    f"({100 * len(candidats) / max(1, len(paragraphs)):.0f} %) |")
add(f"| citations indexées | {len(quotes)} |")
add(f"| paires au-dessus du seuil (score ≥ {args.min_score}) | {len(paires)} |")
add(f"| paragraphes concernés | {len(par_par)} |")
add("")
add("---")
add("")
add(f"## Appariements, par score décroissant (les {min(args.top, len(retenues))} premiers)")
add("")

for n, pr in enumerate(retenues[:args.top], 1):
    p, q = pr["p"], pr["q"]
    orph = " — *citation encore inexploitée*" if not q["trames"] else ""
    add(f"### {n}. `{p['file']}` ligne ~{p['line']} → `{q['id']}`{orph}")
    add("")
    add(f"- **rang** {pr['rang']:.1f} = score {pr['score']:.1f} × couverture {pr['couverture']:.0%}")
    add(f"- **termes partagés** : {', '.join('`' + t + '`' for t in pr['termes'])}")
    add(f"- **source de la citation** : {q['src']} — {q['titre'][:60]} — trames "
        f"{', '.join(str(t) for t in q['trames']) or '—'}")
    add("")
    add("**Idée non étayée :**")
    add("")
    for line in p["text"].splitlines()[:8]:
        add(f"> {line}")
    add("")
    add("**Citation disponible :**")
    add("")
    add("```text")
    for line in q["raw"].splitlines()[:12]:
        add(line)
    add("```")
    add("")

if args.semantique:
    nouveaux = [s for s in sem_pairs if not s["aussi_lexical"]]
    confirmes = [s for s in sem_pairs if s["aussi_lexical"]]
    add("---")
    add("")
    add("## Appariement sémantique")
    add("")
    add(f"Modèle `{args.modele}` — {dim} dimensions, multilingue. "
        "Les paragraphes longs sont découpés en fenêtres glissantes ; on retient la "
        "meilleure similarité obtenue. Le cosinus n'expose pas *pourquoi* deux textes se "
        "ressemblent : cette section demande donc plus de lecture que la précédente, mais "
        "elle attrape les idées formulées avec d'autres mots que leur citation d'appui.")
    add("")
    add(f"- paires retenues (cosinus ≥ {args.min_cos} **et** distinction z ≥ {args.min_z}) : "
        f"**{len(sem_pairs)}**")
    add("")
    add("> Le seuil de cosinus seul ne suffit pas : le corpus ne traite que d'un dossier, "
        "tout y est proche de tout. À 0,55 sans autre critère, la moitié des paragraphes "
        "trouvait un « appui ». Le **z-score** rapporte la similarité d'une paire à la "
        "distribution propre du paragraphe face aux 312 citations : il ne retient que les "
        "rapprochements qui se détachent de ce fond topique.")
    add("")
    add(f"- dont déjà trouvées par l'appariement lexical : {len(confirmes)} "
        "(**convergence des deux méthodes — les plus sûres**)")
    add(f"- dont **invisibles au lexical** : **{len(nouveaux)}** — c'est l'apport propre "
        "de cette passe")
    add("")

    def bloc_sem(items, titre, note):
        add(f"### {titre}")
        add("")
        add(note)
        add("")
        for n, s in enumerate(items[:args.top], 1):
            p, q = s["p"], s["q"]
            orph = " — *citation encore inexploitée*" if not q["trames"] else ""
            add(f"#### {n}. `{p['file']}` ligne ~{p['line']} → `{q['id']}`{orph}")
            add("")
            add(f"- **distinction z = {s['z']:.1f}** — cosinus {s['cos']:.3f}"
                + ("  \n- **la source est déjà nommée dans le paragraphe** : il manque le verbatim, "
                   "pas l'identification de la pièce" if s["renvoi"] else ""))
            add(f"- **source** : {q['src']} — {q['titre'][:60]} — trames "
                f"{', '.join(str(t) for t in q['trames']) or '—'}")
            add("")
            add("**Idée non étayée :**")
            add("")
            for line in p["text"].splitlines()[:8]:
                add(f"> {line}")
            add("")
            add("**Citation disponible :**")
            add("")
            add("```text")
            for line in q["raw"].splitlines()[:12]:
                add(line)
            add("```")
            add("")

    bloc_sem(confirmes, f"Convergence lexical + sémantique ({len(confirmes)})",
             "Les deux méthodes indépendantes désignent la même paire. Ce sont les "
             "candidats les plus solides du rapport.")
    bloc_sem(nouveaux, f"Apport propre du sémantique ({len(nouveaux)})",
             "L'idée et la citation ne partagent pas de vocabulaire distinctif, mais se "
             "rejoignent sur le sens. À lire une par une : c'est ici que le bruit est le "
             "plus probable, et aussi les rapprochements que rien d'autre ne trouverait.")

OUT_PATH.write_text("\n".join(L), encoding="utf-8")

print()
print("=" * 78)
print(f"Ecrit : {OUT_PATH}")
print("=" * 78)
print(f"  paragraphes-idees          : {len(paragraphs)}")
print(f"    etayes                   : {etayes} ({100*etayes/max(1,len(paragraphs)):.0f}%)")
print(f"    NON etayes               : {len(candidats)} ({100*len(candidats)/max(1,len(paragraphs)):.0f}%)")
print(f"  paires >= {args.min_score}              : {len(paires)}")
print(f"  paragraphes concernes      : {len(par_par)}")
inex = sum(1 for pr in retenues[:args.top] if not pr["q"]["trames"])
print(f"  dont citations inexploitees (dans le top {args.top}) : {inex}")
