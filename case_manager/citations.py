"""
Faire citer la bonne pièce, sans réécrire le texte.

LE PIÈGE. Un paragraphe écrit « tel qu'il appert de la pièce P-12 ». Une pièce
antérieure est versée ; dans l'ordre chronologique, la même source devient P-13.
Le réflexe est de chercher « P-12 » dans le texte et de le remplacer.

Ce réflexe détruit le dossier. « P-12 » peut désigner, dans la même base :

  — la pièce que CE paragraphe invoque, qu'il faut effectivement renuméroter ;
  — la cote d'une pièce DIFFÉRENTE, citée ailleurs ;
  — une cote reproduite dans une CITATION HISTORIQUE — « au paragraphe 18, la
    défenderesse invoquait P-12 » — qui rapporte ce qui a été écrit à l'époque
    et doit rester tel quel ;
  — et, plus loin dans le même texte, une date, une somme, un numéro de
    paragraphe d'un acte adverse, qu'un remplacement global toucherait aussi.

D'OÙ L'ANCRAGE. Chaque occurrence est rattachée à une PIÈCE, par son identité et
non par son libellé. Le libellé affiché se recalcule à la lecture depuis l'état
de cotation retenu ; le texte stocké n'est jamais modifié. Une occurrence sans
ancrage n'est pas renumérotée — elle est signalée, et bloque l'export strict.
"""
import re

from case_manager.cotes_concordance import index_cote_cible
from case_manager.models import AncrageCitation, BordereauDepotJuillet

# « P-12 », « P-43.7 ». Sert à PROPOSER des ancrages, jamais à en poser un : ce
# que cette expression trouve est une chaîne, pas une référence.
RE_COTE = re.compile(r"\bP-(\d+)(?:\.(\d+))?\b")


def reperer(texte):
    """`[(debut, fin, libelle)]` — les cotes écrites dans ce texte."""
    return [(m.start(), m.end(), m.group(0)) for m in RE_COTE.finditer(texte or "")]


def proposer_ancrages(noeud):
    """
    Les cotes repérées dans le texte d'une occurrence, avec la pièce que chaque
    libellé désignait au dépôt — À CONFIRMER, jamais posé d'office.

    Une proposition est marquée ambiguë lorsque le libellé ne désigne pas une
    pièce et une seule.
    """
    obj = noeud.content_object
    texte = getattr(obj, 'text', None) or ""
    propositions = []
    for debut, fin, libelle in reperer(texte):
        candidates = list(BordereauDepotJuillet.objects.filter(cote=libelle))
        propositions.append({
            'debut': debut, 'fin': fin, 'libelle_ecrit': libelle,
            'entree': candidates[0] if len(candidates) == 1 else None,
            'ambigu': len(candidates) != 1,
            'motif': ("" if len(candidates) == 1 else
                      f"{len(candidates)} pièce(s) portent la cote {libelle} au dépôt"),
        })
    return propositions


def rendre(noeud, index_cible=None, etat=None):
    """
    Le texte tel qu'il doit se lire sous la cotation cible.

    Seules les positions ANCRÉES et non littérales sont réécrites, de la fin
    vers le début pour que les index restants restent valides. Tout le reste du
    texte — y compris les « P-n » non ancrés — est rendu intact.
    """
    obj = noeud.content_object
    texte = getattr(obj, 'text', None) or ""
    if index_cible is None:
        index_cible = index_cote_cible()

    ancrages = list(noeud.ancrages_citation.select_related('entree')
                    .order_by('-debut'))
    rendu = texte
    remplacements, non_resolus = [], []
    for a in ancrages:
        if a.litterale:
            continue
        if not a.resolu:
            non_resolus.append({'debut': a.debut, 'libelle': a.libelle_ecrit,
                                'motif': 'ambigu' if a.ambigu else 'non rattaché'})
            continue
        cible = index_cible.get(a.entree_id)
        if cible is None:
            non_resolus.append({'debut': a.debut, 'libelle': a.libelle_ecrit,
                                'motif': 'pièce absente de l’état de cotation'})
            continue
        if rendu[a.debut:a.fin] != a.libelle_ecrit:
            non_resolus.append({
                'debut': a.debut, 'libelle': a.libelle_ecrit,
                'motif': 'le texte a changé depuis l’ancrage : positions périmées'})
            continue
        if cible != a.libelle_ecrit:
            remplacements.append({'de': a.libelle_ecrit, 'vers': cible,
                                  'entree': a.entree_id})
        rendu = rendu[:a.debut] + cible + rendu[a.fin:]

    return {'texte_rendu': rendu, 'texte_stocke': texte,
            'remplacements': remplacements, 'non_resolus': non_resolus,
            'litterales_preservees': [a.libelle_ecrit for a in ancrages if a.litterale]}


def citations_non_resolues(document):
    """
    Les références qui bloquent l'export strict (EX04).

    Une cote présente dans un texte sans ancrage n'est pas forcément une
    erreur : c'est peut-être une citation historique qu'on n'a pas encore
    qualifiée. Mais tant qu'elle n'est pas qualifiée, elle est indécidable —
    et c'est précisément pour cela qu'elle bloque.
    """
    from document_manager.models import LibraryNode
    index = index_cote_cible()
    blocages = []
    for n in (LibraryNode.objects.filter(document=document)
              .prefetch_related('content_object', 'ancrages_citation')):
        obj = n.content_object
        texte = getattr(obj, 'text', None) or ""
        if not texte:
            continue
        reperees = reperer(texte)
        if not reperees:
            continue
        ancres = {(a.debut, a.fin) for a in n.ancrages_citation.all()}
        for debut, fin, libelle in reperees:
            if (debut, fin) not in ancres:
                blocages.append({
                    'noeud': n.pk, 'libelle': libelle, 'debut': debut,
                    'motif': "cote écrite sans ancrage : ni rattachée à une "
                             "pièce, ni qualifiée de citation historique",
                })
        resultat = rendre(n, index)
        for nr in resultat['non_resolus']:
            blocages.append({'noeud': n.pk, 'libelle': nr['libelle'],
                             'debut': nr['debut'], 'motif': nr['motif']})
    return blocages
