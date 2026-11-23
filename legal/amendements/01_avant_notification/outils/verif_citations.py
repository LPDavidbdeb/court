#!/usr/bin/env python3
"""Vérifie que chaque citation « … » d'une section se retrouve dans une fiche pièce.

Usage : python3 verif_citations.py <section.md> [<section.md> ...]

- Corpus : uniquement les fiches pièces `legal/**/piece_*.md` (hors `depots/`).
  Une citation qui ne se retrouve que dans une analyse ou une autre section
  n'est PAS vérifiée : elle doit l'être sur sa pièce.
- Extraction : les segments entre « et » du corps de la section (tout ce qui
  précède le marqueur `<!-- fin-du-texte -->`) ; « […] » sépare les fragments,
  chaque fragment de plus de 12 caractères est vérifié séparément.
- Normalisation : NFC, apostrophe typographique -> droite, suppression de
  * > _ ` et des espaces multiples, comparaison insensible à la casse.
  Un numéro de paragraphe en tête de citation (« 56. … ») est ignoré ; un
  ajout éditorial entre crochets (« [Il] ») sépare les fragments comme « […] ».
  Aucune autre tolérance (orthographe source).
- Repli : si un fragment de plusieurs phrases n'est pas trouvé d'un bloc, chaque
  phrase est cherchée séparément (certaines fiches, dont la requête, rangent une
  phrase par ligne) ; le fragment est alors marqué OK* si toutes ses phrases sont
  trouvées.
Sortie : une ligne par fragment, OK, OK* ou NO, et le nom de la première fiche trouvée.
Code de retour 1 si au moins un fragment n'est pas trouvé.
"""
import sys, glob, re, unicodedata, pathlib

MARQUEUR = '<!-- fin-du-texte -->'
RACINE = pathlib.Path(__file__).resolve().parents[3]  # .../legal

def norm(s):
    s = unicodedata.normalize('NFC', s).replace('’', "'")
    s = re.sub(r'[*>_`]', '', s)
    return re.sub(r'\s+', ' ', s).strip().casefold()

def corpus():
    fichiers = [f for f in glob.glob(str(RACINE / '**' / 'piece_*.md'), recursive=True)
                if '/depots/' not in f]
    return {pathlib.Path(f).name: norm(open(f, encoding='utf-8').read()) for f in fichiers}

def fragments(texte):
    corps = texte.split(MARQUEUR)[0]
    for q in re.findall(r'«\s*(.+?)\s*»', corps, flags=re.S):
        q = re.sub(r'^\d+\.\s+', '', q.strip())
        for part in re.sub(r'\[[^\]]*\]', '\x00', q).split('\x00'):
            part = part.strip(' ,.;:')
            if len(part) > 12:
                yield part

def main(chemins):
    c = corpus()
    echec = False
    for chemin in chemins:
        print(f'== {chemin}')
        for frag in fragments(open(chemin, encoding='utf-8').read()):
            n = norm(frag)
            hit = next((nom for nom, t in c.items() if n in t), None)
            tag = 'OK '
            if hit is None:
                phrases = [p for p in re.split(r'(?<=[.!?])\s+', n) if len(p) > 12]
                hits = [next((nom for nom, t in c.items() if p in t), None) for p in phrases]
                if len(phrases) > 1 and all(hits):
                    hit, tag = hits[0], 'OK*'
            if hit is None:
                echec = True
            print((tag if hit else 'NO ') + ' ' + frag[:80] + (' -> ' + hit if hit else ''))
    return 1 if echec else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
