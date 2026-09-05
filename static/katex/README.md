# KaTeX (vendored)

Khan Academy KaTeX, kept in the repository so formulas render without reaching
the network — the same reason pdf.js is vendored next door.

| | |
|---|---|
| Version | 0.16.22 |
| Package | [`katex`](https://www.npmjs.com/package/katex) |
| Fetched from | `https://registry.npmjs.org/katex/-/katex-0.16.22.tgz` (`package/dist/`) |
| Licence | MIT (notice retained at the head of each file) |

    e8d885505949f3a5f4abdd5dd0d53696bd1371ad26ffbf4f310dcd77c8cdae89  katex.min.js
    19095127357ed6d29fe0a63a6b000c913a89f7f1963b765dd3715e97c9852e75  katex.min.css

Loaded by a plain `<script>` and `<link>` from
`core/templates/core/partials/champs_editables_js.html`, alongside
`core/static/js/maths_plugin.js`, which is the TinyMCE side of the pairing.
The stylesheet resolves `fonts/` relative to itself, so the two must stay
siblings.

## What is deliberately not vendored

`fonts/*.woff` and `fonts/*.ttf` — the fallbacks the stylesheet names after
WOFF2 in each `@font-face`. A browser picks the first format it supports and
never requests the rest, and every browser TinyMCE 7 itself supports has had
WOFF2 for a decade. Keeping all three formats trebles the directory, from 592K
to 1.7M, for files no one would ever fetch. Copy them from the same package
version if a browser without WOFF2 ever has to be served.

`contrib/auto-render.js` — the extension that scans a page for `$…$` and
`\(…\)` in running text. Formulas here are never loose in the text: each one is
a `<span class="math-tex">` that `maths_plugin.js` finds by class and renders by
a direct `katex.render` call. Scanning the whole page would also mean finding
delimiters inside quoted evidence, which is precisely what must not happen.

`katex.css` (unminified), `katex.mjs`, and the sources — nothing loads them.

## Upgrading

Replace both files and `fonts/*.woff2` from one package version, update the
version and hashes above, and re-check the round trip that the whole design
rests on: open a field holding a formula, confirm it reverts to its `\(…\)`
source, and confirm `getContent()` returns that source with no `katex` markup
in it. `maths_plugin.js` documents why that invariant is the load-bearing one.
