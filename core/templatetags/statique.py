"""
Adresse d'un fichier statique, horodatée.

`{% static %}` rend toujours la même adresse : quand le fichier change, le
navigateur n'a aucune raison de le redemander. Et le serveur n'envoie ni
`Cache-Control` ni `ETag`, seulement `Last-Modified` — le navigateur applique
alors une fraîcheur heuristique, de l'ordre d'un dixième de l'âge du fichier.
Un script vieux de dix mois est donc tenu pour frais pendant un mois, sans même
une revalidation.

Le plugin d'insertion de citations en a fait les frais : sa réponse serveur a
changé de forme, le navigateur exécutait encore la version précédente, et
l'erreur — `data[type].map is not a function` — désignait un code qui n'existait
plus dans le fichier.

Ce tag suffixe l'adresse de la date de dernière écriture du fichier. Elle change
quand le fichier change, et alors seulement. À utiliser pour ce qu'on modifie
soi-même ; les paquets tiers, qui ne bougent qu'à une mise à jour de
dépendance, n'en ont pas besoin.
"""

import os

from django import template
from django.contrib.staticfiles import finders
from django.templatetags.static import static

register = template.Library()


@register.simple_tag
def statique(chemin):
    adresse = static(chemin)
    fichier = finders.find(chemin)
    if not fichier:
        # Fichier introuvable par les chercheurs (collecté sans les sources,
        # par exemple) : mieux vaut une adresse sans version qu'une erreur.
        return adresse
    try:
        horodatage = int(os.path.getmtime(fichier))
    except OSError:
        return adresse
    return f"{adresse}{'&' if '?' in adresse else '?'}v={horodatage}"
