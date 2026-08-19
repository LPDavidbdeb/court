"""
L'état des axes pour une pièce donnée — union du triage et des appuis précis.

Une pièce peut être reliée à un axe de deux façons qui ne disent pas la même
chose (voir `RattachementAxe`). Toute vue qui affiche « les axes de cette
pièce » doit montrer l'union, et distinguer les deux : un axe adossé à un
`AppuiFait` porte une fonction probatoire nommée, un axe simplement coché ne
porte qu'un jugement de pertinence.

C'est aussi ce qui interdit de décocher le premier : une case ne doit pas
pouvoir supprimer un lien probatoire.
"""
from django.contrib.contenttypes.models import ContentType

from argument_manager.models import AppuiFait, Axe, RattachementAxe


def cle(objet):
    """(content_type_id, object_id) pour n'importe quelle pièce."""
    return (ContentType.objects.get_for_model(objet).id, objet.pk)


def etat_axes(objet):
    """
    Pour chaque axe du dossier : la pièce y est-elle rattachée, et comment ?

    Retourne une liste de dicts, un par axe :
        axe, coche (bool), rattachement_pk, appuis (liste), verrouille (bool)

    `verrouille` est vrai lorsqu'un `AppuiFait` adosse l'axe : la case reste
    affichée cochée, mais elle ne se décoche pas — il faudrait retirer l'appui,
    ce qui est une décision d'un autre ordre.
    """
    ct_id, obj_id = cle(objet)

    rattachements = {r.axe_id: r for r in RattachementAxe.objects.filter(
        content_type_id=ct_id, object_id=obj_id)}

    par_axe = {}
    appuis = (AppuiFait.objects
              .filter(content_type_id=ct_id, object_id=obj_id)
              .select_related('fait')
              .prefetch_related('fait__axes'))
    for ap in appuis:
        for axe in ap.fait.axes.all():
            par_axe.setdefault(axe.pk, []).append(ap)

    etat = []
    for axe in Axe.objects.all().order_by('nom'):
        appuis_axe = par_axe.get(axe.pk, [])
        r = rattachements.get(axe.pk)
        etat.append({
            'axe': axe,
            'coche': bool(r) or bool(appuis_axe),
            'rattachement_pk': r.pk if r else None,
            'note': r.note if r else '',
            'appuis': appuis_axe,
            'verrouille': bool(appuis_axe),
        })
    return etat


def axes_par_piece_union():
    """
    `{(content_type_id, object_id): [{axe, precis, role, fait}, …]}`

    L'index qu'utilise le tableau des cotes. `precis` distingue l'appui nommé
    du simple rattachement de triage — sans quoi le tableau afficherait au même
    rang une ATTESTATION datée et une case cochée.
    """
    index = {}

    for r in RattachementAxe.objects.select_related('axe'):
        index.setdefault((r.content_type_id, r.object_id), []).append({
            'axe': r.axe, 'precis': False, 'role': None,
            'role_libelle': 'pertinence', 'fait': None, 'note': r.note,
        })

    for ap in (AppuiFait.objects
               .select_related('fait')
               .prefetch_related('fait__axes')):
        for axe in ap.fait.axes.all():
            index.setdefault((ap.content_type_id, ap.object_id), []).append({
                'axe': axe, 'precis': True, 'role': ap.role,
                'role_libelle': ap.get_role_display(),
                'fait': ap.fait, 'note': ap.note,
            })

    # Un axe adossé à la fois par un appui et par une case coche apparaîtrait
    # deux fois : on garde la version précise, qui dit strictement plus.
    for k, entrees in index.items():
        precis = {e['axe'].pk for e in entrees if e['precis']}
        index[k] = [e for e in entrees if e['precis'] or e['axe'].pk not in precis]

    return index
