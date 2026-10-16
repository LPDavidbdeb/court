#!/usr/bin/env python
"""
Doublons de citations par source, et tout ce qui pointe vers une citation.

    .venv/bin/python docs/purge_quotes/mesure_doublons.py

Trois classes de paires, à l'intérieur d'une même source (courriel ou PDF) :

    identiques     même texte une fois normalisé (casse, accents, ponctuation)
    inclusion      l'une est contenue dans l'autre
    partiel        au moins un 8-gramme de mots en commun, sans inclusion

La comparaison se fait entre citations, pas contre la source : elle trouve les
candidats, elle ne dit pas laquelle est fidèle. Voir PLAN_FUSION_CITATIONS.md §3.

Lecture seule : ce script n'écrit jamais en base.
"""
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django  # noqa: E402
django.setup()

from django.apps import apps  # noqa: E402
from django.contrib.contenttypes.fields import GenericForeignKey  # noqa: E402
from django.contrib.contenttypes.models import ContentType  # noqa: E402

from email_manager.models import Quote as EmailQuote  # noqa: E402
from pdf_manager.models import Quote as PDFQuote  # noqa: E402


def normaliser(texte):
    texte = unicodedata.normalize('NFKD', texte or '').encode('ascii', 'ignore').decode().lower()
    return " ".join(re.sub(r"[^\w]+", " ", texte).split())


def ngrammes(mots, n=8):
    return {tuple(mots[k:k + n]) for k in range(len(mots) - n + 1)}


def paires(modele, champ_source):
    groupes = defaultdict(list)
    for q in modele.objects.only('id', champ_source, 'quote_text'):
        groupes[getattr(q, champ_source)].append((q.id, normaliser(q.quote_text)))

    classes = defaultdict(list)
    for source, citations in groupes.items():
        for i, (pk_a, a) in enumerate(citations):
            for pk_b, b in citations[i + 1:]:
                if not a or not b:
                    continue
                if a == b:
                    classes['identiques'].append((source, pk_a, pk_b))
                elif a in b or b in a:
                    classes['inclusion'].append((source, pk_a, pk_b))
                elif ngrammes(a.split()) & ngrammes(b.split()):
                    classes['partiel'].append((source, pk_a, pk_b))
    return groupes, classes


def main():
    for modele, champ, prefixe in ((EmailQuote, 'email_id', 'eq'),
                                   (PDFQuote, 'pdf_document_id', 'pq')):
        groupes, classes = paires(modele, champ)
        impliquees = {pk for liste in classes.values() for _, a, b in liste for pk in (a, b)}
        print(f"{modele._meta.label}: {sum(map(len, groupes.values()))} citations, "
              f"{len(groupes)} sources, {sum(len(v) > 1 for v in groupes.values())} "
              f"sources à plus d'une citation")
        for nom in ('identiques', 'inclusion', 'partiel'):
            liste = classes[nom]
            print(f"   {nom:<11} {len(liste):>3} paires   "
                  + " ".join(f"{prefixe}-{a}/{b}" for _, a, b in liste))
        print(f"   citations impliquées dans au moins une paire : {len(impliquees)}")
        print()

    # Tout ce qui pointe vers une citation. Les clés génériques n'ont aucune
    # contrainte en base : le collector de Django ne les voit pas.
    cts = {ContentType.objects.get_for_model(EmailQuote).id: 'eq',
           ContentType.objects.get_for_model(PDFQuote).id: 'pq'}
    print("Références")
    for modele in (EmailQuote, PDFQuote):
        for rel in modele._meta.related_objects:
            if rel.many_to_many:
                n = rel.field.remote_field.through.objects.count()
                print(f"   M2M  {rel.related_model._meta.label}.{rel.field.name:<20} {n}")
    for modele in apps.get_models():
        for champ in modele._meta.private_fields:
            if isinstance(champ, GenericForeignKey):
                ids = modele.objects.filter(
                    **{f"{champ.ct_field}_id__in": list(cts)}
                ).values_list(f"{champ.ct_field}_id", flat=True)
                compte = Counter(cts[i] for i in ids)
                print(f"   GFK  {modele._meta.label:<40} {dict(compte) or 0}")


if __name__ == '__main__':
    main()
