#!/usr/bin/env python
"""
Les citations existantes au regard de la règle « une citation est une phrase ».

    .venv/bin/python docs/purge_quotes/mesure_phrases.py

Chaque citation est située dans le texte brut de sa source (le corps du
courriel, la transcription du PDF), puis ses deux bornes sont confrontées aux
fins de phrase de la source :

    phrase entière              les deux bornes tombent sur une fin de phrase,
                                aucune fin de phrase à l'intérieur
    plusieurs phrases entières  bornes alignées, au moins une fin à l'intérieur
    fragment                    au moins une borne coupe une phrase
    non localisable             le texte stocké a été retouché ou élidé : il ne
                                se retrouve pas mot pour mot dans la source

Fin de phrase, ici : « . ? ! … » suivis d'un blanc, ou une ligne vide. C'est la
définition minimale ; les énumérations et le « : » ne sont pas traités à part,
ce qui est précisément ce que la mesure des expansions fait apparaître.

Lecture seule : ce script n'écrit jamais en base.
"""
import os
import re
import statistics
import sys
import unicodedata
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django  # noqa: E402
django.setup()

from django.contrib.contenttypes.models import ContentType  # noqa: E402

from document_manager.models import LibraryNode  # noqa: E402
from email_manager.models import Quote as EmailQuote  # noqa: E402
from pdf_manager.models import Quote as PDFQuote  # noqa: E402

FIN = re.compile(r'[.!?…]')
LETTRE = r'0-9A-Za-zÀ-ÿ'


def replier_meme_longueur(texte):
    """Sans accents et en minuscules, un caractère pour un caractère : les
    positions trouvées dans le texte replié valent dans le texte brut."""
    def un(c):
        d = unicodedata.normalize('NFD', c)
        return (d[0] if d else c).lower()
    return ''.join(un(c) for c in texte)


def mots(texte):
    d = unicodedata.normalize('NFD', texte or '')
    d = ''.join(c for c in d if not unicodedata.combining(c)).lower()
    return re.findall(r'[0-9a-z]+', d)


def est_borne(intervalle, au_bord):
    return au_bord or bool(FIN.search(intervalle)) or bool(re.search(r'\n\s*\n', intervalle))


def phrase_englobante(source, debut, fin):
    avant = list(re.finditer(r'[.!?…][»"\')\]]*\s+|\n\s*\n', source[:debut]))
    d = avant[-1].end() if avant else 0
    apres = re.search(r'[.!?…]|\n\s*\n', source[fin:])
    f = fin + apres.end() if apres else len(source)
    return d, f


def situer(citation):
    """(classe, longueur de la citation, longueur de la phrase englobante)."""
    source = citation.source_text or ''
    m = mots(citation.quote_text)
    if not source.strip() or len(m) < 2:
        return 'vide ou trop court', 0, 0
    motif = r'(?<![0-9a-z])' + r'[^0-9a-z]+'.join(map(re.escape, m)) + r'(?![0-9a-z])'
    trouve = re.search(motif, replier_meme_longueur(source))
    if not trouve:
        return 'non localisable', 0, 0
    a, b = trouve.start(), trouve.end()
    avant = re.search(rf'[^{LETTRE}]*$', source[:a]).group()
    apres = re.match(rf'[^{LETTRE}]*', source[b:]).group()
    debut_ok = est_borne(avant, a - len(avant) == 0)
    fin_ok = est_borne(apres, b + len(apres) >= len(source))
    internes = len(re.findall(r'[.!?…][»"\')\]]*\s+(?=\S)', source[a:b]))
    longueur = len(' '.join(source[a:b].split()))
    if debut_ok and fin_ok:
        return ('phrase entière' if internes == 0 else 'plusieurs phrases entières'), longueur, longueur
    d, f = phrase_englobante(source, a, b)
    return 'fragment', longueur, len(' '.join(source[d:f].split()))


def main():
    for modele, libelle in ((EmailQuote, 'courriels'), (PDFQuote, 'PDF')):
        classes = Counter()
        expansions = []
        for q in modele.objects.all():
            classe, longueur, phrase = situer(q)
            classes[classe] += 1
            if classe == 'fragment':
                expansions.append((q.pk, longueur, phrase))
        total = sum(classes.values())
        print(f"{libelle} ({total})")
        for classe, n in classes.most_common():
            print(f"   {classe:<28} {n:>4}  {100 * n / total:5.1f} %")
        if expansions:
            facteurs = [p / max(1, l) for _, l, p in expansions]
            longueurs = [p for _, _, p in expansions]
            print(f"   fragment → phrase : longueur médiane {statistics.median(longueurs):.0f} car., "
                  f"facteur médian ×{statistics.median(facteurs):.1f}, "
                  f"> 600 car. : {sum(x > 600 for x in longueurs)}")
            plus_grandes = sorted(expansions, key=lambda t: -t[2])[:6]
            print("   plus grandes expansions (pk, citation, phrase) :", plus_grandes)

        ct = ContentType.objects.get_for_model(modele)
        ids = LibraryNode.objects.filter(content_type=ct).values_list('object_id', flat=True)
        noeuds = Counter(situer(q)[0] for q in modele.objects.filter(pk__in=set(ids)))
        print(f"   citations portées par un LibraryNode : {dict(noeuds)}")
        print()


if __name__ == '__main__':
    main()
