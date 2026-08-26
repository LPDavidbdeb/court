"""
Lire les cotes que la demande de juillet invoque, et les résoudre contre son
bordereau.

Un paragraphe de la demande écrit « tel qu'il appert des pièces P-49.1, P-49.2
et P-72 ». C'est la seule chose que le tribunal lit, et c'est une chaîne de
caractères : rien n'y garantit que P-72 existe, rien ne permet de l'interroger.
Ce module est le pont entre cette prose et `BordereauDepotJuillet`.

IL NE CONNAÎT QUE LE DÉPÔT. Pas d'axes, pas de `Fait`, pas d'exploration en
cours — la demande déposée et le bordereau déposé, rien d'autre. C'est ce qui
garantit qu'un rapport sur le dépôt ne puisse pas se mettre à parler d'autre
chose.

IL N'ÉCRIT RIEN ET NE JUGE RIEN. Deux commandes l'appellent — l'une persiste,
l'autre constate — et il existe pour qu'elles ne divergent jamais dans leur
lecture des cotes.

LES LIASSES. « P-43 » peut désigner une pièce ou la racine d'une liasse de
dix-neuf. Dans le second cas le paragraphe invoque les dix-neuf, et la
résolution les retourne toutes en marquant l'expansion : le texte a nommé la
liasse, pas chacune de ses pièces.
"""
import re

from django.contrib.contenttypes.models import ContentType

from case_manager.models import BordereauDepotJuillet
from document_manager.models import LibraryNode, Statement

# « P-43 », « P-43.7 ». La cotation du dépôt, sous-cotes comprises.
RE_COTE = re.compile(r"\bP-(\d+(?:\.\d+)?)\b")


def cotes_citees(texte):
    """Les cotes qu'un texte invoque, dédoublonnées, dans l'ordre d'apparition."""
    vues, sortie = set(), []
    for brut in RE_COTE.findall(texte or ""):
        cote = f"P-{brut}"
        if cote not in vues:
            vues.add(cote)
            sortie.append(cote)
    return sortie


def index_bordereau():
    """
    `({cote: entrée}, {cote_racine: [entrées]})`, en une seule lecture.

    Les deux index sont retournés ensemble parce que la résolution a besoin des
    deux : une cote citée est soit une pièce, soit la racine d'une liasse, et on
    ne sait laquelle qu'après avoir cherché dans les deux.
    """
    par_cote, par_racine = {}, {}
    # select_related : le type de la pièce est lu pour chaque entrée, ici comme
    # chez tous les appelants. Sans lui, une requête par entrée.
    for e in BordereauDepotJuillet.objects.select_related('content_type'):
        if e.cote:
            par_cote[e.cote] = e
        if e.cote_racine:
            par_racine.setdefault(e.cote_racine, []).append(e)
    return par_cote, par_racine


def resoudre(cote, index):
    """
    `(entrées, mode)` — les lignes du bordereau que cette cote désigne.

      'exacte'   la cote est une pièce ; une entrée.
      'liasse'   la cote est une racine ; toutes les pièces de la liasse.
      'inconnue' aucune correspondance. La prose cite une cote qui n'existe pas
                 au bordereau : à corriger dans le TEXTE, jamais en base.
    """
    par_cote, par_racine = index
    if cote in par_cote:
        return [par_cote[cote]], 'exacte'
    if cote in par_racine:
        return sorted(par_racine[cote], key=lambda e: (e.sous_rang or 0)), 'liasse'
    return [], 'inconnue'


def paragraphes(document_id):
    """
    `[(node, statement)]` — les paragraphes d'un document, dans l'ordre de
    l'arbre. Seuls les nœuds portant un `Statement` sont retournés : un titre
    de section ne cite pas de pièce.
    """
    ct = ContentType.objects.get_for_model(Statement)
    noeuds = list(LibraryNode.objects.filter(
        document_id=document_id, content_type=ct).order_by('path'))
    textes = Statement.objects.in_bulk([n.object_id for n in noeuds])
    return [(n, textes[n.object_id]) for n in noeuds if n.object_id in textes]


def lecture_prose(document_id):
    """
    Ce que la prose invoque, paragraphe par paragraphe.

    Retourne `[(node, statement, appuis, inconnues)]` où `appuis` est une liste
    de `(entrée, cote_citée, via_liasse)` dédoublonnée par pièce, et `inconnues`
    les cotes citées qui ne correspondent à rien. Les paragraphes n'invoquant
    aucune cote sont omis : un fait peut être appuyé par zéro pièce, et cela ne
    laisse simplement aucune trace à persister.
    """
    index = index_bordereau()
    sortie = []
    for node, stmt in paragraphes(document_id):
        appuis, inconnues, vus = [], [], set()
        for cote in cotes_citees(stmt.text):
            entrees, mode = resoudre(cote, index)
            if mode == 'inconnue':
                inconnues.append(cote)
                continue
            for e in entrees:
                if e.pk in vus:
                    continue
                vus.add(e.pk)
                appuis.append((e, cote, mode == 'liasse'))
        if appuis or inconnues:
            sortie.append((node, stmt, appuis, inconnues))
    return sortie


def url_piece(obj):
    """
    L'adresse de TRAVAIL de la pièce, si le modèle en expose une.

    ⚠️ `get_absolute_url` d'abord, `get_public_url` seulement à défaut — et
    l'ordre est porteur. Trois modèles distinguent les deux : `PDFDocument`,
    `Email` et `Document` renvoient par `get_public_url` vers une vue publique
    de PARTAGE, exemptée du contrôle superutilisateur et dépourvue de tout
    outil d'édition. Un lien posé dans l'acte est un outil de travail : il doit
    mener là où l'on peut examiner la pièce, pas là où on la montre à un tiers.
    """
    if obj is None:
        return None
    for methode in ('get_absolute_url', 'get_public_url'):
        f = getattr(obj, methode, None)
        if callable(f):
            try:
                return f()
            except Exception:
                continue
    return None


def libelle_piece(entree, obj):
    """
    Ce que le bordereau dit de la pièce, à défaut ce que la pièce dit d'elle.

    La colonne du bordereau est privilégiée : c'est le libellé DÉPOSÉ. Une
    pièce versée depuis n'en a pas, et se décrit alors par son propre modèle.
    """
    if (entree.description or '').strip():
        return entree.description.strip()
    if obj is not None:
        for methode in ('get_exhibit_description', 'get_exhibit_title'):
            f = getattr(obj, methode, None)
            if callable(f):
                try:
                    v = (f() or '').strip()
                    if v:
                        return v
                except Exception:
                    continue
    return ''


def _objets_en_bloc(entrees):
    """
    `{(content_type_id, object_id): objet}` en une requête par modèle.

    Les entrées du bordereau pointent vers sept modèles par clé générique.
    Résolues une à une, `entree.content_object` coûte une requête par pièce —
    plus de quatre cents pour un acte entier, la quasi-totalité du coût de la
    page. Regroupées par modèle, il en reste sept.
    """
    par_type = {}
    for e in entrees:
        if e.content_type_id:
            par_type.setdefault(e.content_type_id, set()).add(e.object_id)
    objets = {}
    for ct_id, ids in par_type.items():
        modele = ContentType.objects.get_for_id(ct_id).model_class()
        if modele is None:
            continue
        for pk, obj in modele.objects.in_bulk(ids).items():
            objets[(ct_id, pk)] = obj
    return objets


def arbre_des_appuis(document_id):
    """
    Les pièces d'un document, en arbre, par paragraphe et par cote citée.

    LA COTE ÉCRITE EST LA RACINE. Ce n'est pas l'appartenance d'une pièce à une
    liasse qui fixe la profondeur, c'est ce que le paragraphe a nommé. Un § qui
    écrit « P-43.7 » désigne une pièce et l'arbre s'arrête là, quand bien même
    cette pièce appartient à une liasse de dix-neuf ; un § qui écrit « P-43 »
    nomme la liasse, et les dix-neuf sont ses enfants.

        N = 0   le paragraphe ne cite rien — pas de racine du tout
        N = 1   racine ──> pièce
        N > 1   racine ──> liasse ──> pièces

    `via_liasse` porte cette distinction et vient de la résolution elle-même,
    pas d'un calcul refait ici.

    Retourne `{statement_id: {cote: noeud}}`, les cotes dans leur ordre
    d'apparition dans le texte. Un `noeud` porte la cote, sa profondeur, et ses
    pièces déjà résolues en adresse et en libellé — le rendu n'a plus rien à
    interroger.

    LA LECTURE VIENT DE LA PROSE, pas de `AppuiDepotJuillet`. Les deux
    concordent, et une commande le vérifie ; mais la prose est ce que le
    tribunal lit, et un lien doit désigner ce que la phrase désigne. Un texte
    remanié sans repersistage montre alors la divergence au lieu de la taire.
    """
    lecture = lecture_prose(document_id)
    objets = _objets_en_bloc(e for _n, _s, appuis, _i in lecture
                             for e, _c, _v in appuis)

    arbre = {}
    for node, stmt, appuis, inconnues in lecture:
        par_cote = {}
        for entree, cote, via_liasse in appuis:
            obj = objets.get((entree.content_type_id, entree.object_id))
            par_cote.setdefault(cote, {
                'cote': cote,
                'via_liasse': via_liasse,
                'pieces': [],
            })['pieces'].append({
                'cote': entree.cote or cote,
                'url': url_piece(obj),
                'libelle': libelle_piece(entree, obj),
                'reference': f"{entree.content_type.model}-{entree.object_id}"
                             if entree.content_type_id else '',
            })
        for cote in inconnues:
            # Citée par la prose, absente du bordereau. Elle reste affichée
            # telle quelle : la corriger relève du TEXTE, jamais du rendu.
            par_cote.setdefault(cote, {'cote': cote, 'via_liasse': False,
                                       'pieces': []})
        if par_cote:
            arbre[stmt.pk] = par_cote
    return arbre
