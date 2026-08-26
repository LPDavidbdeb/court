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

from case_manager.appui_depot_service import RE_COTE, arbre_des_appuis
from document_manager.models import Document
from document_manager.numerotation import numeroter


def texte_de(noeud):
    obj = noeud.content_object
    if obj is None:
        return None
    return (getattr(obj, "text", None) or getattr(obj, "quote_text", None)
            or getattr(obj, "titre", None) or str(obj))


def lier_cotes(t, noeuds):
    """
    Chaque cote du texte devient l'accès à la pièce qu'elle désigne.

    LA REGEX NE FAIT QUE LOCALISER. Ce vers quoi une cote pointe est tranché
    par `arbre_des_appuis`, jamais deviné ici : une cote absente de l'arbre est
    laissée telle quelle, en clair. Le texte reste donc lisible même quand la
    cotation et la prose divergent, et la divergence se voit.

    Deux formes, selon la profondeur de l'arbre. Une pièce se donne par un
    lien ; une liasse ne le peut pas — un lien qui prétend désigner une pièce
    alors qu'il en désigne vingt-quatre ment sur ce qu'il ouvre — et se déplie
    donc sur ses enfants, en place, sans quitter l'acte.

    Opère sur du texte DÉJÀ ÉCHAPPÉ ; tout ce qu'on y réinjecte l'est aussi.
    """
    if not noeuds:
        return t

    def piece(p):
        libelle = html.escape(p["libelle"])
        if not p["url"]:
            return f'<span class="piece">{html.escape(p["cote"])} — {libelle}</span>'
        return (f'<a class="piece" href="{html.escape(p["url"])}" target="_blank" '
                f'rel="noopener">{html.escape(p["cote"])} — {libelle}</a>')

    def remplacer(m):
        noeud = noeuds.get(m.group(0))
        if not noeud or not noeud["pieces"]:
            return m.group(0)
        cote = html.escape(noeud["cote"])
        if not noeud["via_liasse"] and len(noeud["pieces"]) == 1:
            p = noeud["pieces"][0]
            if not p["url"]:
                return cote
            return (f'<a class="cote" href="{html.escape(p["url"])}" target="_blank" '
                    f'rel="noopener" title="{html.escape(p["libelle"])}">{cote}</a>')
        enfants = "".join(f"<li>{piece(p)}</li>" for p in noeud["pieces"])
        return (f'<span class="cote liasse" tabindex="0">{cote}'
                f'<span class="nb">{len(noeud["pieces"])}</span>'
                f'<span class="pieces"><ul>{enfants}</ul></span></span>')

    return RE_COTE.sub(remplacer, t)


def enrichir(texte, noeuds=None):
    """
    Le texte vient d'une source markdown : **gras** et *italique* y subsistent.
    On échappe d'abord, on stylise ensuite — l'ordre inverse laisserait passer
    du HTML depuis le contenu. Les cotes se lient en dernier, sur du texte déjà
    sûr.
    """
    t = html.escape(texte or "")
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", t)
    t = lier_cotes(t, noeuds)
    return mark_safe(t)


def schema_detail_view(request, pk):
    document = get_object_or_404(Document.objects.select_related("schema"), pk=pk)

    # Une seule lecture pour toute la page : le rendu n'interroge plus rien.
    arbre = arbre_des_appuis(document.pk)

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
            "texte": enrichir(texte_de(noeud) or "",
                              arbre.get(noeud.object_id)),
        })

    resume = {
        "paragraphes": sum(1 for b in blocs if b["genre"] == "paragraphe"),
        "conclusions": sum(1 for b in blocs if b["genre"] == "conclusion"),
        "renumerotes": renumerotes,
        "pieces": sum(len(n["pieces"]) for c in arbre.values() for n in c.values()),
        "cotes": sum(len(c) for c in arbre.values()),
    }

    return render(request, "document_manager/schema_detail.html", {
        "document": document,
        "blocs": blocs,
        "resume": resume,
    })
