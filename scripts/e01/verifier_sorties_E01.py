"""
T17 — ce que chaque sortie active affiche réellement.

LA VÉRIFICATION NE PASSE PAS PAR LE BALISAGE. Chaque gabarit entoure le numéro
d'un marquage différent ; une expression calquée sur l'un d'eux ne dirait rien
des autres. On cherche donc le TEXTE du paragraphe dans la page, puis le numéro
attendu juste avant lui.

Les attentes viennent de la table de concordance publiée, lue ici
indépendamment du résolveur.
"""
import html as htmlmod
import json
import os
import re
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_copie_e01')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client

from document_manager import numerotation
from document_manager.models import Document, LibraryNode

CONC = json.load(open('legal/amendements/01_avant_notification/concordance_md_imprime.json'))
ATTENDUS = {l['numero_md']: l['numero_imprime'] for l in CONC['lignes']}

RE_LIBELLE_ABROGE = re.compile(r"\(dépôt\s+[\w-]+\)")

# L'éditeur PRODUCED porte l'identifiant du nœud sur la même balise que son
# numéro : on vérifie le couple exact, sans dépendre de la proximité du texte,
# que les boutons de l'éditeur séparent.
# Ancré sur le <li> du nœud :  figure aussi sur des éléments
# internes, et un appariement naïf décalerait chaque numéro d'un cran.
RE_NOEUD_EDITEUR = re.compile(
    r'library-node-item[^>]*?data-node-id="(\d+)".*?'
    r'<span class="node-numbering">([^<]*)</span>', re.S)
RE_BALISES = re.compile(r"<[^>]+>")


def texte_nu(page):
    return htmlmod.unescape(RE_BALISES.sub(" ", page))


def numero_avant(page_nue, incipit, numero):
    """Le numéro attendu figure-t-il juste avant ce paragraphe ?"""
    i = page_nue.find(incipit)
    if i < 0:
        return None            # le paragraphe n'est pas dans cette sortie
    amont = page_nue[max(0, i - 120):i]
    return bool(re.search(r"(?<![\w-])" + re.escape(numero) + r"\.?\s*$",
                          amont.rstrip()))


U = get_user_model()
u, _ = U.objects.get_or_create(username='e01_controle', defaults={'is_staff': True})
u.is_superuser = True; u.is_staff = True; u.set_password('x'); u.save()
c = Client(); c.force_login(u)

# Pages dont le gabarit n'a jamais affiché de numéro de paragraphe : la vue
# utilise bien la résolution commune, mais la page ne la rend pas. Constat, et
# non anomalie — le rapport le signale comme limite.
SANS_NUMERO_AFFICHE = {"contestation 9", "contestation 1"}

ROUTES = [
    ("clean 9", "/documents/clean/9/", 9),
    ("interactive 9", "/documents/interactive/9/", 9),
    ("cinematic 9", "/documents/cinematic/9/", 9),
    ("schema 9", "/documents/schema/9/", 9),
    ("publique 9", "/document/9/", 9),
    ("editeur PRODUCED 9", "/documents/produced/editor/9/", 9),
    ("contestation 9", "/documents/contestation/9/", 9),
    ("backbone 1", "/documents/backbone/1/", 1),
    ("contestation 1", "/documents/contestation/1/", 1),
    ("énoncés contestés", "/documents/perjury-elements/", None),
    ("editeur PRODUCED 10", "/documents/produced/editor/10/", 10),
    ("backbone 10", "/documents/backbone/10/", 10),
]

# Les paragraphes témoins de T03, plus un suffixe.
TEMOINS = ("43", "72", "142", "22-A")
echec = 0

print(f"{'sortie':<22}{'code':<6}{'témoins vus':<14}{'numéros justes':<16}"
      f"{'libellé abrogé':<15}{'état'}")
print("-" * 104)
for nom, url, doc_pk in ROUTES:
    r = c.get(url, follow=True)
    page = r.content.decode('utf-8', 'replace')
    nue = " ".join(texte_nu(page).split())
    abroge = bool(RE_LIBELLE_ABROGE.search(nue))
    vus = justes = 0
    if "editeur" in nom and doc_pk is not None:
        index = numerotation.index_par_noeud(Document.objects.get(pk=doc_pk))
        for pk, num in RE_NOEUD_EDITEUR.findall(page):
            attendu = index.get(int(pk))
            if not attendu:
                continue
            vus += 1
            justes += 1 if num.strip().rstrip('.') == attendu else 0
    elif nom in SANS_NUMERO_AFFICHE:
        pass
    elif doc_pk == 9:
        for md in TEMOINS:
            n = LibraryNode.objects.filter(document_id=9, item=md).first()
            incipit = " ".join((n.content_object.text or "")[:45].split())
            res = numero_avant(nue, incipit, ATTENDUS[md])
            if res is None:
                continue
            vus += 1
            justes += 1 if res else 0
    elif nom == "énoncés contestés":
        # Les identifiants « C-1-41 » doivent porter le numéro résolu de
        # l'occurrence contestée dans SON document.
        from django.contrib.contenttypes.models import ContentType
        from document_manager.models import Statement
        ct = ContentType.objects.get_for_model(Statement)
        ids = list(Statement.objects.filter(is_true=False, is_falsifiable=True)
                   .values_list('pk', flat=True))
        docs = sorted(set(LibraryNode.objects
                          .filter(content_type=ct, object_id__in=ids)
                          .values_list('document_id', flat=True)))
        attendus = set()
        for i, dpk in enumerate(docs, start=1):
            index = numerotation.index_par_noeud(Document.objects.get(pk=dpk))
            for n in LibraryNode.objects.filter(document_id=dpk, content_type=ct,
                                                object_id__in=ids):
                num = index.get(n.pk)
                attendus.add(f"C-{i}-{num}" if num else f"C-{i}")
        # Le badge d'un énoncé contesté, et non l'en-tête du document, qui
        # porte « C-1 » tout seul et n'est pas une désignation de paragraphe.
        rendus = re.findall(
            r'badge bg-warning text-dark me-3 mt-1">\s*([^<]+?)\s*<', page)
        vus = len(rendus)
        justes = sum(1 for r in rendus if r in attendus)
    elif doc_pk is not None:
        d = Document.objects.get(pk=doc_pk)
        index = numerotation.index_par_noeud(d)
        for n in d.nodes.select_related('content_type').order_by('path')[:60]:
            num = index.get(n.pk)
            obj = n.content_object
            if not num or obj is None or not getattr(obj, 'text', ''):
                continue
            incipit = " ".join(obj.text[:45].split())
            res = numero_avant(nue, incipit, num)
            if res is None:
                continue
            vus += 1
            justes += 1 if res else 0
    if nom in SANS_NUMERO_AFFICHE:
        etat = "n/a — gabarit sans numéro"
        vus = justes = 0
    elif vus and justes == vus:
        etat = "conformes"
    elif vus == 0:
        etat = "aucun témoin visible"
    else:
        etat = f"ÉCART {vus - justes}"
        echec += 1
    if abroge:
        echec += 1
    print(f"{nom:<22}{r.status_code:<6}{vus:<14}{justes:<16}"
          f"{('PRÉSENT' if abroge else 'absent'):<15}{etat}")

print()
for md in TEMOINS:
    n = LibraryNode.objects.filter(document_id=9, item=md).first()
    attendu = ATTENDUS[md]
    rendu = numerotation.index_par_noeud(Document.objects.get(pk=9)).get(n.pk)
    marque = "OK" if rendu == attendu else "ÉCART"
    print(f"  Markdown {md:<5} → imprimé attendu {attendu:<6} résolu {rendu:<6} {marque}")
    if rendu != attendu:
        echec += 1

print("\nVERDICT :", "CONFORME" if echec == 0 else f"{echec} ANOMALIE(S)")
sys.exit(1 if echec else 0)
