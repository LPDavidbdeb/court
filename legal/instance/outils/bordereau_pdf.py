"""Rend en PDF un bordereau d'envoi (art. 134 C.p.c.) écrit en Markdown.

Le corps vient du .md par pandoc ; l'en-tête du dossier est celui de
`rendre_pieces.py`. Aucun moteur LaTeX n'est requis.

La mise en page passe par `rendre_pieces.pdf_par_blocs`, et non par un
`fitz.Story` conduit à la main : ce module porte la protection établie le
1er nov. 2026 — `Story` perd du contenu quand il coupe lui-même entre deux
pages, donc chaque bloc est mesuré seul avant d'être placé.

Le bloc d'avertissement en citation (« > ... ») est un commentaire de travail :
il est RETIRÉ du PDF. Ce qui part ne porte que le bordereau lui-même.

Usage : bordereau_pdf.py <source.md> <sortie.pdf>
"""
import re
import subprocess
import sys
from pathlib import Path

import fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rendre_pieces as R  # noqa: E402

CSS = R.CSS + """
h1 { font-size: 13pt; text-align: center; font-weight: bold; margin: 0; }
h3 { font-size: 10.5pt; text-align: center; font-weight: normal; margin: 0; }
table.b td, table.b th { font-size: 8.5pt; border-bottom: 0.3pt solid #bbb;
                         padding: 3pt 5pt; vertical-align: top; }
table.b th { font-weight: bold; text-align: left; border-bottom: 0.6pt solid #666; }
code { font-family: monospace; font-size: 7.5pt; }
"""

HAUT = re.compile(r"<(h1|h2|h3|p|table|ul|ol|blockquote)\b[^>]*>.*?</\1>|<hr\s*/?>", re.S)


def blocs_du_md(chemin: str) -> list[str]:
    md = open(chemin, encoding="utf8").read()
    # les lignes « > ... » sont des notes de travail : elles ne partent pas
    md = "\n".join(l for l in md.splitlines() if not l.lstrip().startswith(">"))
    html = subprocess.run(["pandoc", "-f", "markdown+hard_line_breaks", "-t", "html", "--wrap=none"],
                          input=md, capture_output=True, text=True, check=True).stdout
    html = html.replace("<table>", '<table class="b">')
    blocs = [m.group(0) for m in HAUT.finditer(html)]
    if not blocs:
        raise ValueError(f"aucun bloc extrait de {chemin}")
    return [R.ENTETE] + blocs


def rendre(src: str, out: str) -> int:
    doc = R.pdf_par_blocs(blocs_du_md(src), css=CSS)
    n = doc.page_count
    for i, page in enumerate(doc):
        page.insert_text((72, R.LETTRE.height - 44),
                         f"N° {R.DOSSIER} — Bordereau d'envoi (art. 134 C.p.c.)",
                         fontsize=8, fontname="helv")
        t = f"Page {i + 1} sur {n}"
        page.insert_text((R.LETTRE.width - 72 - fitz.get_text_length(t, "helv", 8),
                          R.LETTRE.height - 44), t, fontsize=8, fontname="helv")
    doc.set_metadata({"title": f"Bordereau d'envoi (art. 134 C.p.c.) — {R.DOSSIER}",
                      "author": "Louis-Philippe David"})
    # Sans ceci, une page pèse ~148 Ko, presque uniquement des polices intégrées
    # en entier. Le sous-ensemble ramène à ~45 Ko, pour une pièce jointe de
    # courriel que la destinataire doit recevoir sans friction.
    try:
        doc.subset_fonts(verbose=False)
    except Exception:
        pass  # PyMuPDF trop ancien : on garde le PDF complet plutôt que d'échouer
    doc.save(out, garbage=4, deflate=True, clean=True)
    doc.close()
    return n


if __name__ == "__main__":
    print(sys.argv[2], rendre(sys.argv[1], sys.argv[2]), "pages")
