"""
Rendu d'un document selon son schéma de niveaux, mis en page comme un acte.

Les autres vues affichent l'arbre tel qu'il est stocké. Celle-ci l'affiche tel
que le SCHÉMA le lit — chaque profondeur reçoit le rôle, le format de numéro et
la portée que le schéma lui attribue — et le présente comme il le serait devant
le tribunal.

La numérotation elle-même vit dans `document_manager.numerotation`, partagée
avec les commandes qui rapportent sur ce document. Deux implémentations
parallèles donneraient deux numéros différents au même paragraphe — et comme
l'une n'affiche que le numéro recalculé et l'autre que celui du dépôt, la
divergence resterait invisible.

La correspondance entre le numéro du dépôt et le numéro recalculé est CONSERVÉE
(elle vit dans `LibraryNode.item`) mais n'est pas affichée : elle est portée en
attribut `title` sur le numéro, donc lisible au survol sans encombrer la page.
"""
import html
import re

from django.shortcuts import get_object_or_404, render
from django.utils.safestring import mark_safe

from document_manager.models import Document
from document_manager.numerotation import numeroter


def texte_de(noeud):
    obj = noeud.content_object
    if obj is None:
        return None
    return (getattr(obj, "text", None) or getattr(obj, "quote_text", None)
            or getattr(obj, "titre", None) or str(obj))


def enrichir(texte):
    """
    Le texte vient d'une source markdown : **gras** et *italique* y subsistent.
    On échappe d'abord, on stylise ensuite — l'ordre inverse laisserait passer
    du HTML depuis le contenu.
    """
    t = html.escape(texte or "")
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", t)
    return mark_safe(t)


def schema_detail_view(request, pk):
    document = get_object_or_404(Document.objects.select_related("schema"), pk=pk)

    blocs = []
    renumerotes = 0
    for noeud, genre, numero in numeroter(document):
        item = noeud.item or ""
        if numero and item and numero != item:
            renumerotes += 1
        blocs.append({
            "genre": genre,
            "profondeur": noeud.depth,
            "numero": numero,
            # conservée, non affichée : lisible au survol du numéro
            "origine": item,
            "change": bool(numero and item and numero != item),
            "texte": enrichir(texte_de(noeud) or ""),
        })

    resume = {
        "paragraphes": sum(1 for b in blocs if b["genre"] == "paragraphe"),
        "conclusions": sum(1 for b in blocs if b["genre"] == "conclusion"),
        "renumerotes": renumerotes,
    }

    return render(request, "document_manager/schema_detail.html", {
        "document": document,
        "blocs": blocs,
        "resume": resume,
    })
