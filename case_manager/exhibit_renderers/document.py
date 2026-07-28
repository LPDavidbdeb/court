# case_manager/exhibit_renderers/document.py

"""
Rendu d'un `document_manager.Document` à partir du modèle.

La numérotation des paragraphes est calculée au rendu, exactement comme la
vue HTML « clean » (`document_manager.views.new_views`) : elle n'est stockée
nulle part et découle de la profondeur des nœuds dans l'arbre.

La fidélité des caractères et la pagination sont assurées par
`text_layout` — voir son en-tête.

⚠️ Portée. Ce rendu est une **représentation dérivée** du modèle, non le
document original. Pour un acte dont le contenu est lui-même contesté, la
pièce communiquée devrait être l'original (`Document.file_source`) ou une
copie qui en tient lieu. Voir `legal/METHODOLOGIE_POST_DEPOT.md` §9.2.
"""

from __future__ import annotations

from pathlib import Path

import fitz

from .base import BaseExhibitRenderer
from .common import (
    BODY_SIZE,
    FONT_BOLD,
    FONT_NORMAL,
    MARGIN_BOTTOM,
    MARGIN_LEFT,
    MARGIN_RIGHT,
    PAGE_WIDTH,
    SMALL_SIZE,
    SUBTITLE_SIZE,
    add_exhibit_cover,
    save_document,
)
from .text_layout import (
    PARAGRAPH_SPACING,
    Flow,
    clean,
    prepare,
)


# Largeur de la gouttière réservée au numéro de paragraphe.
GUTTER = 26

# Retrait horizontal par niveau de profondeur (depth 2 = corps du document).
INDENT_PER_DEPTH = 26

PROVENANCE_NOTE = (
    "Représentation générée à partir du modèle documentaire. "
    "La numérotation des paragraphes est calculée au rendu, "
    "selon la structure de l'arbre."
)


def _write_paragraph(
    flow: Flow,
    *,
    numbering: str,
    text: str,
    depth: int,
    fontsize: float = BODY_SIZE,
) -> None:
    """
    Écrit un paragraphe numéroté avec retrait négatif : le numéro occupe la
    gouttière, le texte est aligné dans la colonne.
    """
    text = clean(text)

    if not text.strip():
        return

    indent = max(depth - 2, 0) * INDENT_PER_DEPTH

    number_x = MARGIN_LEFT + indent
    text_x = number_x + GUTTER

    # Ne pas laisser un numéro orphelin en bas de page.
    flow.ensure(fontsize * 2.5)

    flow.label(numbering, x=number_x, fontsize=fontsize)

    flow.insert(
        text,
        x0=text_x,
        x1=PAGE_WIDTH - MARGIN_RIGHT,
        fontsize=fontsize,
    )

    flow.y += PARAGRAPH_SPACING


def _numbered_nodes(document):
    """
    Reproduit la sélection et la numérotation de la vue « clean » :
    `document_manager.views.new_views.new_clean_detail_view`.

    L'import est différé pour éviter tout cycle au chargement du registre.
    """
    from document_manager.views.new_views import (
        _format_nodes_for_new_display,
    )

    nodes = (
        document.nodes
        .filter(depth__gt=1, is_evidence=False)
        .prefetch_related("content_object")
        .order_by("path")
    )

    return _format_nodes_for_new_display(list(nodes))


class DocumentRenderer(BaseExhibitRenderer):

    def render(
        self,
        *,
        row,
        sources,
        destination: Path,
    ) -> Path:

        if len(sources) != 1:
            raise ValueError(
                "DocumentRenderer attend une seule source."
            )

        document = sources[0]

        doc = fitz.open()

        add_exhibit_cover(
            doc,
            cote=row.cote,
            description=row.description,
            date=row.date,
            source_type="document",
        )

        flow = Flow(doc)

        flow.insert(
            document.title or "",
            x0=MARGIN_LEFT,
            x1=PAGE_WIDTH - MARGIN_RIGHT,
            fontsize=SUBTITLE_SIZE,
            preferred=FONT_BOLD,
        )

        flow.y += PARAGRAPH_SPACING

        meta = []

        if document.author:
            meta.append(f"Auteur : {document.author}")

        if document.document_original_date:
            meta.append(
                "Date du document : "
                f"{document.document_original_date.isoformat()}"
            )

        if meta:
            flow.insert(
                "   —   ".join(meta),
                x0=MARGIN_LEFT,
                x1=PAGE_WIDTH - MARGIN_RIGHT,
                fontsize=SMALL_SIZE,
            )

        flow.y += PARAGRAPH_SPACING * 2

        for node in _numbered_nodes(document):
            _write_paragraph(
                flow,
                numbering=node.numbering,
                text=getattr(node.content_object, "text", "") or "",
                depth=node.depth,
            )

        if document.solemn_declaration:
            flow.y += PARAGRAPH_SPACING * 2

            flow.ensure(BODY_SIZE * 6)

            flow.insert(
                "DÉCLARATION SOUS SERMENT",
                x0=MARGIN_LEFT,
                x1=PAGE_WIDTH - MARGIN_RIGHT,
                fontsize=BODY_SIZE,
                preferred=FONT_BOLD,
            )

            flow.y += PARAGRAPH_SPACING

            _write_paragraph(
                flow,
                numbering="",
                text=document.solemn_declaration,
                depth=2,
            )

        # Mention de provenance, sur la page de garde : la placer en pied
        # d'une page de contenu l'intercalerait, à l'extraction, au milieu
        # d'un paragraphe à cheval sur deux pages.
        cover = doc[0]

        note, fontname, fontfile, _ = prepare(
            f"{PROVENANCE_NOTE} Document #{document.pk}.",
            FONT_NORMAL,
        )

        cover.insert_textbox(
            fitz.Rect(
                MARGIN_LEFT,
                cover.rect.height - 90,
                PAGE_WIDTH - MARGIN_RIGHT,
                cover.rect.height - 55,
            ),
            note,
            fontsize=SMALL_SIZE,
            fontname=fontname,
            fontfile=fontfile,
        )

        return save_document(doc, destination)
