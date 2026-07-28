"""Audit read-only de la chaîne des pièces judiciaires.

Cette couche complète :mod:`case_manager.evidence_audit`. Elle prend les
fiches ``legal/piece*.md`` et le bordereau comme deux vues d'une même chaîne :

    bordereau -> fiche Markdown -> (model, pk) -> objet Django -> original
               -> renderer -> PDF normalisé -> cahier

Le module ne modifie ni la base, ni les fiches, ni les fichiers assemblés.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import fitz

from django.db.models import Model

from case_manager.evidence_audit import (
    MODEL_CLASSES,
    ReferenceOccurrence,
    _object_date,
    _object_title,
    audit_occurrences,
    extract_references_from_text,
    object_original_status,
    resolve_descriptive_piece_occurrences,
)
from case_manager.exhibit_renderers.registry import RENDERERS
from case_manager.management.commands.sync_pieces import (
    BordereauRow,
    SourceRef,
    parse_bordereau,
    resolve_source,
)
from case_manager.management.commands.sync_pieces_pdf import resolve_objects
from document_manager.models import Document, DocumentSource
from email_manager.models import Email, EmailThread
from events.models import Event
from googlechat_manager.models import ChatMessage, ChatSequence
from pdf_manager.models import PDFDocument
from photos.models import Photo, PhotoDocument


PIECE_TOKEN_PATTERN = re.compile(
    r"(?<![\w])(?P<name>piece_[\wÀ-ÿ….-]+)",
    re.IGNORECASE,
)
SEVERITY_ORDER = {"info": 0, "warning": 1, "error": 2}

KIND_MODEL_NAMES = {
    "pdf": "PDFDocument",
    "document": "Document",
    "email": "Email",
    "thread": "EmailThread",
    "event": "Event",
    "photo": "Photo",
    "photodoc": "PhotoDocument",
    "chatsequence": "ChatSequence",
}


@dataclass(frozen=True)
class AuditIssue:
    severity: str
    stage: str
    code: str
    message: str
    file: str = ""
    cote: str = ""
    model: str = ""
    pk: str = ""
    detail: str = ""


def make_issue(
    severity: str,
    code: str,
    message: str,
    *,
    file: str = "",
    cote: str = "",
    model: str = "",
    pk: object = "",
    detail: str = "",
) -> AuditIssue:
    if severity not in SEVERITY_ORDER:
        raise ValueError(f"Niveau de sévérité inconnu : {severity}")
    if code.startswith(("ASSEMBLY_", "ASSEMBLED_", "DEPOT_")):
        stage = "communication"
    elif code.startswith(
        (
            "RENDERER_",
            "MANUAL_",
            "ORIGINAL_",
            "EVENT_",
            "PHOTODOC_",
            "THREAD_EMPTY",
            "CHATSEQUENCE_",
            "PDF_EXTENSION_",
        )
    ):
        stage = "render"
    else:
        stage = "source"
    return AuditIssue(
        severity=severity,
        stage=stage,
        code=code,
        message=message,
        file=file,
        cote=cote,
        model=model,
        pk=str(pk) if pk != "" else "",
        detail=detail,
    )


def normalize_piece_filename(raw_name: str) -> str:
    """Normalise une référence Markdown vers le nom du fichier attendu."""
    name = raw_name.strip().strip("`").rstrip(".,;:")
    if not name.casefold().endswith(".md"):
        name += ".md"
    return name


def extract_piece_filenames(text: str) -> list[str]:
    """Retourne les références ``piece_*`` distinctes, dans leur ordre."""
    names: list[str] = []
    seen: set[str] = set()
    for match in PIECE_TOKEN_PATTERN.finditer(text or ""):
        name = normalize_piece_filename(match.group("name"))
        key = name.casefold()
        if key not in seen:
            seen.add(key)
            names.append(name)
    return names


def identity_key(model: str, pk: object) -> str:
    return f"{model}:{pk}"


def compare_identity_sets(
    expected: set[str],
    actual: set[str],
) -> tuple[str, str, str] | None:
    """Compare l'identité du bordereau à celle de ses fiches d'appui."""
    if not expected or not actual:
        return None
    if expected == actual:
        return None
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    detail = f"manquantes={missing}; supplémentaires={extra}"
    if missing:
        return (
            "error",
            "BORDEREAU_PIECE_SOURCE_MISMATCH",
            detail,
        )
    return (
        "warning",
        "PIECE_HAS_ADDITIONAL_SOURCES",
        detail,
    )


def _piece_occurrences(path: Path, legal_dir: Path) -> list[ReferenceOccurrence]:
    """Résout l'identité primaire déclarée par une fiche ``piece_*.md``."""
    occurrences = extract_references_from_text(
        path.name,
        source_file=path.name,
        source_format="piece_filename",
        source_location="filename",
        context=path.name,
    )
    return resolve_descriptive_piece_occurrences(occurrences, legal_dir)


def _load_objects(
    identities: Iterable[tuple[str, int]],
) -> dict[tuple[str, int], Model]:
    """Charge les objets par lots, avec les relations utiles aux validateurs."""
    grouped: dict[str, set[int]] = {}
    for model_name, pk in identities:
        grouped.setdefault(model_name, set()).add(pk)

    objects: dict[tuple[str, int], Model] = {}
    for model_name, pks in grouped.items():
        model_class = MODEL_CLASSES.get(model_name)
        if model_class is None:
            continue
        queryset = model_class.objects.filter(pk__in=sorted(pks))
        if model_class == Email:
            queryset = queryset.select_related("thread")
        elif model_class == Event:
            queryset = queryset.select_related("linked_email").prefetch_related(
                "linked_photos"
            )
        elif model_class == PhotoDocument:
            queryset = queryset.prefetch_related("photos")
        elif model_class == EmailThread:
            queryset = queryset.prefetch_related("emails")
        elif model_class == ChatSequence:
            queryset = queryset.prefetch_related("messages")
        for obj in queryset:
            objects[(model_name, obj.pk)] = obj
    return objects


def _validate_object(obj: Model, *, file: str = "", cote: str = "") -> list[AuditIssue]:
    """Contrôles structurels propres aux modèles, sans modifier l'objet."""
    issues: list[AuditIssue] = []
    model_name = obj.__class__.__name__
    common = {"file": file, "cote": cote, "model": model_name, "pk": obj.pk}

    if isinstance(obj, PDFDocument):
        if not (obj.title or "").strip():
            issues.append(
                make_issue(
                    "warning",
                    "PDF_TITLE_EMPTY",
                    "Le document PDF n'a pas de titre.",
                    **common,
                )
            )
        if obj.file and Path(obj.file.name).suffix.casefold() != ".pdf":
            issues.append(
                make_issue(
                    "error",
                    "PDF_EXTENSION_INVALID",
                    "Le fichier d'un PDFDocument n'a pas l'extension .pdf.",
                    detail=str(obj.file.name),
                    **common,
                )
            )

    elif isinstance(obj, Email):
        if obj.date_sent is None:
            issues.append(
                make_issue(
                    "warning",
                    "EMAIL_DATE_MISSING",
                    "Le courriel n'a pas de date d'envoi.",
                    **common,
                )
            )
        if not (obj.sender or "").strip():
            issues.append(
                make_issue(
                    "warning",
                    "EMAIL_SENDER_MISSING",
                    "Le courriel n'a pas d'expéditeur enregistré.",
                    **common,
                )
            )
        if not (obj.body_plain_text or "").strip():
            issues.append(
                make_issue(
                    "warning",
                    "EMAIL_BODY_EMPTY",
                    "Le corps texte du courriel est vide.",
                    **common,
                )
            )

    elif isinstance(obj, EmailThread):
        if not list(obj.emails.all()):
            issues.append(
                make_issue(
                    "error",
                    "THREAD_EMPTY",
                    "Le fil ne contient aucun courriel et ne peut pas être rendu.",
                    **common,
                )
            )

    elif isinstance(obj, Event):
        if not list(obj.linked_photos.all()):
            issues.append(
                make_issue(
                    "error",
                    "EVENT_WITHOUT_PHOTOS",
                    "L'événement ne contient aucune photo; son renderer échouerait.",
                    **common,
                )
            )

    elif isinstance(obj, Photo):
        if not obj.datetime_original and not obj.datetime_utc and not obj.date_folder:
            issues.append(
                make_issue(
                    "warning",
                    "PHOTO_DATE_MISSING",
                    "La photo ne possède aucune date exploitable.",
                    **common,
                )
            )

    elif isinstance(obj, PhotoDocument):
        if not list(obj.photos.all()):
            issues.append(
                make_issue(
                    "error",
                    "PHOTODOC_EMPTY",
                    "Le document photographié ne contient aucune photo.",
                    **common,
                )
            )

    elif isinstance(obj, Document):
        if not (obj.title or "").strip():
            issues.append(
                make_issue(
                    "warning",
                    "DOCUMENT_TITLE_EMPTY",
                    "Le document n'a pas de titre.",
                    **common,
                )
            )
        if obj.source_type == DocumentSource.REPRODUCED and not obj.file_source:
            issues.append(
                make_issue(
                    "warning",
                    "DOCUMENT_SOURCE_FILE_MISSING",
                    "Le document reproduit n'a pas de fichier source enregistré.",
                    **common,
                )
            )

    elif isinstance(obj, ChatSequence):
        messages = list(obj.messages.all())
        if not messages:
            issues.append(
                make_issue(
                    "error",
                    "CHATSEQUENCE_EMPTY",
                    "La séquence de clavardage ne contient aucun message.",
                    **common,
                )
            )
        else:
            timestamps = sorted(message.timestamp for message in messages)
            if obj.start_date and obj.start_date != timestamps[0]:
                issues.append(
                    make_issue(
                        "warning",
                        "CHATSEQUENCE_START_MISMATCH",
                        "La date de début ne correspond pas au premier message.",
                        detail=f"enregistrée={obj.start_date}; réelle={timestamps[0]}",
                        **common,
                    )
                )
            if obj.end_date and obj.end_date != timestamps[-1]:
                issues.append(
                    make_issue(
                        "warning",
                        "CHATSEQUENCE_END_MISMATCH",
                        "La date de fin ne correspond pas au dernier message.",
                        detail=f"enregistrée={obj.end_date}; réelle={timestamps[-1]}",
                        **common,
                    )
                )

    elif isinstance(obj, ChatMessage):
        if not (obj.text_content or "").strip():
            issues.append(
                make_issue(
                    "warning",
                    "CHATMESSAGE_EMPTY",
                    "Le message de clavardage est vide.",
                    **common,
                )
            )

    return issues


def _validate_assembly_source(
    *,
    cote: str,
    ref: SourceRef,
    objects: list[Model],
) -> list[AuditIssue]:
    """Vérifie que la source peut être rendue sans placeholder silencieux."""
    issues: list[AuditIssue] = []
    if ref.kind not in RENDERERS:
        issues.append(
            make_issue(
                "error",
                "RENDERER_MISSING",
                "Aucun renderer PDF n'est disponible pour cette source.",
                cote=cote,
                detail=ref.kind,
            )
        )
        return issues

    for obj in objects:
        issues.extend(_validate_object(obj, cote=cote))
        model_name = obj.__class__.__name__
        if ref.kind == "document":
            # Rendu depuis le modèle documentaire : aucune représentation
            # manuelle n'est requise, mais l'arbre doit porter du contenu.
            if not obj.nodes.filter(depth__gt=1, is_evidence=False).exists():
                issues.append(
                    make_issue(
                        "error",
                        "DOCUMENT_TREE_EMPTY",
                        "Le document ne porte aucun paragraphe : le rendu serait vide.",
                        cote=cote,
                        model=model_name,
                        pk=obj.pk,
                    )
                )
            continue

        if ref.kind == "chatsequence":
            # Transcription depuis la base : aucune représentation manuelle
            # n'est requise, mais la séquence doit porter des messages.
            if not obj.messages.exists():
                issues.append(
                    make_issue(
                        "error",
                        "CHATSEQUENCE_EMPTY",
                        "La séquence ne contient aucun message : la transcription serait vide.",
                        cote=cote,
                        model=model_name,
                        pk=obj.pk,
                    )
                )
            continue

        status, reference = object_original_status(obj)
        if status in {"missing", "none_available", "partially_available"}:
            severity = "warning" if ref.kind in {"email", "thread"} else "error"
            issues.append(
                make_issue(
                    severity,
                    "ORIGINAL_INCOMPLETE",
                    "L'original nécessaire à l'assemblage est absent ou incomplet.",
                    cote=cote,
                    model=model_name,
                    pk=obj.pk,
                    detail=f"{status}: {reference}",
                )
            )
    return issues


def _source_ref_without_override(row: BordereauRow, text: str) -> SourceRef | None:
    """Résout une seule colonne sans déclencher SOURCE_OVERRIDES par cote."""
    isolated = BordereauRow(
        cote=f"AUDIT-{row.cote}",
        date=row.date,
        description=row.description,
        fichier_appui=text,
        source_base="",
    )
    return resolve_source(isolated)


def _canonical_identities(
    ref: SourceRef,
    objects: list[Model],
) -> set[str]:
    if ref.kind == "path":
        return {f"path:{value}" for value in ref.ids}
    model_name = KIND_MODEL_NAMES.get(ref.kind)
    if not model_name:
        return set()
    return {identity_key(model_name, obj.pk) for obj in objects}


def _read_assembly_manifest(assembly_dir: Path) -> tuple[dict, AuditIssue | None]:
    path = assembly_dir / "manifest.json"
    if not path.is_file():
        return {}, make_issue(
            "warning",
            "ASSEMBLY_MANIFEST_MISSING",
            "Aucun manifest d'assemblage pieces_pdf n'est disponible.",
            file=str(path),
        )
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except (OSError, json.JSONDecodeError) as exc:
        return {}, make_issue(
            "error",
            "ASSEMBLY_MANIFEST_INVALID",
            "Le manifest d'assemblage est illisible.",
            file=str(path),
            detail=str(exc),
        )


TOP_LEVEL_DEPOT_PATTERN = re.compile(
    r"^\s*-\s+\*\*(?P<cote>P-\d+)\*\*\s+—\s+(?P<body>.+?)\s*;?\s*$",
    re.IGNORECASE,
)
SUBCOTE_DEPOT_PATTERN = re.compile(
    r"^\|\s*(?P<cote>P-\d+\.\d+)\s*\|[^|]*\|"
    r"\s*(?P<model>[A-Za-z]+)\s*:\s*(?P<pk>\d+)\s*\|",
    re.IGNORECASE,
)
DEPOT_MODEL_NAMES = {
    "email": "Email",
    "event": "Event",
    "pdfdocument": "PDFDocument",
    "photodocument": "PhotoDocument",
    "photo": "Photo",
    "document": "Document",
    "chatsequence": "ChatSequence",
}


def parse_depot_bordereau(path: Path) -> dict:
    """Parse les cotes principales et l'index des sous-cotes du dépôt."""
    top_level: list[str] = []
    subcotes: dict[str, list[tuple[str, str]]] = {}
    duplicates: list[str] = []
    seen: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        top_match = TOP_LEVEL_DEPOT_PATTERN.match(line)
        if top_match:
            cote = top_match.group("cote").upper()
            if cote in seen:
                duplicates.append(cote)
            else:
                seen.add(cote)
                top_level.append(cote)
            continue
        sub_match = SUBCOTE_DEPOT_PATTERN.match(line)
        if not sub_match:
            continue
        subcote = sub_match.group("cote").upper()
        parent = subcote.split(".", 1)[0]
        model = DEPOT_MODEL_NAMES.get(
            sub_match.group("model").casefold(),
            sub_match.group("model"),
        )
        subcotes.setdefault(parent, []).append(
            (subcote, identity_key(model, int(sub_match.group("pk"))))
        )
    return {
        "top_level": top_level,
        "subcotes": subcotes,
        "duplicates": duplicates,
    }


def _expected_subcote_identities(ref: SourceRef) -> list[str]:
    model_name = KIND_MODEL_NAMES.get(ref.kind)
    if not model_name or ref.kind == "thread":
        return []
    identities = []
    for raw_id in ref.ids:
        if not str(raw_id).isdigit():
            return []
        identities.append(identity_key(model_name, int(raw_id)))
    return identities


def validate_depot_bordereau(
    *,
    technical_rows: list[BordereauRow],
    depot_path: Path,
) -> tuple[dict, list[AuditIssue]]:
    """Compare le registre technique au bordereau présenté pour le dépôt."""
    issues: list[AuditIssue] = []
    result = {
        "available": depot_path.is_file(),
        "top_level_count": 0,
        "indexed_group_count": 0,
    }
    if not depot_path.is_file():
        issues.append(
            make_issue(
                "error",
                "DEPOT_BORDEREAU_MISSING",
                "Le bordereau destiné au dépôt est introuvable.",
                file=str(depot_path),
            )
        )
        return result, issues

    parsed = parse_depot_bordereau(depot_path)
    depot_cotes = parsed["top_level"]
    result["top_level_count"] = len(depot_cotes)
    result["indexed_group_count"] = len(parsed["subcotes"])
    for cote in parsed["duplicates"]:
        issues.append(
            make_issue(
                "error",
                "DEPOT_DUPLICATE_COTE",
                "Une cote principale apparaît plusieurs fois dans le bordereau de dépôt.",
                cote=cote,
                file=str(depot_path),
            )
        )

    technical_cotes = [row.cote.upper() for row in technical_rows]
    technical_set = set(technical_cotes)
    depot_set = set(depot_cotes)
    for cote in sorted(technical_set - depot_set):
        issues.append(
            make_issue(
                "error",
                "DEPOT_COTE_MISSING",
                "Une cote technique est absente du bordereau de dépôt.",
                cote=cote,
                file=str(depot_path),
            )
        )
    for cote in sorted(depot_set - technical_set):
        issues.append(
            make_issue(
                "error",
                "DEPOT_COTE_WITHOUT_TECHNICAL_SOURCE",
                "Une cote du bordereau de dépôt n'existe pas dans le registre technique.",
                cote=cote,
                file=str(depot_path),
            )
        )
    if depot_cotes and technical_cotes and depot_cotes != technical_cotes:
        issues.append(
            make_issue(
                "error",
                "DEPOT_COTE_ORDER_MISMATCH",
                "L'ordre des cotes principales diffère entre les deux bordereaux.",
                file=str(depot_path),
            )
        )

    rows_by_cote = {row.cote.upper(): row for row in technical_rows}
    for parent, entries in parsed["subcotes"].items():
        row = rows_by_cote.get(parent)
        if not row:
            continue
        ref = resolve_source(row)
        if not ref:
            continue
        actual_identities = [identity for _, identity in entries]
        expected_identities = _expected_subcote_identities(ref)
        if expected_identities and actual_identities != expected_identities:
            issues.append(
                make_issue(
                    "error",
                    "DEPOT_SUBCOTE_SOURCE_MISMATCH",
                    "L'ordre ou l'identité des sous-cotes diffère du registre technique.",
                    cote=parent,
                    file=str(depot_path),
                    detail=(
                        f"dépôt={actual_identities}; "
                        f"technique={expected_identities}"
                    ),
                )
            )
        expected_labels = [
            f"{parent}.{index}"
            for index in range(1, len(actual_identities) + 1)
        ]
        actual_labels = [label for label, _ in entries]
        if actual_labels != expected_labels:
            issues.append(
                make_issue(
                    "error",
                    "DEPOT_SUBCOTE_SEQUENCE_INVALID",
                    "La numérotation des sous-cotes n'est pas continue.",
                    cote=parent,
                    file=str(depot_path),
                    detail=str(actual_labels),
                )
            )
    return result, issues


def _validate_assembled_entry(
    *,
    row: BordereauRow,
    ref: SourceRef,
    manifest: dict,
    assembly_dir: Path,
) -> tuple[dict, list[AuditIssue]]:
    issues: list[AuditIssue] = []
    meta = manifest.get(row.cote)
    result = {
        "manifest_status": "missing",
        "assembled_file": "",
        "assembled_exists": False,
        "assembled_page_count": 0,
        "assembled_sha256": "",
        "placeholder": False,
    }
    if not meta:
        issues.append(
            make_issue(
                "error",
                "ASSEMBLED_COTE_MISSING",
                "La cote du bordereau est absente du manifest assemblé.",
                cote=row.cote,
            )
        )
        return result, issues

    result["manifest_status"] = str(meta.get("status", ""))
    result["placeholder"] = bool(meta.get("placeholder"))
    if meta.get("status") != "ok":
        issues.append(
            make_issue(
                "error",
                "ASSEMBLED_COTE_NOT_OK",
                "La cote assemblée n'a pas le statut ok.",
                cote=row.cote,
                detail=str(meta.get("error", "")),
            )
        )
    if result["placeholder"]:
        issues.append(
            make_issue(
                "error",
                "ASSEMBLED_PLACEHOLDER",
                "Le PDF assemblé contient une représentation de remplacement.",
                cote=row.cote,
            )
        )

    manifest_kind = str(meta.get("source_type", ""))
    manifest_ids = [str(value) for value in meta.get("source_ids", [])]
    if manifest_kind and manifest_kind != ref.kind:
        issues.append(
            make_issue(
                "error",
                "ASSEMBLY_SOURCE_TYPE_MISMATCH",
                "Le type de source assemblé diffère du bordereau courant.",
                cote=row.cote,
                detail=f"manifest={manifest_kind}; bordereau={ref.kind}",
            )
        )
    if manifest_ids and manifest_ids != list(ref.ids):
        issues.append(
            make_issue(
                "error",
                "ASSEMBLY_SOURCE_IDS_MISMATCH",
                "Les identifiants assemblés diffèrent du bordereau courant.",
                cote=row.cote,
                detail=f"manifest={manifest_ids}; bordereau={list(ref.ids)}",
            )
        )

    output_name = str(meta.get("output") or f"{row.cote}.pdf")
    output_path = assembly_dir / output_name
    result["assembled_file"] = str(output_path)
    result["assembled_exists"] = output_path.is_file() and output_path.stat().st_size > 0
    if not result["assembled_exists"]:
        issues.append(
            make_issue(
                "error",
                "ASSEMBLED_PDF_MISSING",
                "Le PDF normalisé annoncé par le manifest est absent ou vide.",
                cote=row.cote,
                file=str(output_path),
            )
        )
        return result, issues

    try:
        with fitz.open(str(output_path)) as document:
            result["assembled_page_count"] = document.page_count
    except Exception as exc:
        issues.append(
            make_issue(
                "error",
                "ASSEMBLED_PDF_INVALID",
                "Le PDF normalisé est illisible ou corrompu.",
                cote=row.cote,
                file=str(output_path),
                detail=str(exc),
            )
        )
    else:
        if result["assembled_page_count"] < 1:
            issues.append(
                make_issue(
                    "error",
                    "ASSEMBLED_PDF_EMPTY",
                    "Le PDF normalisé ne contient aucune page.",
                    cote=row.cote,
                    file=str(output_path),
                )
            )
        manifest_page_count = meta.get("page_count")
        if (
            manifest_page_count is not None
            and manifest_page_count != result["assembled_page_count"]
        ):
            issues.append(
                make_issue(
                    "error",
                    "ASSEMBLY_PAGE_COUNT_MISMATCH",
                    "Le nombre de pages du PDF diffère du manifest.",
                    cote=row.cote,
                    file=str(output_path),
                    detail=(
                        f"manifest={manifest_page_count}; "
                        f"pdf={result['assembled_page_count']}"
                    ),
                )
            )
    result["assembled_sha256"] = hashlib.sha256(output_path.read_bytes()).hexdigest()
    return result, issues


def audit_piece_chain(
    *,
    legal_dir: Path,
    bordereau_path: Path,
    depot_bordereau_path: Path,
    assembly_dir: Path,
) -> dict:
    """Exécute l'audit complet des fiches, du bordereau et de l'assemblage."""
    legal_dir = legal_dir.resolve()
    bordereau_path = bordereau_path.resolve()
    assembly_dir = assembly_dir.resolve()
    rows = parse_bordereau(bordereau_path)
    bordereau_support_names = {
        name.casefold()
        for row in rows
        for name in extract_piece_filenames(row.fichier_appui)
    }
    piece_paths = sorted(
        legal_dir.glob("piece*.md"),
        key=lambda path: path.name.casefold(),
    )

    piece_occurrences: dict[str, list[ReferenceOccurrence]] = {}
    all_occurrences: list[ReferenceOccurrence] = []
    issues: list[AuditIssue] = []
    for path in piece_paths:
        occurrences = _piece_occurrences(path, legal_dir)
        piece_occurrences[path.name] = occurrences
        all_occurrences.extend(occurrences)

    reference_audit = audit_occurrences(all_occurrences)
    canonical_rows = {
        row["canonical_key"]: row for row in reference_audit["canonical"]
    }
    all_identities = {
        (occurrence.model, occurrence.pk)
        for occurrence in all_occurrences
        if occurrence.model and occurrence.pk is not None
    }
    objects = _load_objects(all_identities)

    piece_rows: list[dict] = []
    piece_identity_map: dict[str, set[str]] = {}
    for path in piece_paths:
        occurrences = piece_occurrences[path.name]
        identities = {
            identity_key(item.model, item.pk)
            for item in occurrences
            if item.model and item.pk is not None
        }
        piece_identity_map[path.name.casefold()] = identities
        forms = sorted({item.reference_form for item in occurrences})
        record_issues: list[AuditIssue] = []
        if not identities:
            is_bordereau_support = path.name.casefold() in bordereau_support_names
            record_issues.append(
                make_issue(
                    "error" if is_bordereau_support else "warning",
                    (
                        "PIECE_IDENTITY_UNRESOLVED"
                        if is_bordereau_support
                        else "UNUSED_PIECE_IDENTITY_UNRESOLVED"
                    ),
                    (
                        "La fiche citée au bordereau ne peut pas être reliée "
                        "à un objet (model, pk)."
                        if is_bordereau_support
                        else "La fiche non citée au bordereau n'expose pas "
                        "d'identité primaire résoluble."
                    ),
                    file=str(path),
                )
            )
        if any(
            form in {"descriptive_piece_resolved", "descriptive_piece_components"}
            for form in forms
        ):
            record_issues.append(
                make_issue(
                    "info",
                    "PIECE_DESCRIPTIVE_NAME",
                    "L'identité est résolue depuis le contenu plutôt que le nom.",
                    file=str(path),
                )
            )

        dates: list[str] = []
        titles: list[str] = []
        original_statuses: list[str] = []
        for canonical_key in sorted(identities):
            canonical = canonical_rows.get(canonical_key)
            if not canonical or canonical["db_status"] != "found":
                model_name, pk = canonical_key.split(":", 1)
                record_issues.append(
                    make_issue(
                        "error",
                        "PIECE_DB_OBJECT_MISSING",
                        "L'objet référencé par la fiche est absent de PostgreSQL.",
                        file=str(path),
                        model=model_name,
                        pk=pk,
                    )
                )
                continue
            dates.append(canonical["object_date"])
            titles.append(canonical["object_title"])
            original_statuses.append(canonical["original_status"])
            if canonical["context_status"].startswith("mismatch"):
                record_issues.append(
                    make_issue(
                        "error",
                        "PIECE_THREAD_MISMATCH",
                        "Le courriel n'appartient pas au fil annoncé dans le nom.",
                        file=str(path),
                        model=canonical["model"],
                        pk=canonical["pk"],
                        detail=canonical["context_status"],
                    )
                )
            obj = objects.get((canonical["model"], canonical["pk"]))
            if obj:
                record_issues.extend(_validate_object(obj, file=str(path)))

        issues.extend(record_issues)
        piece_rows.append(
            {
                "file": str(path),
                "reference_forms": " | ".join(forms),
                "canonical_identities": " | ".join(sorted(identities)),
                "identity_count": len(identities),
                "db_status": (
                    "unresolved"
                    if not identities
                    else "missing"
                    if any(
                        canonical_rows.get(key, {}).get("db_status") != "found"
                        for key in identities
                    )
                    else "found"
                ),
                "original_statuses": " | ".join(sorted(set(original_statuses))),
                "object_dates": " | ".join(value for value in dates if value),
                "object_titles": " | ".join(value for value in titles if value),
                "issue_count": len(record_issues),
            }
        )

    depot_result, depot_issues = validate_depot_bordereau(
        technical_rows=rows,
        depot_path=depot_bordereau_path.resolve(),
    )
    issues.extend(depot_issues)
    manifest, manifest_issue = _read_assembly_manifest(assembly_dir)
    if manifest_issue:
        issues.append(manifest_issue)

    bordereau_rows: list[dict] = []
    seen_cotes: set[str] = set()
    resolved_cache: dict[tuple[str, tuple[str, ...]], list[Model]] = {}
    numeric_cotes: list[int] = []
    for row in rows:
        row_issues: list[AuditIssue] = []
        if row.cote in seen_cotes:
            row_issues.append(
                make_issue(
                    "error",
                    "BORDEREAU_DUPLICATE_COTE",
                    "La cote apparaît plus d'une fois dans le bordereau.",
                    cote=row.cote,
                )
            )
        seen_cotes.add(row.cote)
        number_match = re.fullmatch(r"P-(\d+)", row.cote, re.IGNORECASE)
        if number_match:
            numeric_cotes.append(int(number_match.group(1)))

        ref = resolve_source(row)
        support_names = extract_piece_filenames(row.fichier_appui)
        support_identities: set[str] = set()
        missing_support_files: list[str] = []
        for name in support_names:
            path = legal_dir / name
            if not path.is_file():
                missing_support_files.append(name)
                row_issues.append(
                    make_issue(
                        "error",
                        "BORDEREAU_PIECE_FILE_MISSING",
                        "La fiche d'appui citée au bordereau est introuvable.",
                        cote=row.cote,
                        file=str(path),
                    )
                )
                continue
            support_identities.update(piece_identity_map.get(name.casefold(), set()))

        if not support_names:
            row_issues.append(
                make_issue(
                    "info",
                    "BORDEREAU_DIRECT_SOURCE",
                    "La ligne utilise directement une source DB, sans fiche piece_*.md.",
                    cote=row.cote,
                )
            )

        expected_identities: set[str] = set()
        resolved_objects: list[Model] = []
        assembly_result = {
            "manifest_status": "not_checked",
            "assembled_file": "",
            "assembled_exists": False,
            "assembled_page_count": 0,
            "assembled_sha256": "",
            "placeholder": False,
        }
        if ref is None:
            row_issues.append(
                make_issue(
                    "error",
                    "BORDEREAU_SOURCE_UNRESOLVED",
                    "La source de la ligne du bordereau ne peut pas être résolue.",
                    cote=row.cote,
                    detail=f"{row.fichier_appui} | {row.source_base}",
                )
            )
        else:
            cache_key = (ref.kind, tuple(ref.ids))
            try:
                if cache_key not in resolved_cache:
                    resolved_cache[cache_key] = resolve_objects(ref)
                resolved_objects = resolved_cache[cache_key]
                expected_identities = _canonical_identities(ref, resolved_objects)
            except Exception as exc:
                row_issues.append(
                    make_issue(
                        "error",
                        "BORDEREAU_DB_OBJECT_MISSING",
                        "Une source du bordereau est absente ou inaccessible.",
                        cote=row.cote,
                        detail=f"{ref.kind}:{','.join(ref.ids)} — {exc}",
                    )
                )
            else:
                row_issues.extend(
                    _validate_assembly_source(
                        cote=row.cote,
                        ref=ref,
                        objects=resolved_objects,
                    )
                )

            comparison = compare_identity_sets(expected_identities, support_identities)
            if comparison:
                severity, code, detail = comparison
                row_issues.append(
                    make_issue(
                        severity,
                        code,
                        "L'identité des fiches d'appui ne correspond pas à la source du bordereau.",
                        cote=row.cote,
                        detail=detail,
                    )
                )

            support_ref = _source_ref_without_override(row, row.fichier_appui)
            base_ref = _source_ref_without_override(row, row.source_base)
            if (
                support_ref
                and base_ref
                and support_ref != base_ref
                and row.cote not in {"P-35", "P-36"}
            ):
                row_issues.append(
                    make_issue(
                        "warning",
                        "BORDEREAU_COLUMNS_DISAGREE",
                        "Les colonnes Fichier d'appui et Source (base) se résolvent différemment.",
                        cote=row.cote,
                        detail=f"appui={support_ref}; base={base_ref}",
                    )
                )

            if manifest:
                assembly_result, assembly_issues = _validate_assembled_entry(
                    row=row,
                    ref=ref,
                    manifest=manifest,
                    assembly_dir=assembly_dir,
                )
                row_issues.extend(assembly_issues)

        issues.extend(row_issues)
        bordereau_rows.append(
            {
                "cote": row.cote,
                "date": row.date,
                "description": row.description,
                "fichier_appui": row.fichier_appui,
                "source_base": row.source_base,
                "resolved_source": (
                    f"{ref.kind}:{','.join(ref.ids)}" if ref else ""
                ),
                "piece_files": " | ".join(support_names),
                "piece_identities": " | ".join(sorted(support_identities)),
                "expected_identities": " | ".join(sorted(expected_identities)),
                "missing_piece_files": " | ".join(missing_support_files),
                **assembly_result,
                "issue_count": len(row_issues),
            }
        )

    if numeric_cotes:
        expected_numbers = set(range(min(numeric_cotes), max(numeric_cotes) + 1))
        missing_numbers = sorted(expected_numbers - set(numeric_cotes))
        if missing_numbers:
            issues.append(
                make_issue(
                    "error",
                    "BORDEREAU_COTE_GAP",
                    "La séquence des cotes du bordereau contient des trous.",
                    detail=", ".join(f"P-{number}" for number in missing_numbers),
                )
            )

    if manifest:
        manifest_summary = manifest.get("_summary", {})
        manifest_count = manifest_summary.get("exhibit_count")
        if manifest_count is not None and manifest_count != len(rows):
            issues.append(
                make_issue(
                    "error",
                    "ASSEMBLY_COUNT_MISMATCH",
                    "Le nombre de pièces du manifest diffère du bordereau courant.",
                    detail=f"manifest={manifest_count}; bordereau={len(rows)}",
                )
            )
        manifest_cotes = {
            key for key in manifest if re.fullmatch(r"P-\d+", key, re.IGNORECASE)
        }
        stale_cotes = sorted(manifest_cotes - seen_cotes)
        if stale_cotes:
            issues.append(
                make_issue(
                    "warning",
                    "ASSEMBLY_HAS_STALE_COTES",
                    "Le manifest assemblé contient des cotes absentes du bordereau.",
                    detail=", ".join(stale_cotes),
                )
            )
        expected_outputs = {
            Path(str(manifest.get(row.cote, {}).get("output") or f"{row.cote}.pdf")).name
            for row in rows
            if row.cote in manifest
        }
        extra_outputs = sorted(
            path.name
            for path in assembly_dir.glob("P-*.pdf")
            if path.name not in expected_outputs
        )
        if extra_outputs:
            issues.append(
                make_issue(
                    "warning",
                    "ASSEMBLY_EXTRA_PDFS",
                    "Des PDF assemblés ne sont référencés par aucune cote courante.",
                    detail=", ".join(extra_outputs),
                )
            )

    issues = sorted(
        issues,
        key=lambda issue: (
            -SEVERITY_ORDER[issue.severity],
            issue.cote,
            issue.file.casefold(),
            issue.code,
            issue.model,
            issue.pk,
        ),
    )
    severity_counts = Counter(issue.severity for issue in issues)
    code_counts = Counter(issue.code for issue in issues)
    stage_error_counts = Counter(
        issue.stage for issue in issues if issue.severity == "error"
    )
    summary = {
        "piece_file_count": len(piece_rows),
        "piece_resolved_count": sum(row["db_status"] == "found" for row in piece_rows),
        "piece_unresolved_count": sum(
            row["db_status"] == "unresolved" for row in piece_rows
        ),
        "piece_db_missing_count": sum(
            row["db_status"] == "missing" for row in piece_rows
        ),
        "bordereau_cote_count": len(bordereau_rows),
        "bordereau_resolved_count": sum(
            bool(row["resolved_source"]) for row in bordereau_rows
        ),
        "bordereau_with_piece_file_count": sum(
            bool(row["piece_files"]) for row in bordereau_rows
        ),
        "depot_bordereau_cote_count": depot_result["top_level_count"],
        "depot_indexed_group_count": depot_result["indexed_group_count"],
        "assembled_cote_count": sum(
            row["assembled_exists"] for row in bordereau_rows
        ),
        "assembled_placeholder_count": sum(
            row["placeholder"] for row in bordereau_rows
        ),
        "issue_count": len(issues),
        "error_count": severity_counts["error"],
        "warning_count": severity_counts["warning"],
        "info_count": severity_counts["info"],
        "issue_codes": dict(sorted(code_counts.items())),
        "source_error_count": stage_error_counts["source"],
        "render_error_count": stage_error_counts["render"],
        "communication_error_count": stage_error_counts["communication"],
        "source_ready": stage_error_counts["source"] == 0,
        "render_ready": (
            stage_error_counts["source"] == 0
            and stage_error_counts["render"] == 0
        ),
        "communication_ready": severity_counts["error"] == 0,
    }
    return {
        "summary": summary,
        "pieces": piece_rows,
        "bordereau": bordereau_rows,
        "issues": [asdict(issue) for issue in issues],
    }


def _write_csv(path: Path, rows: list[dict]) -> None:
    fieldnames = list(rows[0].keys()) if rows else ["status"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows or [{"status": "aucune ligne"}])


def write_piece_audit_reports(output_dir: Path, audit: dict) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = [
        output_dir / "audit_piece_chain.json",
        output_dir / "resume_piece_chain.json",
        output_dir / "pieces_auditees.csv",
        output_dir / "bordereau_audite.csv",
        output_dir / "anomalies_piece_chain.csv",
    ]
    paths[0].write_text(
        json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    paths[1].write_text(
        json.dumps(audit["summary"], ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    _write_csv(paths[2], audit["pieces"])
    _write_csv(paths[3], audit["bordereau"])
    _write_csv(paths[4], audit["issues"])
    return paths
