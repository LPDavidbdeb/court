"""
Adresse d'enregistrement d'un champ éditable.

Le gabarit ne peut pas atteindre `objet._meta` — Django interdit les attributs
commençant par un souligné — et la vue n'a pas à calculer une URL pour chaque
champ qu'elle affiche. Ce tag fait le lien : il nomme le modèle et le champ
dans l'adresse, et le point d'entrée vérifie que ce champ est éditable.
"""

from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def url_champ(objet, champ):
    return reverse('core:ajax_maj_champ',
                   args=[objet._meta.app_label, objet._meta.model_name, objet.pk, champ])
