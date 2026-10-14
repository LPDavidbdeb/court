"""
La numérotation d'un document — une seule implémentation, deux régimes.

QUEL NUMÉRO PORTE CE PARAGRAPHE ? La réponse dépend du document, pas du
paragraphe, et surtout pas du Statement, qui peut être partagé entre deux actes
et y porter deux numéros.

    AUTO    le numéro se RECALCULE depuis la structure et le schéma. Insérer un
            paragraphe renumérote la suite — ce qu'on attend d'un texte en cours
            de rédaction.

    STORED  le numéro est CONSERVÉ sur le nœud (`LibraryNode.paragraph_number`).
            C'est le régime d'un acte imprimé : sur la demande du 24 juillet
            2026, le papier porte 41 là où le fichier de travail porte 43. Ce 41
            n'obéit à aucune règle — Word repart du premier numéro de chaque bloc
            de liste et incrémente, de sorte qu'un numéro sauté décale tout le
            bloc. Aucun recalcul ne le retrouvera.

CE QUE `item` N'EST PAS. `item` porte le numéro du Markdown de travail. Il a
longtemps été présenté comme « le numéro du dépôt », et les rapports écrivaient
« § 44 (dépôt 28) » pour obliger à citer les deux ensemble. Cette parenthèse est
ABROGÉE : elle annonçait un numéro de dépôt que `item` ne porte pas. Chaque
version affiche désormais SON numéro, et la concordance (`document_manager.
concordance`) porte le lien entre versions — c'est là qu'il appartient.

UN NUMÉRO SE RÉSOUT SUR LE DOCUMENT ENTIER. Afficher un sous-ensemble, masquer
les pièces, filtrer un axe : aucune de ces lectures ne doit changer le numéro
d'un paragraphe. Les vues résolvent donc sur le document complet, puis filtrent.
"""
import re

from document_manager.models import (
    FormatNumero, LibraryNode, NumberingMode, PorteeNumero, RoleNiveau,
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


# ---------------------------------------------------------------------------
# LES DOCUMENTS SANS SCHÉMA
#
# Un document peut entrer dans la base avant que sa forme soit arrêtée : le
# schéma est une LECTURE, pas une contrainte d'écriture (voir SchemaNiveaux).
# Quatre documents produits sont aujourd'hui dans ce cas.
#
# Ils n'étaient pourtant pas sans numéros à l'écran : l'éditeur PRODUCED, la
# vue backbone et la liste des énoncés contestés portaient chacun le MÊME
# compteur local — décimal à la profondeur 2, lettre à la 3, romain minuscule
# à la 4, les deux derniers repartant sous chaque parent. Centraliser la
# résolution sans reprendre cette grammaire aurait vidé ces trois écrans.
#
# Elle est donc reprise ici, telle quelle et explicitement. Ce n'est pas une
# grammaire nouvelle, et surtout pas une grammaire déduite d'`item` : c'est le
# comportement effectivement en service, écrit une fois au lieu de trois. Un
# document qui reçoit un schéma cesse aussitôt d'y être soumis.
# ---------------------------------------------------------------------------

ROMAINS_MIN = {1: 'i', 2: 'ii', 3: 'iii', 4: 'iv', 5: 'v', 6: 'vi', 7: 'vii',
               8: 'viii', 9: 'ix', 10: 'x'}


def _numeroter_sans_schema(noeuds):
    """`[(noeud, genre, numero)]` selon la grammaire héritée des vues."""
    compteurs_parent = {}
    compteur_doc = 0
    sortie = []
    for noeud in noeuds:
        if noeud.depth == 1 or noeud.content_type_id is None:
            continue
        chemin_parent = noeud.path[:-LibraryNode.steplen]
        if noeud.depth == 2:
            compteur_doc += 1
            numero = str(compteur_doc)
        elif noeud.depth in (3, 4):
            cle = (noeud.depth, chemin_parent)
            compteurs_parent[cle] = compteurs_parent.get(cle, 0) + 1
            rang = compteurs_parent[cle]
            numero = (chr(96 + rang) if noeud.depth == 3
                      else ROMAINS_MIN.get(rang, str(rang)))
        else:
            sortie.append((noeud, "libre", ""))
            continue
        sortie.append((noeud, "paragraphe", numero))
    return sortie


def numeroter(document, noeuds=None):
    """
    `[(noeud, genre, numero_ecran)]` pour les nœuds porteurs de contenu.

    La racine et les nœuds transparents (sans `content_type`) sont écartés :
    ils portent la structure, pas le texte.
    """
    if noeuds is None:
        noeuds = list(document.nodes.select_related("content_type")
                      .prefetch_related("content_object").order_by("path"))

    if not document.schema:
        return _numeroter_sans_schema(noeuds)

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


# ---------------------------------------------------------------------------
# LA RÉSOLUTION COMMUNE
#
# Tout ce qui affiche, exporte ou rapporte un numéro passe par ici. Il y avait
# auparavant quatre compteurs parallèles — un par vue — et rien ne garantissait
# qu'ils s'accordent ; deux d'entre eux numérotaient même un sous-ensemble
# filtré, de sorte qu'un paragraphe changeait de numéro selon l'écran qui
# l'affichait.
# ---------------------------------------------------------------------------

# Les genres qui portent un NUMÉRO DE PARAGRAPHE, c'est-à-dire ceux dont le
# cahier dit qu'en mode STORED leur numéro se lit sur le nœud. Un titre n'en est
# pas : « § I — LES PARTIES » est une section, et sa numérotation romaine reste
# structurelle même dans un acte imprimé.
GENRES_NUMEROTES_PAR_LA_SOURCE = ("paragraphe",)

# Les genres qu'un index destiné à la citation doit retenir.
GENRES_CITABLES = ("paragraphe", "titre", "conclusion", "sous_paragraphe")


class NumeroResolu:
    """Ce qu'on sait du numéro d'une occurrence, et d'où il vient."""

    __slots__ = ("noeud", "genre", "numero", "origine", "manquant", "calcule")

    def __init__(self, noeud, genre, numero, origine, manquant, calcule):
        self.noeud = noeud
        self.genre = genre
        self.numero = numero
        # 'STORED' | 'AUTO' | '' — d'où vient `numero`.
        self.origine = origine
        # True quand le document est en STORED, que ce paragraphe devrait porter
        # un numéro conservé, et qu'il n'en porte pas. Le numéro reste VIDE :
        # un numéro calculé mis à sa place serait une invention.
        self.manquant = manquant
        # Le numéro qu'AURAIT donné le calcul. Conservé pour le diagnostic et
        # la détection de conflit, jamais affiché en mode STORED.
        self.calcule = calcule

    @property
    def pk(self):
        return self.noeud.pk

    def __repr__(self):
        return (f"<NumeroResolu nœud={self.noeud.pk} {self.genre} "
                f"{self.numero!r} ({self.origine})>")


class AmbiguiteOccurrence(Exception):
    """
    Un Statement apparaît plusieurs fois : il n'a pas « un » numéro.

    Levée plutôt que résolue par `.first()`. Choisir arbitrairement la première
    occurrence produit un numéro juste par hasard et faux sans prévenir.
    """


def resoudre(document, noeuds=None):
    """
    `[NumeroResolu]` pour les nœuds porteurs de contenu du document ENTIER.

    `noeuds` ne sert qu'à éviter une requête lorsque l'appelant détient déjà la
    liste COMPLÈTE. Passer un sous-ensemble filtré fausserait les compteurs :
    pour n'afficher qu'une partie, résoudre d'abord, filtrer ensuite.
    """
    if noeuds is None:
        noeuds = list(document.nodes.select_related("content_type")
                      .prefetch_related("content_object").order_by("path"))

    stored = document.numbering_mode == NumberingMode.STORED
    sortie = []
    for noeud, genre, calcule in numeroter(document, noeuds):
        conserve = (noeud.paragraph_number or "").strip()
        if not stored:
            # Une valeur conservée ne prend jamais la main sur le calcul, et la
            # lecture ne la réécrit pas : elle reste disponible pour le jour où
            # le document passe en STORED.
            sortie.append(NumeroResolu(noeud, genre, calcule, 'AUTO' if calcule else '',
                                       False, calcule))
            continue
        if conserve:
            sortie.append(NumeroResolu(noeud, genre, conserve, 'STORED', False, calcule))
        elif genre in GENRES_NUMEROTES_PAR_LA_SOURCE:
            sortie.append(NumeroResolu(noeud, genre, "", 'STORED', True, calcule))
        else:
            # Titres, énumérations, mentions : leur numéro reste structurel même
            # dans un acte imprimé, et leur absence n'est pas un manque.
            sortie.append(NumeroResolu(noeud, genre, calcule, 'AUTO' if calcule else '',
                                       False, calcule))
    return sortie


def index_par_noeud(document, noeuds=None):
    """
    `{LibraryNode.pk: "41"}` — l'index de référence.

    C'est l'OCCURRENCE qui porte le numéro. Un index par Statement ne peut pas
    répondre lorsqu'un énoncé est repris deux fois.
    """
    return {r.noeud.pk: r.numero for r in resoudre(document, noeuds)}


def index_par_statement(document, noeuds=None, strict=True):
    """
    `{statement_pk: "41"}` — ADAPTATEUR pour les interfaces anciennes.

    Lève `AmbiguiteOccurrence` si un Statement apparaît plusieurs fois dans le
    document. `strict=False` renvoie alors le couple `(index, ambigus)` sans
    trancher : les Statements ambigus sont ABSENTS de l'index, jamais résolus
    par leur première occurrence.
    """
    index, vus, ambigus = {}, {}, set()
    for r in resoudre(document, noeuds):
        if r.genre not in GENRES_CITABLES or r.noeud.object_id is None:
            continue
        sid = r.noeud.object_id
        if sid in vus and vus[sid] != r.numero:
            ambigus.add(sid)
        vus.setdefault(sid, r.numero)
        index[sid] = r.numero
    for sid in ambigus:
        index.pop(sid, None)
    if ambigus and strict:
        raise AmbiguiteOccurrence(
            f"Document {document.pk} : {len(ambigus)} Statement(s) apparaissent "
            f"à plusieurs numéros ({sorted(ambigus)[:5]}…). Désigner "
            f"l'occurrence (LibraryNode) plutôt que l'énoncé."
        )
    return index if strict else (index, ambigus)


def numero_de_noeud(noeud):
    """Le numéro d'UNE occurrence, résolu dans son propre document."""
    return index_par_noeud(noeud.document).get(noeud.pk, "")


def numeros_manquants(document):
    """Les occurrences qu'un export complet ne peut pas numéroter (C03/EX03)."""
    return [r for r in resoudre(document) if r.manquant]


def conflits_stored(document, attendus):
    """
    `[(noeud, present, attendu)]` — où un numéro déjà conservé contredit la
    valeur qu'on s'apprête à écrire.

    Appelé avant la reprise : on ne réécrit pas en silence un numéro que
    quelqu'un a posé.
    """
    out = []
    for noeud in document.nodes.all():
        present = (noeud.paragraph_number or "").strip()
        attendu = attendus.get(noeud.pk)
        if present and attendu is not None and present != attendu:
            out.append((noeud, present, attendu))
    return out


def pour_affichage(numero):
    """
    « 41 » → « 41. » — la ponctuation d'une liste, et rien de plus.

    LA PONCTUATION N'EST PAS UN COMPTEUR. Les vues suffixaient leur numéro d'un
    point ; ce point est une convention d'affichage, et le fait qu'il soit posé
    ici plutôt que dans chaque vue est précisément ce qui évite qu'une sortie
    se remette à calculer pour pouvoir formater.
    """
    return f"{numero}." if numero else ""
