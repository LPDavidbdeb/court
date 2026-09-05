"""
La numérotation d'un document selon son schéma — une seule implémentation.

UN DOCUMENT PORTE DEUX NUMÉROTATIONS. `LibraryNode.item` conserve le numéro que
le paragraphe avait AU DÉPÔT ; le schéma en recalcule un autre, qui est celui
affiché à l'écran et celui que porterait une version amendée. Sur la demande du
24 juillet 2026, plus de deux cents nœuds diffèrent entre les deux.

CE MODULE EXISTE POUR QU'AUCUN RAPPORT NE CITE UN NUMÉRO SANS L'AUTRE. La vue
affichait le numéro recalculé et gardait celui du dépôt en attribut `title` ;
une commande qui imprimait `item` désignait donc, sous le même mot « § », un
paragraphe entièrement différent de celui que l'écran montre. Deux
implémentations parallèles de la numérotation rendent cette méprise
indétectable : elles n'affichent jamais les deux ensemble.

La règle est donc : on désigne un paragraphe par `§ 44 (dépôt 28)`, jamais par
l'un des deux seul.
"""
import re

from document_manager.models import (
    FormatNumero, LibraryNode, PorteeNumero, RoleNiveau,
)

ROMAINS = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"),
           (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"),
           (5, "V"), (4, "IV"), (1, "I")]

# Convention posée par l'importateur : une conclusion porte « C-n », une mention
# de clôture porte un item vide, un paragraphe porte le numéro qu'il avait au
# dépôt. Le schéma ne sait pas encore qu'une même profondeur peut porter des
# rôles différents selon son ascendance.
RE_CONCLUSION = re.compile(r"^C-\d+$")

# CE QUI DISTINGUE UN SOUS-ITEM DU DOCUMENT D'UNE SCISSION DE TRAVAIL.
#
# Les actes reproduits ne comportent pas de sous-paragraphes. Là où l'arbre en
# porte, ce sont deux choses différentes : soit une énumération qui EXISTE dans
# l'acte déposé — et alors sa puce est imprimée en tête du texte, « a) Alexia
# David, née le… » — soit un paragraphe que la lecture a scindé en deux idées,
# et qui ne porte rien.
#
# La puce est donc le seul indice fiable, et il est intrinsèque au texte. Sans
# cette distinction, on calcule une lettre devant un texte qui porte déjà la
# sienne : la vue « propre » affiche aujourd'hui « a. a) Alexia David… » sur les
# cinq énumérations des trois actes.
RE_PUCE = re.compile(r"^\s*(?:[•·▪◦‣\-–—*]|\(?[a-zA-Z]\)|\(?[ivxIVX]+\)|\(?\d+[.)])\s+")


def en_romain(n):
    out = ""
    for valeur, signe in ROMAINS:
        while n >= valeur:
            out += signe
            n -= valeur
    return out


def formater(n, format_numero):
    if format_numero == FormatNumero.DECIMAL:
        return str(n)
    if format_numero == FormatNumero.ROMAIN_MAJ:
        return en_romain(n)
    if format_numero == FormatNumero.LETTRE_MAJ:
        return chr(ord("A") + (n - 1) % 26)
    if format_numero == FormatNumero.LETTRE_MIN:
        return f"{chr(ord('a') + (n - 1) % 26)})"
    return ""


def genre_du_noeud(role, item, texte=""):
    """
    Nature réelle du bloc, au-delà de ce que la profondeur seule dit.

    `texte` sert à la seule règle qui ne peut pas se lire ailleurs : une
    énumération de l'acte porte sa puce dans son texte, une scission de travail
    n'en porte aucune. Voir RE_PUCE.
    """
    if role == RoleNiveau.PARAGRAPHE and RE_CONCLUSION.match(item or ""):
        return "conclusion"
    if role == RoleNiveau.PARAGRAPHE and not item:
        return "mention"
    if role == RoleNiveau.PARAGRAPHE:
        return "paragraphe"
    if role == RoleNiveau.SOUS_ITEM:
        return "enumeration" if RE_PUCE.match(texte or "") else "sous_paragraphe"
    if role in (RoleNiveau.SECTION, RoleNiveau.SOUS_SECTION, RoleNiveau.THEME,
                RoleNiveau.SOUS_THEME, RoleNiveau.CHAPEAU):
        return "titre"
    return "libre"


def texte_du_noeud(noeud):
    """Le texte porté par un nœud, quel que soit le modèle qui le porte."""
    obj = noeud.content_object
    if obj is None:
        return ""
    return (getattr(obj, "text", None) or getattr(obj, "quote_text", None)
            or getattr(obj, "titre", None) or "")


def numeroter(document, noeuds=None):
    """
    `[(noeud, genre, numero_ecran)]` pour les nœuds porteurs de contenu.

    La racine et les nœuds transparents (sans `content_type`) sont écartés :
    ils portent la structure, pas le texte.
    """
    if noeuds is None:
        noeuds = list(document.nodes.select_related("content_type")
                      .prefetch_related("content_object").order_by("path"))

    niveaux = {}
    if document.schema:
        niveaux = {n.profondeur: n for n in document.schema.niveaux.all()}

    compteurs_document, compteurs_parent = {}, {}
    # Le numéro déjà attribué à chaque chemin : un sous-paragraphe se désigne
    # par celui de son parent suivi de sa lettre — « 57a » —, jamais par une
    # lettre seule, qui ne dirait pas de quel paragraphe il est la suite.
    numero_par_chemin = {}
    sortie = []

    for noeud in noeuds:
        if noeud.depth == 1 or noeud.content_type_id is None:
            continue

        niveau = niveaux.get(noeud.depth)
        role = niveau.role if niveau else None
        genre = genre_du_noeud(role, noeud.item, texte_du_noeud(noeud))
        chemin_parent = noeud.path[:-LibraryNode.steplen]

        numero = ""
        if genre == "sous_paragraphe":
            cle = (noeud.depth, chemin_parent)
            compteurs_parent[cle] = compteurs_parent.get(cle, 0) + 1
            lettre = chr(ord("a") + (compteurs_parent[cle] - 1) % 26)
            numero = f"{numero_par_chemin.get(chemin_parent, '')}{lettre}"
        elif niveau and niveau.format_numero != FormatNumero.AUCUN \
                and genre in ("paragraphe", "titre"):
            if niveau.portee == PorteeNumero.PARENT:
                cle = (noeud.depth, chemin_parent)
                compteurs_parent[cle] = compteurs_parent.get(cle, 0) + 1
                rang = compteurs_parent[cle]
            else:
                compteurs_document[noeud.depth] = \
                    compteurs_document.get(noeud.depth, 0) + 1
                rang = compteurs_document[noeud.depth]
            numero = formater(rang, niveau.format_numero)

        # Une énumération garde un numéro vide : sa puce est déjà dans son
        # texte, et en calculer une seconde produirait « a) a) Alexia David… ».
        numero_par_chemin[noeud.path] = numero
        sortie.append((noeud, genre, numero))

    return sortie


def index_numeros(document):
    """
    `{statement_pk: "44 (dépôt 28)"}` — comment désigner un paragraphe.

    C'est la fonction que les rapports appellent. Elle rend impossible de citer
    un numéro sans l'autre, ce qui est tout son objet.
    """
    index = {}
    for noeud, genre, numero in numeroter(document):
        if genre not in ("paragraphe", "titre", "conclusion", "sous_paragraphe"):
            continue
        item = noeud.item or ""
        # « (dépôt M) » ne se dit que là où M EST un numéro de dépôt. Sur les
        # actes reproduits, `item` porte l'incipit du paragraphe et non un
        # numéro : l'ajouter produisait « 1 (dépôt Les parties se sont
        # fréquentées et fait...) ».
        if numero and item.strip().isdigit() and numero != item:
            libelle = f"{numero} (dépôt {item})"
        else:
            libelle = numero or item or "?"
        index[noeud.object_id] = libelle
    return index
