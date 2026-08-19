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


def genre_du_noeud(role, item):
    """Nature réelle du bloc, au-delà de ce que la profondeur seule dit."""
    if role == RoleNiveau.PARAGRAPHE and RE_CONCLUSION.match(item or ""):
        return "conclusion"
    if role == RoleNiveau.PARAGRAPHE and not item:
        return "mention"
    if role == RoleNiveau.PARAGRAPHE:
        return "paragraphe"
    if role in (RoleNiveau.SECTION, RoleNiveau.SOUS_SECTION, RoleNiveau.THEME,
                RoleNiveau.SOUS_THEME, RoleNiveau.CHAPEAU):
        return "titre"
    return "libre"


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
    sortie = []

    for noeud in noeuds:
        if noeud.depth == 1 or noeud.content_type_id is None:
            continue

        niveau = niveaux.get(noeud.depth)
        role = niveau.role if niveau else None
        genre = genre_du_noeud(role, noeud.item)

        numero = ""
        if niveau and niveau.format_numero != FormatNumero.AUCUN \
                and genre in ("paragraphe", "titre"):
            if niveau.portee == PorteeNumero.PARENT:
                cle = (noeud.depth, noeud.path[:-LibraryNode.steplen])
                compteurs_parent[cle] = compteurs_parent.get(cle, 0) + 1
                rang = compteurs_parent[cle]
            else:
                compteurs_document[noeud.depth] = \
                    compteurs_document.get(noeud.depth, 0) + 1
                rang = compteurs_document[noeud.depth]
            numero = formater(rang, niveau.format_numero)

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
        if genre not in ("paragraphe", "titre", "conclusion"):
            continue
        item = noeud.item or ""
        if numero and item and numero != item:
            libelle = f"{numero} (dépôt {item})"
        else:
            libelle = numero or item or "?"
        index[noeud.object_id] = libelle
    return index
