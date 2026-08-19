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
    for e in BordereauDepotJuillet.objects.all():
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
