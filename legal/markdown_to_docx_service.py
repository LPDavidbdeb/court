from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pypandoc


DEFAULT_REFERENCE_DOC_NAME = "reference_cour_superieure_quebec.docx"


@dataclass(frozen=True)
class ConversionResult:
    source_path: Path
    output_path: Path
    reference_doc: Path | None = None


class MarkdownToDocxService:
    """
    Convert Markdown files under legal/ into DOCX files under legal/docx_file/.

    The output mirrors the source path relative to legal/. For example:
    legal/analyse/foo.md -> legal/docx_file/analyse/foo.docx
    """

    def __init__(
        self,
        legal_root: str | Path | None = None,
        output_root_name: str = "docx_file",
        reference_doc: str | Path | None = None,
        use_default_reference_doc: bool = True,
    ) -> None:
        self.legal_root = (
            Path(legal_root).expanduser().resolve()
            if legal_root
            else Path(__file__).resolve().parent
        )
        self.output_root = self.legal_root / output_root_name
        self.reference_doc = self._resolve_reference_doc(
            reference_doc,
            use_default_reference_doc=use_default_reference_doc,
        )

    def output_path_for(self, markdown_path: str | Path) -> Path:
        source_path = self._resolve_markdown_path(markdown_path)
        relative_path = source_path.relative_to(self.legal_root)
        return (self.output_root / relative_path).with_suffix(".docx")

    def convert_file(self, markdown_path: str | Path, overwrite: bool = True) -> ConversionResult:
        source_path = self._resolve_markdown_path(markdown_path)
        output_path = self.output_path_for(source_path)

        if output_path.exists() and not overwrite:
            return ConversionResult(
                source_path=source_path,
                output_path=output_path,
                reference_doc=self.reference_doc,
            )

        output_path.parent.mkdir(parents=True, exist_ok=True)

        extra_args = ["--standalone"]
        if self.reference_doc:
            extra_args.extend(["--reference-doc", str(self.reference_doc)])

        pypandoc.convert_file(
            str(source_path),
            "docx",
            outputfile=str(output_path),
            extra_args=extra_args,
        )

        return ConversionResult(
            source_path=source_path,
            output_path=output_path,
            reference_doc=self.reference_doc,
        )

    def convert_all(self, overwrite: bool = True) -> list[ConversionResult]:
        results: list[ConversionResult] = []
        for markdown_path in self.iter_markdown_files():
            results.append(self.convert_file(markdown_path, overwrite=overwrite))
        return results

    def iter_markdown_files(self) -> Iterable[Path]:
        for markdown_path in sorted(self.legal_root.rglob("*.md")):
            if self.output_root in markdown_path.parents:
                continue
            yield markdown_path

    def _resolve_markdown_path(self, markdown_path: str | Path) -> Path:
        source_path = Path(markdown_path).expanduser()
        if not source_path.is_absolute():
            source_path = self.legal_root / source_path
        source_path = source_path.resolve()

        if not source_path.is_file():
            raise FileNotFoundError(f"Markdown file not found: {source_path}")
        if source_path.suffix.lower() != ".md":
            raise ValueError(f"Expected a .md file: {source_path}")
        if not source_path.is_relative_to(self.legal_root):
            raise ValueError(f"Markdown file must be inside legal/: {source_path}")
        if self.output_root in source_path.parents:
            raise ValueError(f"Refusing to convert files inside output directory: {source_path}")

        return source_path

    def _resolve_reference_doc(
        self,
        reference_doc: str | Path | None,
        use_default_reference_doc: bool,
    ) -> Path | None:
        if reference_doc:
            candidate = Path(reference_doc).expanduser()
            if not candidate.is_absolute():
                candidate = self.legal_root / candidate
            candidate = candidate.resolve()
            if not candidate.is_file():
                raise FileNotFoundError(f"Reference DOCX not found: {candidate}")
            if candidate.suffix.lower() != ".docx":
                raise ValueError(f"Expected a .docx reference file: {candidate}")
            return candidate

        if not use_default_reference_doc:
            return None

        default_reference_doc = self.legal_root / DEFAULT_REFERENCE_DOC_NAME
        return default_reference_doc if default_reference_doc.is_file() else None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert legal Markdown files to DOCX while preserving relative paths."
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="Markdown path relative to legal/, or an absolute path. Omit with --all.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Convert every .md file under legal/ except legal/docx_file/.",
    )
    parser.add_argument(
        "--no-overwrite",
        action="store_true",
        help="Keep existing .docx files instead of replacing them.",
    )
    parser.add_argument(
        "--reference-doc",
        help=(
            "DOCX template used by Pandoc for styling. Defaults to "
            f"{DEFAULT_REFERENCE_DOC_NAME} when present."
        ),
    )
    parser.add_argument(
        "--no-reference-doc",
        action="store_true",
        help="Disable the default court reference DOCX.",
    )
    args = parser.parse_args()

    if not args.all and not args.path:
        parser.error("provide a Markdown path or use --all")

    service = MarkdownToDocxService(
        reference_doc=args.reference_doc,
        use_default_reference_doc=not args.no_reference_doc,
    )
    overwrite = not args.no_overwrite

    if args.all:
        results = service.convert_all(overwrite=overwrite)
    else:
        results = [service.convert_file(args.path, overwrite=overwrite)]

    for result in results:
        reference_part = (
            f" (reference: {result.reference_doc})"
            if result.reference_doc
            else " (no reference doc)"
        )
        print(f"{result.source_path} -> {result.output_path}{reference_part}")


if __name__ == "__main__":
    main()
