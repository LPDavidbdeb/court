"""Rend en PDF la section « Texte » du relevé des points de divergence.

Le corps vient du .md (pandoc) ; seul l'en-tête du dossier est mis en page à la main.
Usage : releve_pdf.py <source.md> <sortie.pdf>
La section « Texte » est le bloc cité entre « ## Texte » et le « --- » suivant.
"""
import os, re, subprocess, sys

import fitz

src, out = sys.argv[1], sys.argv[2]
md = open(src, encoding="utf8").read()
texte = md.split("## Texte", 1)[1].split("\n---\n", 1)[0]
lignes = [re.sub(r"^> ?", "", l) for l in texte.strip().splitlines()]
corps = "\n".join(lignes)
# l'en-tête (jusqu'à « défenderesses ») est remplacé par la mise en page du dossier
corps = corps.split("défenderesses\n", 1)[1]
corps = corps.replace("## RELEVÉ DES POINTS DE DIVERGENCE\n### (art. 152 C.p.c.)", "")
# paragraphes numérotés : rendus tels quels (Story ne respecte pas <ol start>)
blocs = corps.split("\n\n")
for k, bl in enumerate(blocs):
    m = re.match(r"^(\d+)\. (.*)", bl, re.S)
    if m:
        txt = re.sub(r"\s*\n\s*", " ", m.group(2)).strip()
        blocs[k] = f'<p class="n"><b>{m.group(1)}.</b>&#160;&#160;{txt}</p>'
    elif bl.startswith("______"):
        nom, courriel = bl.splitlines()[1:3]
        blocs[k] = ('<p class="sig">&#160;</p><p class="ligne">&#160;</p>'
                    '<p class="nom"><b>LOUIS-PHILIPPE DAVID</b><br>Demandeur agissant en son propre nom<br>'
                    f'{courriel.strip()}</p>')
        assert "LOUIS-PHILIPPE DAVID" in nom and "propre nom" in nom
corps = "\n\n".join(blocs)
html_corps = subprocess.run(["pandoc", "-f", "gfm", "-t", "html"], input=corps,
                            capture_output=True, text=True, check=True).stdout

entete = """
<table class="cap"><tr>
<td class="g">CANADA<br><br>PROVINCE DE QUÉBEC<br>DISTRICT DE LONGUEUIL<br><br>
N° : 505-17-016235-261</td>
<td class="d"><b>COUR SUPÉRIEURE</b><br>(Chambre civile)<br><br>
<b>LOUIS-PHILIPPE DAVID</b><br><span class="q">Demandeur</span><br><br>c.<br><br>
<b>ÉLISE MARIE AYOUB</b><br>-et-<br><b>Me MARIE-JOSÉE AYOUB</b><br>
<span class="q">Défenderesses</span></td></tr></table>
<p class="titre">RELEVÉ DES POINTS DE DIVERGENCE<br><span>(art. 152 C.p.c.)</span></p>
"""
css = """
* { font-family: sans-serif; font-size: 10pt; line-height: 1.3; }
p { margin: 0 0 7pt 0; text-align: justify; }
ol { margin: 0 0 7pt 0; padding-left: 18pt; }
li { margin-bottom: 6pt; text-align: justify; }
table { border-collapse: collapse; width: 100%; margin: 4pt 0 10pt 0; }
th, td { border: 0.6pt solid #000; padding: 3pt 4pt; vertical-align: top; font-size: 9pt; text-align: left; }
th { font-weight: bold; }
table.cap td { border: none; font-size: 10.5pt; padding: 0; }
table.cap td.g { width: 45%; font-weight: bold; }
table.cap td.d { width: 55%; padding-left: 12pt; border-left: 0.6pt solid #000; }
span.q { padding-left: 40pt; }
p.titre { text-align: center; font-weight: bold; font-size: 12pt; margin: 10pt 0 10pt 0;
          border-top: 1pt solid #000; border-bottom: 1pt solid #000; padding: 5pt 0; }
p.n { margin: 0 0 7pt 0; }
p.sig { margin: 0; line-height: 1.6; }
p.ligne { width: 45%; border-bottom: 0.6pt solid #000; margin: 0 0 2pt 0; }
p.nom { text-align: left; }
p.titre span { font-weight: normal; font-size: 10.5pt; }
"""
html = f"<html><body>{entete}{html_corps}</body></html>"

LETTRE = fitz.paper_rect("letter")
cadre = LETTRE + (72, 54, -72, -60)
story = fitz.Story(html=html, user_css=css)
w = fitz.DocumentWriter(out)
plus = True
while plus:
    dev = w.begin_page(LETTRE)
    plus, _ = story.place(cadre)
    story.draw(dev)
    w.end_page()
w.close()

doc = fitz.open(out)
n = doc.page_count
for i, page in enumerate(doc):
    page.insert_text((72, LETTRE.height - 40), "N° 505-17-016235-261 — Relevé des points de divergence",
                     fontsize=8, fontname="helv")
    t = f"Page {i + 1} sur {n}"
    page.insert_text((LETTRE.width - 72 - fitz.get_text_length(t, "helv", 8), LETTRE.height - 40),
                     t, fontsize=8, fontname="helv")
doc.set_metadata({"title": "Relevé des points de divergence (art. 152 C.p.c.) — 505-17-016235-261",
                  "author": "Louis-Philippe David"})
doc.save(out + ".tmp", garbage=3, deflate=True)
doc.close()
os.replace(out + ".tmp", out)
print(out, n, "pages")
