#!/usr/bin/env python3
"""Cherche une expression dans le texte d'une loi, avec son contexte.

⚠️ Existe parce qu'un `grep` ordinaire sur ces fichiers est TROMPEUR : la couche
texte des PDF de LegisQuébec est en Unicode décomposé, de sorte qu'une recherche
portant un accent renvoie zéro résultat alors que le mot est présent. Ce script
normalise les deux côtés avant de comparer.

  scripts/loi/chercher.py <code> "jour férié"
"""
import re
import sys
import unicodedata
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
DOSSIER = RACINE / "legal" / "analyse" / "textes_de_loi"


def main():
    if len(sys.argv) < 3:
        sys.exit('usage: chercher.py <code> "expression" [contexte]')
    code, motif = sys.argv[1], sys.argv[2]
    marge = int(sys.argv[3]) if len(sys.argv) > 3 else 260

    txts = sorted(DOSSIER.glob(f"{code}*.txt"))
    if not txts:
        sys.exit(f"Aucun texte extrait pour « {code} ». Lancer d'abord : scripts/loi/lire.sh {code} 1")
    texte = unicodedata.normalize("NFC", txts[-1].read_text(encoding="utf-8", errors="replace"))
    texte = re.sub(r"[ \t]+", " ", texte)
    cible = unicodedata.normalize("NFC", motif)

    trouves = list(re.finditer(re.escape(cible), texte, re.IGNORECASE))
    print(f"— source : {txts[-1].name}")
    print(f"— « {motif} » : {len(trouves)} occurrence(s)\n")
    for n, m in enumerate(trouves, 1):
        extrait = texte[max(0, m.start() - marge):m.end() + marge].replace("\n", " ⏎ ")
        print(f"[{n}] …{extrait}…\n")


if __name__ == "__main__":
    main()
