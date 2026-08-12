"""
Rendu d'un document selon son schéma de niveaux, mis en page comme un acte.

Les autres vues affichent l'arbre tel qu'il est stocké. Celle-ci l'affiche tel
que le SCHÉMA le lit — chaque profondeur reçoit le rôle, le format de numéro et
la portée que le schéma lui attribue — et le présente comme il le serait devant
le tribunal.

La correspondance entre le numéro du dépôt et le numéro recalculé est CONSERVÉE
(elle vit dans `LibraryNode.item`) mais n'est pas affichée : elle est portée en
attribut `title` sur le numéro, donc lisible au survol sans encombrer la page.
"""
import html
import re

from django.shortcuts import get_object_or_404, render
from django.utils.safestring import mark_safe

from document_manager.models import (
    Document, FormatNumero, LibraryNode, PorteeNumero, RoleNiveau,
)

ROMAINS = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"),
           (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"),
           (5, "V"), (4, "IV"), (1, "I")]

# Convention provisoire, posée par l'importateur : une conclusion porte « C-n »,
# une mention de clôture porte un item vide, un paragraphe porte le numéro qu'il
# avait au dépôt. Le schéma ne sait pas encore qu'une même profondeur peut porter
# des rôles différents selon son ascendance — un paragraphe sous un thème, une
# conclusion sous un chapeau. Tant qu'il ne le sait pas, la mise en page s'appuie
# sur cette convention plutôt que de numéroter « ACCUEILLIR la présente demande »
# comme s'il s'agissait d'une allégation.
RE_CONCLUSION = re.compile(r"^C-\d+$")


def en_romain(n):
    out = ""
    for valeur, signe in ROMAINS:
        while n >= valeur:
            out += signe
            n -= valeur
    return out


def formater(n, format_numero):
    if format_numero == FormatNumero.DECIMAL:
        return str(n)
    if format_numero == FormatNumero.ROMAIN_MAJ:
        return en_romain(n)
    if format_numero == FormatNumero.LETTRE_MAJ:
        return chr(ord("A") + (n - 1) % 26)
    if format_numero == FormatNumero.LETTRE_MIN:
        return f"{chr(ord('a') + (n - 1) % 26)})"
    return ""


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
    noeuds = list(
        document.nodes.select_related("content_type")
        .prefetch_related("content_object").order_by("path")
    )

    niveaux = {}
    if document.schema:
        niveaux = {n.profondeur: n for n in document.schema.niveaux.all()}

    compteurs_document = {}
    compteurs_parent = {}
    blocs = []
    renumerotes = 0

    for noeud in noeuds:
        if noeud.depth == 1 or noeud.content_type_id is None:
            continue                      # racine et nœuds transparents : structure seule

        niveau = niveaux.get(noeud.depth)
        texte = texte_de(noeud) or ""
        item = noeud.item or ""
        role = niveau.role if niveau else None

        # Nature réelle du bloc, au-delà de ce que la profondeur seule dit.
        if role == RoleNiveau.PARAGRAPHE and RE_CONCLUSION.match(item):
            genre = "conclusion"
        elif role == RoleNiveau.PARAGRAPHE and not item:
            genre = "mention"
        elif role == RoleNiveau.PARAGRAPHE:
            genre = "paragraphe"
        elif role in (RoleNiveau.SECTION, RoleNiveau.SOUS_SECTION,
                      RoleNiveau.THEME, RoleNiveau.SOUS_THEME, RoleNiveau.CHAPEAU):
            genre = "titre"
        else:
            genre = "libre"

        numero = ""
        if niveau and niveau.format_numero != FormatNumero.AUCUN \
                and genre in ("paragraphe", "titre"):
            if niveau.portee == PorteeNumero.PARENT:
                cle = (noeud.depth, noeud.path[:-LibraryNode.steplen])
                compteurs_parent[cle] = compteurs_parent.get(cle, 0) + 1
                rang = compteurs_parent[cle]
            else:
                compteurs_document[noeud.depth] = \
                    compteurs_document.get(noeud.depth, 0) + 1
                rang = compteurs_document[noeud.depth]
            numero = formater(rang, niveau.format_numero)

        if numero and item and numero != item:
            renumerotes += 1

        blocs.append({
            "genre": genre,
            "profondeur": noeud.depth,
            "numero": numero,
            # conservée, non affichée : lisible au survol du numéro
            "origine": item,
            "change": bool(numero and item and numero != item),
            "texte": enrichir(texte),
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
