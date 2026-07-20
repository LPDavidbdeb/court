# case_manager/management/commands/sync_pieces.py

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from document_manager.models import Document
from email_manager.models import Email, EmailThread
from events.models import Event
from googlechat_manager.models import ChatSequence
from pdf_manager.models import PDFDocument
from photos.models import Photo, PhotoDocument


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BORDEREAU_PATH = Path(settings.BASE_DIR) / "legal" / "bordereau_pieces.md"

# Dossier entièrement reconstruit à chaque synchronisation.
OUTPUT_DIR = Path(settings.BASE_DIR) / "pieces"

# Dossier permanent, JAMAIS supprimé par la commande.
#
# Exemple :
# manual_pieces/
#   chatsequence-9/
#       capture_01.png
#       capture_02.png
#
#   document-1/
#       requete_originale.pdf
MANUAL_DIR = Path(settings.BASE_DIR) / "manual_pieces"

STAGING_DIR = Path(settings.BASE_DIR) / ".pieces_build"
BACKUP_DIR = Path(settings.BASE_DIR) / ".pieces_backup"


# Quelques entrées du bordereau actuel ne contiennent pas encore
# un model+pk exploitable automatiquement.
#
# Ajouter ici leur identité stable lorsqu'elle sera connue.
#
# Exemple :
#
# SOURCE_OVERRIDES = {
#     "P-8": SourceRef("photo", ("1234",)),
#     "P-14": SourceRef("thread", ("42",)),
#     "P-101": SourceRef("photo", ("5678",)),
#     "P-105": SourceRef("email", ("999",)),
# }
SOURCE_OVERRIDES = {}


# ---------------------------------------------------------------------------
# Structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class BordereauRow:
    cote: str
    date: str
    description: str
    fichier_appui: str
    source_base: str


@dataclass(frozen=True)
class SourceRef:
    """
    Référence stable vers la couche primaire.

    kind :
        pdf
        email
        thread
        photo
        photodoc
        event
        document
        chatsequence
        path
    """
    kind: str
    ids: tuple[str, ...]


# ---------------------------------------------------------------------------
# Lecture du bordereau Markdown
# ---------------------------------------------------------------------------

def parse_bordereau(path: Path) -> list[BordereauRow]:
    if not path.exists():
        raise CommandError(f"Bordereau introuvable : {path}")

    rows: list[BordereauRow] = []

    for line in path.read_text(encoding="utf-8").splitlines():
        if not re.match(r"^\|\s*P-\d+\s*\|", line):
            continue

        columns = [
            value.strip()
            for value in line.strip().strip("|").split("|")
        ]

        if len(columns) < 5:
            continue

        rows.append(
            BordereauRow(
                cote=columns[0],
                date=columns[1],
                description=columns[2],
                fichier_appui=columns[3],
                source_base=columns[4],
            )
        )

    if not rows:
        raise CommandError("Aucune cote P-n trouvée dans le bordereau.")

    return rows


# ---------------------------------------------------------------------------
# Parsing des références model+pk
# ---------------------------------------------------------------------------

def parse_id_list(raw: str) -> tuple[str, ...]:
    """
    Transforme :
        "1, 2, 3"
        "1/2/3"
    en :
        ("1", "2", "3")
    """
    return tuple(re.findall(r"\d+", raw))


def expand_range(start: str, end: str) -> tuple[str, ...]:
    return tuple(str(i) for i in range(int(start), int(end) + 1))


def resolve_source(row: BordereauRow) -> SourceRef | None:
    if row.cote in SOURCE_OVERRIDES:
        return SOURCE_OVERRIDES[row.cote]

    # Normaliser les tirets typographiques.
    text = f"{row.fichier_appui} | {row.source_base}"
    text = text.replace("–", "-").replace("—", "-")

    # ------------------------------------------------------------------
    # 1. Déclarations explicites du bordereau
    # ------------------------------------------------------------------

    explicit_patterns = [
        ("pdf", r"PDFDocuments?\s+id\s*=\s*([0-9,\s]+)"),
        ("email", r"Emails?\s+id\s*=\s*([0-9,\s]+)"),
        ("event", r"Events?\s+id\s*=\s*([0-9,\s]+)"),
        ("photodoc", r"PhotoDocuments?\s+id\s*=\s*([0-9,\s]+)"),
        ("chatsequence", r"ChatSequence\s+id\s*=\s*(\d+)"),
    ]

    for kind, pattern in explicit_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return SourceRef(kind, parse_id_list(match.group(1)))

    # ------------------------------------------------------------------
    # 2. Listes/ranges : emails-1/2/3, events-1-10, pdfs-45-58...
    # ------------------------------------------------------------------

    for kind, prefix in [
        ("pdf", "pdf"),
        ("email", "email"),
        ("event", "event"),
        ("photodoc", "photodoc"),
    ]:
        # Range, ex. pdfs-45-58
        match = re.search(
            rf"\b{prefix}s?-(\d+)-(\d+)\b",
            text,
            re.IGNORECASE,
        )
        if match:
            return SourceRef(
                kind,
                expand_range(match.group(1), match.group(2)),
            )

        # Liste, ex. emails-136/137
        match = re.search(
            rf"\b{prefix}s?[-\s]+(\d+(?:/\d+)+)",
            text,
            re.IGNORECASE,
        )
        if match:
            return SourceRef(kind, parse_id_list(match.group(1)))

    # ------------------------------------------------------------------
    # 3. Références simples
    # ------------------------------------------------------------------

    # Email avant Thread :
    # piece_thread-89_email-365 doit résoudre vers email-365.
    match = re.search(r"\bemail-(\d+)", text, re.IGNORECASE)
    if match:
        return SourceRef("email", (match.group(1),))

    match = re.search(r"\bpdf-(\d+)", text, re.IGNORECASE)
    if match:
        return SourceRef("pdf", (match.group(1),))

    match = re.search(r"\bphotodoc-(\d+)", text, re.IGNORECASE)
    if match:
        return SourceRef("photodoc", (match.group(1),))

    match = re.search(r"(?:piece_)?photo-(\d+)", text, re.IGNORECASE)
    if match:
        return SourceRef("photo", (match.group(1),))

    match = re.search(r"\bevent-(\d+)", text, re.IGNORECASE)
    if match:
        return SourceRef("event", (match.group(1),))

    match = re.search(r"\bchatsequence-(\d+)", text, re.IGNORECASE)
    if match:
        return SourceRef("chatsequence", (match.group(1),))

    match = re.search(r"\bdocument-(\d+)", text, re.IGNORECASE)
    if match:
        return SourceRef("document", (match.group(1),))

    # Thread par PK numérique.
    match = re.search(r"\bthread-(\d+)", text, re.IGNORECASE)
    if match:
        return SourceRef("thread", (match.group(1),))

    # Thread par thread_id Google/Gmail.
    match = re.search(
        r"\bthread\s+([a-f0-9]{10,})",
        text,
        re.IGNORECASE,
    )
    if match:
        return SourceRef("thread", (match.group(1),))

    # Fichier local explicite, par exemple Downloads/document-2.pdf
    match = re.search(
        r"(Downloads/[^\s|]+\.[A-Za-z0-9]+)",
        text,
    )
    if match:
        return SourceRef("path", (match.group(1),))

    return None


# ---------------------------------------------------------------------------
# Utilitaires de copie
# ---------------------------------------------------------------------------

def copy_field_file(field_file, destination: Path) -> Path:
    if not field_file or not getattr(field_file, "name", None):
        raise FileNotFoundError("FileField vide.")

    suffix = Path(field_file.name).suffix
    final_path = destination.with_suffix(suffix)

    final_path.parent.mkdir(parents=True, exist_ok=True)

    with field_file.open("rb") as source:
        with final_path.open("wb") as target:
            shutil.copyfileobj(source, target)

    return final_path


def copy_local_file(source: Path, destination: Path) -> Path:
    if not source.exists():
        raise FileNotFoundError(source)

    final_path = destination.with_suffix(source.suffix)
    final_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(source, final_path)
    return final_path


def preview_field_file(field_file, destination: Path) -> Path:
    if not field_file or not getattr(field_file, "name", None):
        raise FileNotFoundError("FileField vide.")

    suffix = Path(field_file.name).suffix
    return destination.with_suffix(suffix)


def preview_local_file(source: Path, destination: Path) -> Path:
    if not source.exists():
        raise FileNotFoundError(source)

    return destination.with_suffix(source.suffix)


def preview_manual_representation(
    source_key: str,
    label: str,
    output_root: Path,
) -> list[Path]:
    manual_source = MANUAL_DIR / source_key

    if not manual_source.exists():
        return []

    files = sorted(path for path in manual_source.iterdir() if path.is_file())

    if not files:
        return []

    if len(files) == 1:
        source = files[0]
        return [output_root / f"{label}{source.suffix}"]

    piece_dir = output_root / label
    return [
        piece_dir / f"{index:02d}{source.suffix}"
        for index, source in enumerate(files, start=1)
    ]


def preview_email(email_obj: Email, label: str, root: Path) -> list[Path]:
    destination = root / label

    if email_obj.eml_file and email_obj.eml_file.name:
        return [preview_field_file(email_obj.eml_file, destination)]

    if email_obj.eml_file_path:
        path = Path(email_obj.eml_file_path)
        if path.exists():
            return [preview_local_file(path, destination)]

    raise FileNotFoundError(
        f"Email(pk={email_obj.pk}) ne possède aucun fichier EML accessible."
    )


def preview_photo(photo: Photo, label: str, root: Path) -> list[Path]:
    if not photo.file or not photo.file.name:
        raise FileNotFoundError(
            f"Photo(pk={photo.pk}) ne possède aucun fichier."
        )

    return [preview_field_file(photo.file, root / label)]


def preview_pdf(pdf: PDFDocument, label: str, root: Path) -> list[Path]:
    return [preview_field_file(pdf.file, root / label)]


def preview_event(event: Event, label: str, root: Path) -> list[Path]:
    outputs = []

    photos = list(event.linked_photos.all().order_by("pk"))

    if len(photos) == 1 and not event.linked_email:
        return preview_photo(photos[0], label, root)

    if photos or event.linked_email:
        group_dir = root / label

        for index, photo in enumerate(photos, start=1):
            if not photo.file or not photo.file.name:
                raise FileNotFoundError(
                    f"Photo(pk={photo.pk}) liée à Event(pk={event.pk}) ne possède aucun fichier."
                )

            suffix = Path(photo.file.name).suffix
            outputs.append(group_dir / f"{index:02d}{suffix}")

        if event.linked_email:
            outputs.extend(
                preview_email(
                    event.linked_email,
                    "email",
                    group_dir,
                )
            )

    if not outputs:
        raise FileNotFoundError(
            f"Event(pk={event.pk}) ne référence aucune photo ni aucun email."
        )

    return outputs


def preview_photodoc(
    photodoc: PhotoDocument,
    label: str,
    root: Path,
) -> list[Path]:
    photos = list(photodoc.photos.all().order_by("pk"))

    if not photos:
        raise FileNotFoundError(
            f"PhotoDocument(pk={photodoc.pk}) est vide."
        )

    if len(photos) == 1:
        return preview_photo(photos[0], label, root)

    group_dir = root / label

    outputs = []

    for index, photo in enumerate(photos, start=1):
        if not photo.file or not photo.file.name:
            raise FileNotFoundError(
                f"Photo(pk={photo.pk}) liée à PhotoDocument(pk={photodoc.pk}) ne possède aucun fichier."
            )

        suffix = Path(photo.file.name).suffix
        outputs.append(group_dir / f"{index:02d}{suffix}")

    return outputs


def preview_thread(
    thread: EmailThread,
    label: str,
    root: Path,
) -> list[Path]:
    emails = list(thread.emails.all().order_by("date_sent", "pk"))

    if not emails:
        raise FileNotFoundError(
            f"EmailThread(pk={thread.pk}) ne contient aucun email."
        )

    if len(emails) == 1:
        return preview_email(emails[0], label, root)

    group_dir = root / label
    outputs = []

    for index, email_obj in enumerate(emails, start=1):
        outputs.extend(
            preview_email(
                email_obj,
                f"{index:02d}",
                group_dir,
            )
        )

    return outputs


def copy_manual_representation(
    source_key: str,
    label: str,
    output_root: Path,
) -> list[Path]:
    """
    Copie une représentation manuelle stable.

    Exemple source :
        manual_pieces/chatsequence-9/capture1.png
        manual_pieces/chatsequence-9/capture2.png

    Sortie :
        pieces/P-58/01.png
        pieces/P-58/02.png
    """
    manual_source = MANUAL_DIR / source_key

    if not manual_source.exists():
        return []

    files = sorted(
        path
        for path in manual_source.iterdir()
        if path.is_file()
    )

    if not files:
        return []

    # Un seul fichier : P-19.pdf
    if len(files) == 1:
        source = files[0]
        destination = output_root / f"{label}{source.suffix}"
        shutil.copy2(source, destination)
        return [destination]

    # Plusieurs fichiers : P-58/01.png, P-58/02.png...
    piece_dir = output_root / label
    piece_dir.mkdir(parents=True, exist_ok=True)

    outputs = []

    for index, source in enumerate(files, start=1):
        destination = piece_dir / f"{index:02d}{source.suffix}"
        shutil.copy2(source, destination)
        outputs.append(destination)

    return outputs


def create_placeholder(
    label: str,
    source_key: str,
    description: str,
    output_root: Path,
) -> Path:
    path = output_root / f"{label}__PLACEHOLDER.txt"

    path.write_text(
        "\n".join(
            [
                f"Cote : {label}",
                f"Source stable : {source_key}",
                f"Description : {description}",
                "",
                "Aucune représentation physique n'est actuellement associée.",
                "Déposer la représentation manuelle dans :",
                f"manual_pieces/{source_key}/",
            ]
        ),
        encoding="utf-8",
    )

    return path


# ---------------------------------------------------------------------------
# Export des objets fondamentaux
# ---------------------------------------------------------------------------

def export_email(email_obj: Email, label: str, root: Path) -> list[Path]:
    destination = root / label

    if email_obj.eml_file and email_obj.eml_file.name:
        return [copy_field_file(email_obj.eml_file, destination)]

    if email_obj.eml_file_path:
        path = Path(email_obj.eml_file_path)
        if path.exists():
            return [copy_local_file(path, destination)]

    raise FileNotFoundError(
        f"Email(pk={email_obj.pk}) ne possède aucun fichier EML accessible."
    )


def export_photo(photo: Photo, label: str, root: Path) -> list[Path]:
    if not photo.file or not photo.file.name:
        raise FileNotFoundError(
            f"Photo(pk={photo.pk}) ne possède aucun fichier."
        )

    return [copy_field_file(photo.file, root / label)]


def export_pdf(pdf: PDFDocument, label: str, root: Path) -> list[Path]:
    return [copy_field_file(pdf.file, root / label)]


def export_event(event: Event, label: str, root: Path) -> list[Path]:
    """
    Event est une association.

    On descend vers :
      - linked_photos
      - linked_email
    """
    outputs = []

    photos = list(event.linked_photos.all().order_by("pk"))

    if len(photos) == 1 and not event.linked_email:
        return export_photo(photos[0], label, root)

    if photos or event.linked_email:
        group_dir = root / label
        group_dir.mkdir(parents=True, exist_ok=True)

        for index, photo in enumerate(photos, start=1):
            if photo.file and photo.file.name:
                suffix = Path(photo.file.name).suffix
                destination = group_dir / f"{index:02d}{suffix}"

                with photo.file.open("rb") as source:
                    with destination.open("wb") as target:
                        shutil.copyfileobj(source, target)

                outputs.append(destination)

        if event.linked_email:
            email_outputs = export_email(
                event.linked_email,
                "email",
                group_dir,
            )
            outputs.extend(email_outputs)

    if not outputs:
        raise FileNotFoundError(
            f"Event(pk={event.pk}) ne référence aucune photo ni aucun email."
        )

    return outputs


def export_photodoc(
    photodoc: PhotoDocument,
    label: str,
    root: Path,
) -> list[Path]:
    """
    PhotoDocument est une association de Photo.
    """
    photos = list(photodoc.photos.all().order_by("pk"))

    if not photos:
        raise FileNotFoundError(
            f"PhotoDocument(pk={photodoc.pk}) est vide."
        )

    if len(photos) == 1:
        return export_photo(photos[0], label, root)

    group_dir = root / label
    group_dir.mkdir(parents=True, exist_ok=True)

    outputs = []

    for index, photo in enumerate(photos, start=1):
        suffix = Path(photo.file.name).suffix
        destination = group_dir / f"{index:02d}{suffix}"

        with photo.file.open("rb") as source:
            with destination.open("wb") as target:
                shutil.copyfileobj(source, target)

        outputs.append(destination)

    return outputs


def export_thread(
    thread: EmailThread,
    label: str,
    root: Path,
) -> list[Path]:
    """
    EmailThread est une association d'Email.
    """
    emails = list(
        thread.emails.all().order_by("date_sent", "pk")
    )

    if not emails:
        raise FileNotFoundError(
            f"EmailThread(pk={thread.pk}) ne contient aucun email."
        )

    if len(emails) == 1:
        return export_email(emails[0], label, root)

    group_dir = root / label
    group_dir.mkdir(parents=True, exist_ok=True)

    outputs = []

    for index, email_obj in enumerate(emails, start=1):
        outputs.extend(
            export_email(
                email_obj,
                f"{index:02d}",
                group_dir,
            )
        )

    return outputs


# ---------------------------------------------------------------------------
# Export d'une référence
# ---------------------------------------------------------------------------

def export_source(
    row: BordereauRow,
    ref: SourceRef,
    output_root: Path,
) -> list[Path]:

    # Document et ChatSequence :
    # 1. représentation manuelle
    # 2. sinon placeholder
    if ref.kind in {"document", "chatsequence"}:
        if len(ref.ids) != 1:
            raise ValueError(
                f"{ref.kind} avec plusieurs IDs non supporté : {ref.ids}"
            )

        source_key = f"{ref.kind}-{ref.ids[0]}"

        manual = copy_manual_representation(
            source_key,
            row.cote,
            output_root,
        )

        if manual:
            return manual

        return [
            create_placeholder(
                row.cote,
                source_key,
                row.description,
                output_root,
            )
        ]

    # Un ensemble explicitement énuméré dans le bordereau devient
    # P-x.1, P-x.2, etc.
    multiple = len(ref.ids) > 1

    outputs = []

    for index, raw_id in enumerate(ref.ids, start=1):
        label = (
            f"{row.cote}.{index}"
            if multiple
            else row.cote
        )

        pk = int(raw_id) if raw_id.isdigit() else raw_id

        if ref.kind == "pdf":
            obj = PDFDocument.objects.get(pk=pk)
            outputs.extend(export_pdf(obj, label, output_root))

        elif ref.kind == "email":
            obj = Email.objects.get(pk=pk)
            outputs.extend(export_email(obj, label, output_root))

        elif ref.kind == "photo":
            obj = Photo.objects.get(pk=pk)
            outputs.extend(export_photo(obj, label, output_root))

        elif ref.kind == "event":
            obj = Event.objects.get(pk=pk)
            outputs.extend(export_event(obj, label, output_root))

        elif ref.kind == "photodoc":
            obj = PhotoDocument.objects.get(pk=pk)
            outputs.extend(export_photodoc(obj, label, output_root))

        elif ref.kind == "thread":
            if str(raw_id).isdigit():
                obj = EmailThread.objects.get(pk=int(raw_id))
            else:
                obj = EmailThread.objects.get(thread_id=raw_id)

            outputs.extend(export_thread(obj, label, output_root))

        elif ref.kind == "path":
            source = Path(settings.BASE_DIR) / raw_id
            outputs.append(
                copy_local_file(
                    source,
                    output_root / label,
                )
            )

        else:
            raise ValueError(f"Type de source inconnu : {ref.kind}")

    return outputs


def preview_source(
    row: BordereauRow,
    ref: SourceRef,
    output_root: Path,
) -> list[Path]:

    if ref.kind in {"document", "chatsequence"}:
        if len(ref.ids) != 1:
            raise ValueError(
                f"{ref.kind} avec plusieurs IDs non supporté : {ref.ids}"
            )

        if ref.kind == "document":
            Document.objects.get(pk=int(ref.ids[0]))
        else:
            ChatSequence.objects.get(pk=int(ref.ids[0]))

        source_key = f"{ref.kind}-{ref.ids[0]}"

        manual = preview_manual_representation(
            source_key,
            row.cote,
            output_root,
        )

        if manual:
            return manual

        return [output_root / f"{row.cote}__PLACEHOLDER.txt"]

    multiple = len(ref.ids) > 1
    outputs = []

    for index, raw_id in enumerate(ref.ids, start=1):
        label = f"{row.cote}.{index}" if multiple else row.cote
        pk = int(raw_id) if raw_id.isdigit() else raw_id

        if ref.kind == "pdf":
            obj = PDFDocument.objects.get(pk=pk)
            outputs.extend(preview_pdf(obj, label, output_root))

        elif ref.kind == "email":
            obj = Email.objects.get(pk=pk)
            outputs.extend(preview_email(obj, label, output_root))

        elif ref.kind == "photo":
            obj = Photo.objects.get(pk=pk)
            outputs.extend(preview_photo(obj, label, output_root))

        elif ref.kind == "event":
            obj = Event.objects.get(pk=pk)
            outputs.extend(preview_event(obj, label, output_root))

        elif ref.kind == "photodoc":
            obj = PhotoDocument.objects.get(pk=pk)
            outputs.extend(preview_photodoc(obj, label, output_root))

        elif ref.kind == "thread":
            if str(raw_id).isdigit():
                obj = EmailThread.objects.get(pk=int(raw_id))
            else:
                obj = EmailThread.objects.get(thread_id=raw_id)

            outputs.extend(preview_thread(obj, label, output_root))

        elif ref.kind == "path":
            source = Path(settings.BASE_DIR) / raw_id
            outputs.append(preview_local_file(source, output_root / label))

        else:
            raise ValueError(f"Type de source inconnu : {ref.kind}")

    return outputs


# ---------------------------------------------------------------------------
# Commande Django
# ---------------------------------------------------------------------------

class Command(BaseCommand):
    help = (
        "Synchronise le dossier pieces/ à partir de "
        "legal/bordereau_pieces.md."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--allow-unresolved",
            action="store_true",
            help=(
                "Crée un placeholder pour les lignes du bordereau "
                "dont la source model+pk ne peut pas être résolue."
            ),
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simule la synchronisation sans écrire sur le disque.",
        )

    def _run_resolution(
        self,
        rows,
        output_root: Path,
        allow_unresolved: bool,
        dry_run: bool = False,
    ):
        manifest = {}
        unresolved = []

        for row in rows:
            ref = resolve_source(row)

            if ref is None:
                unresolved.append(row.cote)

                if not allow_unresolved:
                    continue

                if dry_run:
                    output = output_root / f"{row.cote}__PLACEHOLDER.txt"
                else:
                    output = create_placeholder(
                        row.cote,
                        "SOURCE-NON-RESOLUE",
                        row.description,
                        output_root,
                    )

                manifest[row.cote] = {
                    "status": "unresolved",
                    "description": row.description,
                    "files": [str(output.relative_to(output_root))],
                }

                continue

            self.stdout.write(f"{row.cote:<6} -> {ref.kind}:{','.join(ref.ids)}")

            outputs = preview_source(row, ref, output_root)

            manifest[row.cote] = {
                "status": "ok",
                "source_type": ref.kind,
                "source_ids": list(ref.ids),
                "description": row.description,
                "files": [str(path.relative_to(output_root)) for path in outputs],
            }

        return manifest, unresolved

    def handle(self, *args, **options):
        allow_unresolved = options["allow_unresolved"]
        dry_run = options["dry_run"]

        rows = parse_bordereau(BORDEREAU_PATH)

        self.stdout.write(
            f"{len(rows)} cotes trouvées dans le bordereau."
        )

        if dry_run:
            manifest, unresolved = self._run_resolution(
                rows,
                STAGING_DIR,
                allow_unresolved,
                dry_run=True,
            )

            if unresolved and not allow_unresolved:
                raise CommandError(
                    "Sources non résolues : " + ", ".join(unresolved)
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Dry-run terminé : {len(manifest)} cotes analysées, aucun fichier n'a été écrit."
                )
            )
            return

        # Reconstruction complète dans un dossier temporaire.
        if STAGING_DIR.exists():
            shutil.rmtree(STAGING_DIR)

        STAGING_DIR.mkdir(parents=True)

        try:
            manifest, unresolved = self._run_resolution(
                rows,
                STAGING_DIR,
                allow_unresolved,
            )

            # En mode strict, aucune modification de pieces/
            # si une source n'est pas résolue.
            if unresolved and not allow_unresolved:
                raise CommandError(
                    "Sources non résolues : "
                    + ", ".join(unresolved)
                    + "\n"
                    "Compléter SOURCE_OVERRIDES ou utiliser "
                    "--allow-unresolved."
                )

            # Manifest
            manifest_path = STAGING_DIR / "manifest.json"

            manifest_path.write_text(
                json.dumps(
                    manifest,
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            # Swap atomique approximatif :
            # ancien pieces/ -> backup
            # staging -> pieces/
            if BACKUP_DIR.exists():
                shutil.rmtree(BACKUP_DIR)

            if OUTPUT_DIR.exists():
                OUTPUT_DIR.rename(BACKUP_DIR)

            try:
                STAGING_DIR.rename(OUTPUT_DIR)
            except Exception:
                # Restaurer l'ancien dossier en cas d'échec.
                if BACKUP_DIR.exists() and not OUTPUT_DIR.exists():
                    BACKUP_DIR.rename(OUTPUT_DIR)
                raise

            if BACKUP_DIR.exists():
                shutil.rmtree(BACKUP_DIR)

        except Exception:
            if STAGING_DIR.exists():
                shutil.rmtree(STAGING_DIR)
            raise

        self.stdout.write(
            self.style.SUCCESS(
                f"Synchronisation terminée : {OUTPUT_DIR}"
            )
        )