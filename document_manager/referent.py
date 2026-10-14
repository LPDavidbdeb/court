"""
Identifier un acte déposé, puis constater qu'il n'a pas bougé.

DEUX CHOSES DISTINCTES, souvent confondues :

    la PROTECTION   empêche l'écriture. Elle vit dans `protection.py` et
                    consulte `ReferentHistorique`.

    l'INSTANTANÉ    permet de dire après coup « voici ce qui a changé ». Il ne
                    bloque rien. Pris seul, il donne l'illusion d'une garde :
                    on constaterait la dérive, une fois faite.

Les deux sont donc posées ensemble : la ligne de référent active les gardes,
l'instantané donne de quoi prouver qu'elles ont tenu.
"""
import hashlib

from django.db import transaction

from document_manager.models import (
    InstantaneNoeud, InstantaneReferent, LibraryNode, ReferentHistorique,
)


def _texte(noeud):
    obj = noeud.content_object
    if obj is None:
        return ""
    return (getattr(obj, "text", None) or getattr(obj, "quote_text", None)
            or getattr(obj, "titre", None) or "")


def _cotes_appuyantes(statement_pk, index_appuis):
    return ",".join(index_appuis.get(statement_pk, []))


def _index_appuis(document):
    """`{statement_pk: [cotes…]}` — les appuis de juillet, par paragraphe."""
    try:
        from case_manager.models import AppuiDepotJuillet
    except Exception:            # pragma: no cover - case_manager absent
        return {}
    index = {}
    qs = (AppuiDepotJuillet.objects
          .filter(statement__in=LibraryNode.objects
                  .filter(document=document).values_list('object_id', flat=True))
          .select_related('entree'))
    for a in qs:
        index.setdefault(a.statement_id, []).append(a.entree.cote or "(sans cote)")
    for v in index.values():
        v.sort()
    return index


@transaction.atomic
def prendre_instantane(referent, motif):
    """
    Fige l'état courant du référent : textes, arborescence, numéros, appuis.

    L'empreinte globale porte sur les lignes ORDONNÉES par chemin. Deux
    instantanés d'empreintes égales décrivent donc le même acte, au même ordre.
    """
    document = referent.document
    noeuds = list(document.nodes.select_related('content_type')
                  .prefetch_related('content_object').order_by('path'))
    index_appuis = _index_appuis(document)

    instantane = InstantaneReferent.objects.create(
        referent=referent, motif=motif, empreinte_globale="",
        nombre_noeuds=len(noeuds),
        nombre_appuis=sum(len(v) for v in index_appuis.values()),
    )

    lignes, h = [], hashlib.sha256()
    for n in noeuds:
        texte = _texte(n)
        emp = hashlib.sha256(texte.encode('utf-8')).hexdigest() if texte else ""
        cotes = _cotes_appuyantes(n.object_id, index_appuis)
        lignes.append(InstantaneNoeud(
            instantane=instantane, noeud_pk=n.pk, path=n.path, depth=n.depth,
            item=n.item or "", paragraph_number=n.paragraph_number or "",
            content_type_id_releve=n.content_type_id, object_id_releve=n.object_id,
            texte=texte, texte_sha256=emp, cotes_appuyantes=cotes,
        ))
        h.update(f"{n.pk}|{n.path}|{n.item}|{n.content_type_id}|{n.object_id}|"
                 f"{emp}|{cotes}\n".encode('utf-8'))

    InstantaneNoeud.objects.bulk_create(lignes, batch_size=500)
    instantane.empreinte_globale = h.hexdigest()
    instantane.save(update_fields=['empreinte_globale'])
    return instantane


def comparer(instantane, inclure_numeros=False):
    """
    Ce qui a changé depuis l'instantané.

    `inclure_numeros=False` par défaut : la reprise des numéros imprimés est
    précisément l'ajout de métadonnée que l'Epic autorise sur le référent, et
    la rapporter comme une dérive noierait les vraies. Elle reste comptée à
    part, sous `numeros`.
    """
    document = instantane.referent.document
    actuels = {n.pk: n for n in document.nodes.select_related('content_type')
               .prefetch_related('content_object')}
    index_appuis = _index_appuis(document)

    ecarts = {'textes': [], 'arborescence': [], 'items': [], 'appuis': [],
              'disparus': [], 'apparus': [], 'numeros': []}

    for ligne in instantane.noeuds.all():
        n = actuels.pop(ligne.noeud_pk, None)
        if n is None:
            ecarts['disparus'].append(ligne.noeud_pk)
            continue
        if _texte(n) != ligne.texte:
            ecarts['textes'].append(ligne.noeud_pk)
        if n.path != ligne.path or n.depth != ligne.depth:
            ecarts['arborescence'].append(ligne.noeud_pk)
        if (n.item or "") != ligne.item:
            ecarts['items'].append(ligne.noeud_pk)
        if _cotes_appuyantes(n.object_id, index_appuis) != ligne.cotes_appuyantes:
            ecarts['appuis'].append(ligne.noeud_pk)
        if (n.paragraph_number or "") != ligne.paragraph_number:
            ecarts['numeros'].append(ligne.noeud_pk)

    ecarts['apparus'] = sorted(actuels)
    if not inclure_numeros:
        ecarts['numeros_sont_des_metadonnees_autorisees'] = True
    return ecarts


def contenu_intact(ecarts):
    """Vrai si seules les métadonnées de numérotation ont changé."""
    return not any(ecarts[c] for c in
                   ('textes', 'arborescence', 'items', 'appuis',
                    'disparus', 'apparus'))


def referent_de(document):
    return ReferentHistorique.objects.filter(document=document).first()
