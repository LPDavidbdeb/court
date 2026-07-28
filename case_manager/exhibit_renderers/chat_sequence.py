# case_manager/exhibit_renderers/chat_sequence.py

"""
Rendu d'un `googlechat_manager.ChatSequence` à partir de la base.

Contrairement aux actes d'une autre partie, ces conversations sont des
documents technologiques dont le demandeur est détenteur : la base **est** le
dépôt du document, et le PDF n'est qu'un changement de support. Ce qui est
exigé n'est donc pas une provenance tierce mais la **documentation de
l'intégrité** du transfert.

Le rendu la fournit de trois manières :

1. la totalité des messages de la séquence est reproduite, en ordre
   chronologique, sans troncature ni résumé;
2. chaque message porte son horodatage et son expéditeur (nom + adresse);
3. une annexe rappelle, pour chaque message, l'identifiant Google Chat
   (`message_id`) et l'horodatage original tel qu'exporté, de sorte que
   chaque ligne soit vérifiable contre l'export source.

⚠️ Périmètre. Une séquence est une **sélection** de messages. Lorsqu'elle ne
retient les propos que d'un seul participant, le rendu l'indique : une
conversation amputée de l'autre voix s'expose au reproche de
décontextualisation.
"""

from __future__ import annotations

from pathlib import Path

import fitz

from .base import BaseExhibitRenderer
from .common import (
    BODY_SIZE,
    FONT_BOLD,
    FONT_NORMAL,
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
    prepare,
)


# Largeur de la gouttière réservée au numéro de message.
GUTTER = 30

# Retrait du corps du message sous sa ligne d'en-tête.
MESSAGE_INDENT = 30

JOURS = (
    "lundi", "mardi", "mercredi", "jeudi",
    "vendredi", "samedi", "dimanche",
)

MOIS = (
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
)

PROVENANCE_NOTE = (
    "Transcription générée à partir de la base. Tous les messages de la "
    "séquence sont reproduits en ordre chronologique. L'annexe donne, pour "
    "chaque message, son identifiant d'origine."
)


def _date_longue(value) -> str:
    return (
        f"{JOURS[value.weekday()]} {value.day} "
        f"{MOIS[value.month - 1]} {value.year}"
    )


def _expediteur(message) -> tuple[str, str]:
    """
    Retourne (nom, adresse) en privilégiant le participant lié, et en
    retombant sur les données brutes de l'export.
    """
    sender = message.sender

    nom = getattr(sender, "name", None) or ""
    adresse = getattr(sender, "email", None) or ""

    creator = (message.raw_data or {}).get("creator") or {}

    return (
        nom or creator.get("name") or "Expéditeur inconnu",
        adresse or creator.get("email") or "",
    )


def _messages(sequence):
    return list(
        sequence.messages
        .select_related("sender", "thread")
        .order_by("timestamp", "pk")
    )


class ChatSequenceRenderer(BaseExhibitRenderer):

    def render(
        self,
        *,
        row,
        sources,
        destination: Path,
    ) -> Path:

        if len(sources) != 1:
            raise ValueError(
                "ChatSequenceRenderer attend une seule source."
            )

        sequence = sources[0]
        messages = _messages(sequence)

        doc = fitz.open()

        add_exhibit_cover(
            doc,
            cote=row.cote,
            description=row.description,
            date=row.date,
            source_type="chatsequence",
        )

        flow = Flow(doc)

        self._entete(flow, sequence, messages)
        self._transcription(flow, messages)
        self._annexe(flow, messages)

        self._provenance(doc, sequence, messages)

        return save_document(doc, destination)

    # -- Sections ----------------------------------------------------------

    def _entete(self, flow: Flow, sequence, messages) -> None:
        right = PAGE_WIDTH - MARGIN_RIGHT

        flow.insert(
            sequence.title or "",
            x0=MARGIN_LEFT,
            x1=right,
            fontsize=SUBTITLE_SIZE,
            preferred=FONT_BOLD,
        )

        flow.y += PARAGRAPH_SPACING

        if messages:
            debut = messages[0].timestamp
            fin = messages[-1].timestamp

            periode = (
                _date_longue(debut)
                if debut.date() == fin.date()
                else f"du {_date_longue(debut)} au {_date_longue(fin)}"
            )
        else:
            periode = "aucun message"

        participants = sorted(
            {_expediteur(m)[0] for m in messages}
        )

        lignes = [
            f"Période : {periode}",
            f"Nombre de messages : {len(messages)}",
            "Participants représentés : "
            + (", ".join(participants) or "—"),
        ]

        if len(participants) == 1 and len(messages) > 1:
            lignes.append(
                "Cette séquence ne retient les propos que d'un seul "
                "participant; elle est un extrait de la conversation et "
                "non son intégralité."
            )

        for ligne in lignes:
            flow.insert(
                ligne,
                x0=MARGIN_LEFT,
                x1=right,
                fontsize=SMALL_SIZE,
            )

        flow.rule(MARGIN_LEFT, right, gap=PARAGRAPH_SPACING)

    def _transcription(self, flow: Flow, messages) -> None:
        right = PAGE_WIDTH - MARGIN_RIGHT
        jour_courant = None

        for index, message in enumerate(messages, start=1):
            jour = message.timestamp.date()

            if jour != jour_courant:
                jour_courant = jour

                flow.y += PARAGRAPH_SPACING
                flow.ensure(BODY_SIZE * 5)

                flow.label(
                    _date_longue(message.timestamp).capitalize(),
                    x=MARGIN_LEFT,
                    fontsize=SMALL_SIZE,
                )

                flow.y += SMALL_SIZE + 2
                flow.rule(MARGIN_LEFT, right, gap=2)

            nom, adresse = _expediteur(message)

            entete = (
                f"{message.timestamp.strftime('%H:%M')}  {nom}"
                + (f"  <{adresse}>" if adresse else "")
            )

            # En-tête et première ligne du message restent solidaires.
            flow.ensure(BODY_SIZE * 4)

            flow.label(
                f"{index}.",
                x=MARGIN_LEFT,
                fontsize=SMALL_SIZE,
            )

            flow.label(
                entete,
                x=MARGIN_LEFT + GUTTER,
                fontsize=SMALL_SIZE,
            )

            flow.y += SMALL_SIZE + 3

            flow.insert(
                message.text_content or "",
                x0=MARGIN_LEFT + MESSAGE_INDENT,
                x1=right,
                fontsize=BODY_SIZE,
            )

            flow.y += PARAGRAPH_SPACING

    def _annexe(self, flow: Flow, messages) -> None:
        right = PAGE_WIDTH - MARGIN_RIGHT

        flow.new_page()

        flow.insert(
            "ANNEXE — IDENTIFIANTS D'ORIGINE DES MESSAGES",
            x0=MARGIN_LEFT,
            x1=right,
            fontsize=BODY_SIZE,
            preferred=FONT_BOLD,
        )

        flow.y += PARAGRAPH_SPACING

        flow.insert(
            "Chaque ligne renvoie au numéro de message de la transcription "
            "et reproduit l'horodatage ainsi que l'identifiant attribués "
            "par le service à l'origine, tels qu'ils figurent dans "
            "l'export.",
            x0=MARGIN_LEFT,
            x1=right,
            fontsize=SMALL_SIZE,
        )

        flow.rule(MARGIN_LEFT, right, gap=PARAGRAPH_SPACING)

        for index, message in enumerate(messages, start=1):
            raw = message.raw_data or {}

            horodatage = (
                raw.get("created_date")
                or message.timestamp.isoformat()
            )

            identifiant = raw.get("message_id") or "—"

            flow.ensure(BODY_SIZE * 3)

            flow.label(
                f"{index}.",
                x=MARGIN_LEFT,
                fontsize=6,
                preferred=FONT_NORMAL,
            )

            flow.insert(
                f"{horodatage}   ·   {identifiant}",
                x0=MARGIN_LEFT + GUTTER,
                x1=right,
                fontsize=6,
            )

            flow.y += 2

        self._note_substitutions(flow)

    def _note_substitutions(self, flow: Flow) -> None:
        """
        Documente les caractères qu'aucune police disponible ne rend et qui
        ont été remplacés par un marqueur dans la transcription.
        """
        if not flow.substitutions:
            return

        right = PAGE_WIDTH - MARGIN_RIGHT

        flow.y += PARAGRAPH_SPACING
        flow.ensure(BODY_SIZE * 6)

        flow.insert(
            "Caractères substitués",
            x0=MARGIN_LEFT,
            x1=right,
            fontsize=SMALL_SIZE,
            preferred=FONT_BOLD,
        )

        flow.y += 2

        details = ", ".join(
            f"U+{ord(c):04X}" for c in sorted(flow.substitutions)
        )

        flow.insert(
            "Les caractères suivants, présents dans les messages d'origine, "
            "ne sont rendus par aucune police disponible et apparaissent "
            "dans la transcription sous la forme du marqueur [U+XXXX], "
            "leur point de code Unicode : "
            f"{details}. Aucun autre caractère n'a été modifié.",
            x0=MARGIN_LEFT,
            x1=right,
            fontsize=SMALL_SIZE,
        )

    def _provenance(self, doc, sequence, messages) -> None:
        cover = doc[0]

        note = (
            f"{PROVENANCE_NOTE} "
            f"ChatSequence #{sequence.pk} — {len(messages)} messages."
        )

        note, fontname, fontfile, _ = prepare(note, FONT_NORMAL)

        cover.insert_textbox(
            fitz.Rect(
                MARGIN_LEFT,
                cover.rect.height - 100,
                PAGE_WIDTH - MARGIN_RIGHT,
                cover.rect.height - 55,
            ),
            note,
            fontsize=SMALL_SIZE,
            fontname=fontname,
            fontfile=fontfile,
        )
