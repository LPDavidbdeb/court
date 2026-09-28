# -*- coding: utf-8 -*-
"""Génère 16_liste_chronologique.md — la liste chronologique des éléments de preuve.

Modèle : UNE liste chronologique de tous les éléments ; les AXES en sont des
vues, chacune isolant les éléments qui soutiennent une allégation. Les comptes
ne s'écrivent jamais dans l'acte : ils se lisent ici.

    .venv/bin/python legal/redaction_v2/outils/liste_chronologique.py
"""
import sys, os, io, re, pickle, datetime, collections
RACINE = '/Users/Louis-Philippe/Documents/GitHub/court'
SCRATCH = '/private/tmp/claude-501/-Users-Louis-Philippe-Documents-GitHub-court/c6dbb4b5-4f56-4139-96c9-af76bd2b09f8/scratchpad/'
sys.path.insert(0, RACINE)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django; django.setup()
from email_manager.models import EmailThread
from django.db.models import Min

OUT = os.path.join(RACINE, 'legal/redaction_v2/16_liste_chronologique.md')
DEB, FIN = datetime.date(2009,10,6), datetime.date(2015,2,23)

AXES = {
 'A': ("Soins de santé et besoins imprévus", "22-X · A2.7"),
 'B': ("Disponibilité — absences de la demanderesse", "22-P · 22-Q"),
 'C': ("Prise en charge quotidienne au domicile", "22-B · 22-H à 22-L"),
 'D': ("Activités structurées", "22-R · 22-S"),
 'E1': ("Sorties librement organisées", "22-W · 22-Y"),
 'E2': ("Famille paternelle", "22-V · 22-V-A"),
}

# --- sources -----------------------------------------------------------------
elements = []   # (date, cle_tri, ref, axes, libelle, substrat)

rows = pickle.load(open(SCRATCH+'rows.pkl','rb'))
for r in rows:
    if r['dim'] == '—' or not (DEB <= r['date'] <= FIN): continue
    elements.append((r['date'], 0, f"Event {r['pk']}", r['dim'].split('·'),
                     re.sub(r'\s+',' ',r['txt'])[:110], f"{r['ph']} photo(s)"))

src = io.open(SCRATCH+'classify.py', encoding='utf-8').read()
fils = {}
for m in re.finditer(r'^\s*(\d+):\("([^"]*)","([^"]*)","([^"]*)"', src, re.M):
    if m.group(2) != '—':
        fils[int(m.group(1))] = (m.group(2), m.group(4))
qs = EmailThread.objects.filter(pk__in=fils).annotate(d0=Min('emails__date_sent'))
for t in qs:
    if not t.d0: continue
    d = t.d0.date()
    if not (DEB <= d <= FIN): continue
    dim, what = fils[t.pk]
    n = t.emails.count()
    elements.append((d, 1, f"fil {t.pk}", [x.rstrip('·') for x in dim.split('·') if x.strip('·')],
                     what[:110], f"{n} courriel(s)"))

elements.sort(key=lambda e: (e[0], e[1]))

# --- émission ----------------------------------------------------------------
w = io.open(OUT, 'w', encoding='utf-8').write
w(f"""# 16 — La liste chronologique

> ⚠️ **Fichier généré. Ne pas l'éditer à la main.** Régénérer :
> ```
> .venv/bin/python legal/redaction_v2/outils/liste_chronologique.py
> ```
>
> **Modèle.** Une seule liste, ordonnée dans le temps. Les **axes** (§ 2) en sont des vues : chacun isole les éléments qui soutiennent une allégation. L'acte n'écrit aucun dénombrement — les comptes se lisent ici.
>
> **Périmètre.** Du 6 octobre 2009 au 23 février 2015, soit la cohabitation. Les éléments postérieurs servent d'autres blocs et ne figurent pas.
>
> ⚠️ **Une description n'est pas une source.** Pour un `Event`, le substrat est la photographie horodatée ; pour un fil, ce sont les courriels. La colonne « ce que l'élément porte » est un libellé de travail, à reconduire à la pièce avant toute utilisation.

## 1. La liste

**{len(elements)} éléments.**

| Date | Élément | Axes | Substrat | Ce que l'élément porte |
|---|---|---|---|---|
""")
for d, _, ref, ax, lib, sub in elements:
    w(f"| {d} | `{ref}` | {' '.join(ax)} | {sub} | {lib} |\n")

w("\n## 2. Les axes — vues sur la liste\n\n")
for code, (nom, para) in AXES.items():
    sel = [e for e in elements if code in e[3]]
    if not sel: continue
    d0, d1 = sel[0][0], sel[-1][0]
    nev = sum(1 for e in sel if e[2].startswith('Event'))
    nfi = len(sel) - nev
    w(f"### Axe {code} — {nom}\n\n")
    w(f"*Soutient :* ¶¶ {para} · *Bornes :* {d0} → {d1} · **{len(sel)} éléments** ({nev} `Event`, {nfi} fils)\n\n")
    w("| Date | Élément | Substrat |\n|---|---|---|\n")
    for d, _, ref, _, lib, sub in sel:
        w(f"| {d} | `{ref}` | {sub} |\n")
    w("\n")

# couverture
mois = []; y, m = DEB.year, DEB.month
while (y, m) <= (FIN.year, FIN.month):
    mois.append((y, m)); m += 1
    if m == 13: y, m = y+1, 1
occupes = {(d.year, d.month) for d, *_ in elements}
vides = [t for t in mois if t not in occupes]
ecarts = []
ds = sorted({d for d, *_ in elements})
for a, b in zip(ds, ds[1:]):
    ecarts.append(((b-a).days, a, b))
ecarts.sort(reverse=True)
NOM = {1:'janv',2:'févr',3:'mars',4:'avr',5:'mai',6:'juin',7:'juil',8:'août',9:'sept',10:'oct',11:'nov',12:'déc'}
w(f"""## 3. Couverture

- **{len(mois)-len(vides)} mois sur {len(mois)}** portent au moins un élément.
- Mois sans élément : {', '.join(f'{NOM[m]} {y}' for y, m in vides) or 'aucun'}
- **Plus grand intervalle sans élément : {ecarts[0][0]} jours** ({ecarts[0][1]} → {ecarts[0][2]}).
- Intervalles suivants : {', '.join(f'{n} j' for n, _, _ in ecarts[1:5])}.

⚠️ Ces trois nombres sont les seuls à pouvoir être écrits dans l'acte au sujet de la couverture, et ils le sont au ¶ 22-AC. Ne jamais écrire « présence continue ».
""")
print(f"écrit : {OUT}")
print(f"  {len(elements)} éléments · {len(mois)-len(vides)}/{len(mois)} mois · écart max {ecarts[0][0]} j")
for code,(nom,_) in AXES.items():
    print(f"  axe {code}: {sum(1 for e in elements if code in e[3])}")
