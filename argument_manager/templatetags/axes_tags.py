"""
Le sélecteur d'axes, insérable dans n'importe quelle vue de détail.

    {% load axes_tags %}
    {% selecteur_axes object %}

Sept modèles peuvent figurer au registre des pièces, avec sept vues de détail
dans six applications. Intégrer le sélecteur sept fois produirait sept variantes
qui divergeraient. Une balise d'inclusion règle le problème une fois : elle
accepte n'importe quel objet et se charge elle-même de son état.
"""
from django import template

from argument_manager.axes_service import cle, etat_axes

register = template.Library()


@register.inclusion_tag('argument_manager/_selecteur_axes.html',
                        takes_context=True)
def selecteur_axes(context, objet, titre="Axes d'argumentation"):
    if objet is None or getattr(objet, 'pk', None) is None:
        return {'absent': True}
    ct_id, obj_id = cle(objet)
    etat = etat_axes(objet)
    return {
        'absent': False,
        'titre': titre,
        'ct_id': ct_id,
        'obj_id': obj_id,
        'etat': etat,
        'nb_coches': sum(1 for e in etat if e['coche']),
        'csrf_token': context.get('csrf_token', ''),
    }
