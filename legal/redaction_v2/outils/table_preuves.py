# -*- coding: utf-8 -*-
"""Génère 15_table_preuves.md depuis 14_allegations_proposees.md.

Parcourt le fichier des allégations, extrait pour chacune les références de
pièces (Email / Event / PDFDocument / PhotoDocument / ChatSequence / P-xx),
enrichit depuis la base, et émet deux index : allégation → pièces, pièce →
allégations. À relancer après chaque modification du fichier 14.

    .venv/bin/python legal/redaction_v2/outils/table_preuves.py
"""
import sys, re, io, os, collections
RACINE = '/Users/Louis-Philippe/Documents/GitHub/court'
sys.path.insert(0, RACINE)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django; django.setup()
from email_manager.models import Email
from events.models import Event

SRC = os.path.join(RACINE, 'legal/redaction_v2/14_allegations_proposees.md')
OUT = os.path.join(RACINE, 'legal/redaction_v2/15_table_preuves.md')

# --- 1. découper le fichier en blocs d'allégation ---------------------------
ID = r'(?:A\d+(?:\.\d+)?(?:-(?:bis|ter|[A-Z]))?|B\d+|C\d+)'
texte = io.open(SRC, encoding='utf-8').read()

blocs = []          # (id, texte du bloc)
# Une ALLEGATION est un en-tete « ## A1. ... » et court jusqu'au suivant :
# tout ce qu'il contient (les « En effet » A1.1, A1.2... et le bloc d'appuis)
# lui appartient. Un identifiant a point n'est PAS une allegation.
for m in re.finditer(r'^##\s+(' + ID + r')\.\s+(.*?)(?=\n##\s|\n# |\Z)', texte, re.M | re.S):
    if '.' not in m.group(1):
        blocs.append((m.group(1), m.group(2)))
if blocs:
    pass


# --- 2. extraire les références --------------------------------------------
COTE = re.compile(r'\bP-(\d+(?:\.\d+)?)')

MOIS = r'janvier|f\u00e9vrier|mars|avril|mai|juin|juillet|ao\u00fbt|septembre|octobre|novembre|d\u00e9cembre'
MOTIFS = [
    ('Email',         r'`Email`\s*(?:id=)?\s*'),
    ('Event',         r'`Event`\s*(?:id=)?\s*E?'),
    ('PDFDocument',   r'PDFDocument\s*(?:id=)?\s*'),
    ('PhotoDocument', r'PhotoDocument\s*(?:id=)?\s*'),
    ('ChatSequence',  r'`?ChatSequence`?\s*(?:id=)?\s*'),
]
# Un nombre suivi d'un nom de mois est une DATE, pas un pk. Un nombre \u00e0 quatre
# chiffres est une ann\u00e9e. Les deux sont \u00e9cart\u00e9s : c'est le bug qui faisait entrer
# « Email 590, 26 janvier 2010 » comme deux pi\u00e8ces.
SUITE = re.compile(r'\s*(?:,|\s+et\s+)\s*E?(\d{1,4})(?!\d)')
DATE_APRES = re.compile(r'^\s*(?:' + MOIS + r')', re.I)

def lire_refs(corps):
    """Extrait les (mod\u00e8le, pk) d'un bloc, en \u00e9cartant dates et ann\u00e9es."""
    trouves = []
    for modele, prefixe in MOTIFS:
        for m in re.finditer(prefixe + r'(\d{1,4})(?!\d)', corps):
            trouves.append((modele, int(m.group(1))))
            pos = m.end()
            # suite \u00e9ventuelle : « 100, 81, 80 » ou « 113 et 68 »
            while True:
                sm = SUITE.match(corps, pos)
                if not sm:
                    break
                n = sm.group(1)
                reste = corps[sm.end():]
                if len(n) == 4 or DATE_APRES.match(reste):
                    break                      # c'est une date ou une ann\u00e9e
                trouves.append((modele, int(n)))
                pos = sm.end()
    return trouves

par_alleg = collections.OrderedDict()
for aid, corps in blocs:
    cotes = set(COTE.findall(corps))
    e = par_alleg.setdefault(aid, {'refs': [], 'cotes': set(), 'texte': ''})
    e['refs'] += lire_refs(corps)
    e['cotes'] |= {'P-' + c for c in cotes}
    if len(corps) > len(e['texte']):
        e['texte'] = corps

# d\u00e9doublonner en conservant l'ordre
for e in par_alleg.values():
    vus, uniq = set(), []
    for r in e['refs']:
        if r not in vus:
            vus.add(r); uniq.append(r)
    e['refs'] = uniq

# --- 3. enrichir depuis la base --------------------------------------------
def libelle(modele, pk):
    try:
        if modele == 'Email':
            o = Email.objects.get(pk=pk)
            d = o.date_sent.strftime('%Y-%m-%d') if o.date_sent else '????'
            qui = (o.sender or '').split('<')[0].strip()[:24]
            return f"{d} · {qui}"
        if modele == 'Event':
            o = Event.objects.get(pk=pk)
            n = o.linked_photos.count()
            return f"{o.date} · {n} photo(s)"
    except Exception:
        return '⚠️ introuvable en base'
    return ''

# --- 4. émettre -------------------------------------------------------------
def court(t, n=95):
    t = re.sub(r'\s+', ' ', re.sub(r'[*`>|]', '', t)).strip()
    return (t[:n] + '…') if len(t) > n else t

w = io.open(OUT, 'w', encoding='utf-8').write
w("""# 15 — Table des preuves

> ⚠️ **Fichier généré. Ne pas l'éditer à la main.**
> Source : [`14_allegations_proposees.md`](14_allegations_proposees.md). Régénérer après chaque modification :
>
> ```
> .venv/bin/python legal/redaction_v2/outils/table_preuves.py
> ```
>
> Les pièces sont menées par **modèle + pk**, jamais par cote seule. Une allégation sans référence de pièce est **testimoniale** — ce n'est pas un défaut, c'est une nature, mais elle doit être connue.

## 1. Allégation → pièces\n\n*Une ligne = une allégation. Les « En effet » qui la portent et son bloc d'appuis sont comptés avec elle.*

| Allégation | Énoncé | Pièces (modèle + pk) | Cotes citées | Nature |
|---|---|---|---|---|
""")
testimoniales, cote_seule, textuelles = [], [], []
for aid, e in par_alleg.items():
    refs = ' · '.join(f"{m} {pk}" for m, pk in e['refs']) or '—'
    cotes = ', '.join(sorted(e['cotes'], key=lambda c: float(c[2:]))) or '—'
    if not e['refs'] and not e['cotes']:
        # L'appui peut etre le TEXTE MEME de la Requete adverse (document-1) :
        # une allegation d'absence (« la requete n'allegue nulle part... ») se
        # verifie sur l'acte, pas sur une piece du demandeur.
        if re.search(r'requ\u00eate', e['texte'], re.I):
            textuelles.append(aid); nature = 'textuelle — Requ\u00eate, `Document` 1'
        else:
            testimoniales.append(aid); nature = '**testimoniale**'
    elif not e['refs']:
        cote_seule.append(aid); nature = '⚠️ cote seule'
    else:
        nature = 'documentaire'
    w(f"| **{aid}** | {court(e['texte'])} | {refs} | {cotes} | {nature} |\n")

# index inverse
inverse = collections.defaultdict(list)
for aid, e in par_alleg.items():
    for r in e['refs']:
        inverse[r].append(aid)

w("\n## 2. Pièce → allégations\n\n| Pièce | Repère | Allégations |\n|---|---|---|\n")
for (modele, pk) in sorted(inverse, key=lambda r: (r[0], r[1])):
    w(f"| `{modele}` {pk} | {libelle(modele, pk)} | {', '.join(inverse[(modele, pk)])} |\n")

w(f"""
## 3. Contrôles

- **Testimoniales** — ni pk ni cote, appuyées sur le témoignage du demandeur : {', '.join(testimoniales) if testimoniales else 'aucune'}
- **Textuelles** — vérifiables sur l'acte adverse lui-même (`Document` 1), non sur une pièce du demandeur : {', '.join(textuelles) if textuelles else 'aucune'}
- **⚠️ Cote seule, pk manquant** — à reconduire au `modèle + pk` avant rédaction, LP ne reconnaît pas ses pièces par leur cote : {', '.join(cote_seule) if cote_seule else 'aucune'}
- **Pièces distinctes mobilisées :** {len(inverse)}
- **Allégations recensées :** {len(par_alleg)}

⚠️ Les cotes `P-__` du fichier 14 signalent une pièce **non encore cotée au bordereau**. Elles n'apparaissent pas dans la colonne « cotes citées » : s'y reporter allégation par allégation.
""")
print(f"écrit : {OUT}")
print(f"  {len(par_alleg)} allégations · {len(inverse)} pièces distinctes · {len(testimoniales)} testimoniales · {len(textuelles)} textuelles · {len(cote_seule)} à reconduire au pk")
