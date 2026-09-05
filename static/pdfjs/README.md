# PDF.js (vendored)

Mozilla PDF.js, kept in the repository so the quote workbench renders source
documents without reaching the network.

| | |
|---|---|
| Version | 3.11.174 |
| Package | [`pdfjs-dist`](https://www.npmjs.com/package/pdfjs-dist) |
| Fetched from | `https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/` |
| Licence | Apache 2.0 (notice retained at the head of each file) |

    5b5799e6f8c680663207ac5b42ee14eed2a406fa7af48f50c154f0c0b1566946  pdf.min.js
    feabdf309770ed24bba31a5467836cdc8cf639c705af27d52b585b041bb8527b  pdf.worker.min.js

Both files are the UMD build, loaded by a plain `<script>` tag from
`argument_manager/templates/argument_manager/_pdf_quote_selection_js.html`.
The worker is now served from this origin, so pdf.js loads it directly instead
of wrapping it in the blob it uses for cross-origin worker sources.

## What is deliberately not vendored

`cmaps/` — needed only by PDFs that reference a predefined CJK CMap. Every font
in the corpus uses `WinAnsiEncoding`, `MacRomanEncoding`, or `Identity-H` with
an embedded CID font, none of which read those tables.

`standard_fonts/` — the substitute faces pdf.js draws with when a PDF names one
of the 14 standard fonts without embedding it. No document in the corpus does:
all fonts are embedded. A future upload that isn't would still render, in a
system font rather than the intended one, and its text layer — the part the
quote workbench depends on — is unaffected either way.

Add either directory from the same package version if that changes, and point
`cMapUrl` / `standardFontDataUrl` at it when calling `getDocument`.

## Upgrading

Replace both files from one package version, update the version and hashes
above, and re-check the quote workbench: a document with a text layer must
still yield selectable text, since `renderTextLayer` is the part of the API
most likely to move between releases.
