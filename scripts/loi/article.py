#!/usr/bin/env python3
"""Imprime un ou plusieurs articles depuis le texte d'une loi extrait d'un PDF.

Les PDF de LegisQuébec intercalent des fragments de pied de page au milieu des
phrases (« À jour au 24 octobre 2025 », « © Éditeur officiel », « C-25.01 / n sur
N », et des chiffres de millésime isolés). On les retire avant d'imprimer, sinon
une citation recopiée depuis la sortie contient des caractères qui ne sont pas
dans la loi.
"""
import re
import sys
import unicodedata

# Fragments de pied de page que LegisQuébec intercale AU MILIEU des phrases.
# ⚠️ Chaque motif est borné à une ligne. Un motif à cheval sur les lignes — tel
# un « À jour au.*?sur \d+ » avec re.DOTALL — avale le texte réel jusqu'à sa
# prochaine correspondance quand le pied de page est tronqué à une frontière
# d'article. Défaut introduit puis corrigé le 7 nov. 2026.
# Les chiffres parasites (« off0iciel », « 15 1octobre ») sont des numéros de
# page entrelacés par l'extraction : les motifs les tolèrent.
BRUIT = (
    r"(?m)^.*À jour au\s+\d{1,2}.*$",
    r"(?m)^.*©\s*Éditeur\s*off\d*iciel du Qu\d*ébec.*$",
    r"(?m)^.*Ce document a valeur officielle\..*$",
    r"(?m)^\s*C-\d+(?:\.\d+)?\s*/\s*\d+\s*sur\s*\d+\s*$",
    r"(?m)^\s*CODE DE PROCÉDURE CIVILE\s*$",
    r"(?m)^\s*CODE CIVIL(?: DU QUÉBEC)?\s*$",
    r"(?m)^\s*INTERPRÉTATION\s*$",
)


def charger(chemin):
    texte = open(chemin, encoding="utf-8", errors="replace").read()
    # 🔴 La couche texte des PDF de LegisQuébec est en Unicode DÉCOMPOSÉ
    # (A + accent grave combinant, et non « À »). Sans cette normalisation,
    # toute recherche portant un accent renvoie ZÉRO alors que le mot est
    # présent. Constaté le 7 nov. 2026 : une recherche de « férié » dans la
    # Loi d'interprétation ne trouvait rien, alors que l'art. 61, 23° définit
    # précisément « jour de fête » et « jour férié ». Ne jamais retirer.
    texte = unicodedata.normalize("NFC", texte)
    for motif in BRUIT:
        texte = re.sub(motif, "", texte)
    texte = re.sub(r"\n{3,}", "\n\n", texte)
    return re.sub(r"[ \t]+", " ", texte)


def article(texte, numero, portee=4000):
    """Retourne la DERNIÈRE occurrence : la table des matières vient avant le corps."""
    debut = re.compile(r"(?m)^\s*%s\.\s" % re.escape(str(numero)))
    trouves = []
    for m in debut.finditer(texte):
        bloc = texte[m.start():m.start() + portee]
        apres = re.search(r"(?m)^\s*\d{1,4}(?:\.\d+)?\.\s", bloc[len(str(numero)) + 3:])
        if apres:
            bloc = bloc[: len(str(numero)) + 3 + apres.start()]
        bloc = bloc.strip()
        if len(bloc) > 60:          # écarte les lignes de table des matières
            trouves.append(bloc)
    return trouves[-1] if trouves else None


ENUM_NUE = re.compile(
    r"(?:(?:\d{1,2}°|[a-z]\)|[a-z]\.\d\))[ \n]+){3,}"
)


def enumeration_perdue(bloc):
    """Détecte un article dont les marqueurs d'énumération sont imprimés SANS leur texte.

    Les PDF de LegisQuébec mettent parfois les étiquettes (« 23° », « a) », « b) »)
    dans un flux et leur contenu dans un autre. PDFKit restitue alors les
    étiquettes seules, et l'article paraît vide de ses paragraphes. Cas constaté
    le 7 nov. 2026 sur l'art. 61 I-16, dont le paragraphe 23° — la définition des
    jours fériés — ne figurait pas dans la sortie. Citer un tel article sur la foi
    de cette sortie serait citer une loi tronquée.
    """
    return ENUM_NUE.search(bloc) is not None


def main():
    if len(sys.argv) < 3:
        sys.exit("usage: article.py <texte.txt> <no> [no ...]")
    texte = charger(sys.argv[1])
    manquants = []
    for numero in sys.argv[2:]:
        bloc = article(texte, numero)
        print("=" * 16, "art.", numero, "=" * 16)
        if bloc:
            print(bloc)
            if enumeration_perdue(bloc):
                print()
                print("\u26a0\ufe0f  AVERTISSEMENT — des marqueurs d'\u00e9num\u00e9ration apparaissent SANS leur")
                print("    texte : l'extraction a perdu le contenu de ces paragraphes.")
                print("    NE PAS CITER cet article sur la foi de cette sortie.")
                print("    Chercher le contenu ailleurs dans le texte extrait, p. ex. :")
                print("      python3 -c \"import re,sys; t=open(sys.argv[1],encoding='utf-8',"
                      "errors='replace').read(); [print(t[max(0,m.start()-200):m.start()+400])"
                      " for m in re.finditer(sys.argv[2],t)]\" <texte.txt> <mot-cl\u00e9>")
                manquants.append(numero + " (tronqu\u00e9)")
        else:
            print("NON TROUVÉ")
            manquants.append(numero)
        print()
    if manquants:
        sys.exit("articles non trouvés : " + ", ".join(manquants))


if __name__ == "__main__":
    main()
