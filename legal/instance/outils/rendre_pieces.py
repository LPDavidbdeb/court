"""Rendus lisibles des pièces, sous la numérotation de juillet (ancien régime).

Script autonome (cadre retenu par LP le 29 oct. 2026, comme l'extraction) : il ne
lit pas la base et ne modifie rien. Il lit :

- le dossier des **natifs** produit par `extraire_pieces.py`, et son
  `manifeste.json` ;
- le **bordereau déposé** (`bordereau_bloc_depot.md`), pour la date et la
  description de chaque cote et de chaque sous-cote ;
- pour P-58 à P-64 seulement, qui n'ont pas de natif, le **corps** des
  transcriptions assemblées le 27 juillet (`pieces_pdf/`). Leur page de garde,
  défectueuse, n'est pas reprise.

Il écrit un PDF par cote, un index et un manifeste dans un dossier de sortie
neuf. Le rendu sert la lecture, et **le natif fait foi**.

Contrôle des caractères : chaque courriel est rendu dans son propre document,
puis relu. Tout caractère du courriel source doit se retrouver dans le texte
du rendu, et le nombre de « ? » doit être le même. Les caractères hors du plan
multilingue de base (émojis) sont remplacés par le marqueur visible
`[U+XXXX]`, et chaque remplacement est consigné au manifeste.

Usage :
    .venv/bin/python legal/instance/outils/rendre_pieces.py \\
        --natifs ~/Documents/Pieces_505-17-016235-261_2026-11-06 \\
        --sortie ~/Documents/Rendus_505-17-016235-261_2026-11-06 [--ecrire] [--cotes P-10,P-43]

Sans --ecrire, le script rend en mémoire, contrôle, et n'écrit rien.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import email
import hashlib
import html
import io
import json
import re
import sys
import unicodedata
from email import policy
from pathlib import Path

import fitz
from bs4 import BeautifulSoup
from PIL import Image, ImageOps

RACINE = Path(__file__).resolve().parents[3]
BORDEREAU = RACINE / "legal/depots/2026-07-24_initial/candidats/bordereau_bloc_depot.md"
JUILLET = RACINE / "pieces_pdf"
DOSSIER = "505-17-016235-261"
LETTRE = fitz.paper_rect("letter")
CADRE = LETTRE + (54, 54, -54, -54)
SANS_NATIF = {f"P-{n}" for n in range(58, 65)}

CSS = """
* { font-family: sans-serif; font-size: 10pt; line-height: 1.3; }
p { margin: 0 0 6pt 0; }
table { border-collapse: collapse; width: 100%; }
td { vertical-align: top; padding: 2pt 4pt; }
table.hdr td { border-bottom: 0.4pt solid #999; font-size: 9.5pt; }
table.hdr td.k { width: 14%; font-weight: bold; }
div.corps { margin-top: 10pt; font-size: 10pt; }
p.pj { margin-top: 10pt; font-size: 9pt; }
p.sous { font-weight: bold; font-size: 11pt; margin-bottom: 8pt; }
table.cap td { font-size: 10.5pt; padding: 0; }
table.cap td.g { width: 45%; font-weight: bold; }
table.cap td.d { width: 55%; padding-left: 12pt; border-left: 0.6pt solid #000; }
p.cote { font-size: 22pt; font-weight: bold; margin: 26pt 0 6pt 0; }
p.date { font-size: 12pt; margin-bottom: 12pt; }
p.desc { font-size: 12pt; }
p.petit { font-size: 8.5pt; color: #333; }
table.nat td { font-size: 8pt; border-bottom: 0.3pt solid #bbb; }
table.idx td { font-size: 8.5pt; border-bottom: 0.3pt solid #bbb; }
table.idx td.c { width: 9%; font-weight: bold; }
table.idx td.d { width: 16%; }
"""


# --- utilitaires -----------------------------------------------------------

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def gras(texte: str) -> str:
    """Échappe le texte, puis rend les ** du bordereau en gras."""
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(texte))


def hors_bmp(texte: str) -> tuple[str, list[str]]:
    """Remplace chaque caractère hors du plan de base par un marqueur visible."""
    remplaces = []

    def sub(m):
        code = f"U+{ord(m.group(0)):04X}"
        remplaces.append(code)
        return f"[{code}]"

    return re.sub(r"[\U00010000-\U0010FFFF]", sub, texte), remplaces


def story_pdf(corps_html: str) -> fitz.Document:
    tampon = io.BytesIO()
    story = fitz.Story(html=f"<html><body>{corps_html}</body></html>", user_css=CSS)
    w = fitz.DocumentWriter(tampon)
    plus = True
    while plus:
        dev = w.begin_page(LETTRE)
        plus, _ = story.place(CADRE)
        story.draw(dev)
        w.end_page()
    w.close()
    return fitz.open("pdf", tampon.getvalue())


def texte_pdf(doc: fitz.Document) -> str:
    return "".join(p.get_text() for p in doc)


def controle_caracteres(source: str, doc: fitz.Document) -> list[str]:
    """Retourne la liste des anomalies : caractères absents, « ? » en surnombre."""
    rendu = texte_pdf(doc)
    anomalies = []
    manquants = sorted({c for c in source if not c.isspace() and c not in rendu
                        and unicodedata.category(c) != "Cf"})
    if manquants:
        anomalies.append("caractères absents du rendu : " + " ".join(
            f"{c!r}(U+{ord(c):04X})" for c in manquants))
    if rendu.count("?") != source.count("?"):
        anomalies.append(f"« ? » : {source.count('?')} dans la source, {rendu.count('?')} dans le rendu")
    if "�" in rendu and "�" not in source:
        anomalies.append("caractère de remplacement U+FFFD dans le rendu")
    return anomalies


# --- bordereau déposé ------------------------------------------------------

def lire_bordereau(chemin: Path) -> tuple[dict, dict]:
    racines, sous = {}, {}
    for ligne in chemin.read_text(encoding="utf8").splitlines():
        m = re.match(r"^- \*\*(P-\d+)\*\* — (.*?)\s*[;.]?\s*$", ligne)
        if m:
            date, _, desc = m.group(2).partition(" — ")
            racines[m.group(1)] = (date.strip(), desc.strip())
            continue
        m = re.match(r"^\| (P-\d+\.\d+) \| ([^|]*) \| [^|]* \| (.*) \|\s*$", ligne)
        if m:
            sous[m.group(1)] = (m.group(2).strip(), m.group(3).strip())
    return racines, sous


# --- courriels -------------------------------------------------------------

def decoder(octets: bytes, jeu: str | None) -> tuple[str, bool]:
    """Décode selon le jeu déclaré ; les octets qui n'y sont pas conformes
    (courriel déclaré UTF-8 mais écrit en partie en Latin-1, par exemple)
    sont lus en Windows-1252 plutôt que remplacés par U+FFFD."""
    jeu = jeu or "utf-8"
    try:
        return octets.decode(jeu), False
    except LookupError:
        jeu = "utf-8"
    except UnicodeDecodeError:
        pass
    try:
        return octets.decode(jeu), False
    except UnicodeDecodeError:
        brut = octets.decode(jeu, errors="surrogateescape")
        return re.sub(r"[\udc80-\udcff]+",
                      lambda m: bytes(ord(c) - 0xDC00 for c in m.group(0)).decode("cp1252", errors="replace"),
                      brut), True


def lire_courriel(donnees: bytes):
    if donnees.startswith(b"From "):  # ligne d'enveloppe mbox
        donnees = donnees.split(b"\n", 1)[1]
    msg = email.message_from_bytes(donnees, policy=policy.default)
    entetes = []
    for cle, nom in (("From", "De"), ("To", "À"), ("Cc", "Cc"), ("Date", "Date"), ("Subject", "Objet")):
        valeur = msg.get(cle)
        if valeur is not None:
            entetes.append((nom, str(valeur)))
    corps, nature = "", "aucun corps texte"
    partie = msg.get_body(preferencelist=("plain", "html"))
    if partie is not None:
        contenu, mixte = decoder(partie.get_payload(decode=True) or b"", partie.get_content_charset())
        if partie.get_content_subtype() == "html":
            contenu = BeautifulSoup(contenu, "html.parser").get_text("\n")
            nature = "corps HTML converti en texte"
        else:
            nature = "corps texte"
        if mixte:
            nature += " ; octets non conformes au jeu déclaré lus en Windows-1252"
        corps = re.sub(r"\n{3,}", "\n\n", contenu.replace("\r\n", "\n")).strip()
    pieces_jointes = []
    for pj in msg.iter_attachments():
        charge = pj.get_payload(decode=True) or b""
        pieces_jointes.append({
            "nom": pj.get_filename() or "(sans nom)",
            "type": pj.get_content_type(),
            "octets": len(charge),
            "sha256": sha256(charge),
            "donnees": charge,
        })
    return entetes, corps, nature, pieces_jointes


def rendre_courriel(chemin: Path, titre: str | None):
    entetes, corps, nature, pjs = lire_courriel(chemin.read_bytes())
    entetes = [(k, hors_bmp(v)) for k, v in entetes]
    corps, rempl_corps = hors_bmp(corps)
    remplaces = [c for _, (_, r) in entetes for c in r] + rempl_corps
    lignes = "".join(
        f'<tr><td class="k">{html.escape(k)}</td><td>{html.escape(v)}</td></tr>'
        for k, (v, _) in entetes)
    corps_html = html.escape(corps).replace("\n", "<br/>")
    pj_html = ""
    if pjs:
        items = "<br/>".join(
            f"{html.escape(hors_bmp(p['nom'])[0])} — {p['type']}, {p['octets']} octets, SHA-256 {p['sha256']}"
            for p in pjs)
        pj_html = f'<p class="pj"><b>Pièces jointes au courriel</b> (contenues dans le fichier natif) :<br/>{items}</p>'
    tete = f'<p class="sous">{gras(titre)}</p>' if titre else ""
    doc = story_pdf(
        f'{tete}<p class="petit">Fichier natif : {html.escape(chemin.name)} — {nature}</p>'
        f'<table class="hdr">{lignes}</table><div class="corps">{corps_html}</div>{pj_html}')
    source = (" ".join(v for _, (v, _) in entetes) + corps
              + "".join(hors_bmp(p["nom"])[0] for p in pjs))
    anomalies = controle_caracteres(source, doc)
    invisibles = sorted({f"U+{ord(c):04X}" for c in source if unicodedata.category(c) == "Cf"})
    # pièces jointes lisibles : PDF et images, à la suite du courriel
    for p in pjs:
        try:
            if p["type"] == "application/pdf":
                doc.insert_pdf(fitz.open("pdf", p["donnees"]))
            elif p["type"].startswith("image/"):
                page_image(doc, p["donnees"], f"Pièce jointe : {p['nom']}")
        except Exception as exc:  # une pièce jointe illisible ne bloque pas le rendu
            anomalies.append(f"pièce jointe non rendue ({p['nom']}) : {exc}")
    return doc, anomalies, remplaces, invisibles


# --- images ----------------------------------------------------------------

def jpeg_reduit(donnees: bytes, cote_max: int) -> bytes:
    im = ImageOps.exif_transpose(Image.open(io.BytesIO(donnees))).convert("RGB")
    im.thumbnail((cote_max, cote_max))
    out = io.BytesIO()
    im.save(out, "JPEG", quality=85)
    return out.getvalue()


def page_image(doc: fitz.Document, donnees: bytes, legende: str, cote_max: int = 2000):
    page = doc.new_page(width=LETTRE.width, height=LETTRE.height)
    zone = fitz.Rect(CADRE.x0, CADRE.y0, CADRE.x1, CADRE.y1 - 40)
    page.insert_image(zone, stream=jpeg_reduit(donnees, cote_max), keep_proportion=True)
    page.insert_htmlbox(fitz.Rect(CADRE.x0, CADRE.y1 - 34, CADRE.x1, CADRE.y1),
                        f'<p style="font-size:8.5pt">{html.escape(legende)}</p>')


def planche(doc: fitz.Document, photos: list[tuple[bytes, str]]):
    """Planche de quatre photos par page, avec légende ; le natif reste la pièce."""
    for i in range(0, len(photos), 4):
        page = doc.new_page(width=LETTRE.width, height=LETTRE.height)
        l = (CADRE.width - 12) / 2
        h = (CADRE.height - 12) / 2
        for k, (donnees, legende) in enumerate(photos[i:i + 4]):
            x = CADRE.x0 + (k % 2) * (l + 12)
            y = CADRE.y0 + (k // 2) * (h + 12)
            page.insert_image(fitz.Rect(x, y, x + l, y + h - 30),
                              stream=jpeg_reduit(donnees, 1000), keep_proportion=True)
            page.insert_htmlbox(fitz.Rect(x, y + h - 28, x + l, y + h),
                                f'<p style="font-size:7.5pt">{html.escape(legende)}</p>')


SEUIL_ALLEGEMENT = 5_000_000  # octets


def inserer_pdf_allege(doc: fitz.Document, source: fitz.Document):
    """Copie de lecture d'un PDF lourd : les pages sans texte (numérisations)
    sont rastérisées à 150 ppp ; les pages qui portent du texte sont reprises
    telles quelles. Le natif garde sa pleine résolution."""
    for i, page in enumerate(source):
        if page.get_text().strip():
            doc.insert_pdf(source, from_page=i, to_page=i)
            continue
        pix = page.get_pixmap(dpi=150)
        neuve = doc.new_page(width=page.rect.width, height=page.rect.height)
        neuve.insert_image(neuve.rect, stream=pix.tobytes("jpeg", jpg_quality=80))


def date_exif(fichier: dict) -> str:
    m = re.search(r"DateTimeOriginal = ([0-9: ]+)", fichier.get("exif") or "")
    return f"EXIF DateTimeOriginal : {m.group(1).strip()}" if m else "aucune date EXIF"


# --- page de garde et index ------------------------------------------------

ENTETE = f"""<table class="cap"><tr>
<td class="g">CANADA<br/>PROVINCE DE QUÉBEC<br/>DISTRICT DE LONGUEUIL<br/><br/>N° : {DOSSIER}</td>
<td class="d"><b>COUR SUPÉRIEURE</b> (Chambre civile)<br/><br/><b>LOUIS-PHILIPPE DAVID</b>, demandeur<br/>c.<br/>
<b>ÉLISE MARIE AYOUB</b> et <b>Me MARIE-JOSÉE AYOUB</b>, défenderesses</td></tr></table>"""


def page_de_garde(cote: str, date: str, desc: str, natifs: list[tuple[str, str]], note: str):
    lignes = "".join(f"<tr><td>{html.escape(n)}</td><td>{s}</td></tr>" for n, s in natifs)
    tableau = (f'<p class="petit"><b>Fichiers natifs communiqués</b> (ils font foi) :</p>'
               f'<table class="nat">{lignes}</table>') if natifs else ""
    return story_pdf(
        f'{ENTETE}<p class="cote">PIÈCE {cote}</p><p class="date">{gras(date)}</p>'
        f'<p class="desc">{gras(desc)}</p><p>&#160;</p>{tableau}<p>&#160;</p>'
        f'<p class="petit">{html.escape(note)}</p>')


def pieds_de_page(doc: fitz.Document, cote: str):
    n = doc.page_count
    for i, page in enumerate(doc):
        t = f"N° {DOSSIER} - Pièce {cote} - page {i + 1} de {n}"
        page.insert_text((LETTRE.width - 54 - fitz.get_text_length(t, "helv", 7.5), LETTRE.height - 28),
                         t, fontsize=7.5, fontname="helv")


# --- programme -------------------------------------------------------------

def cle_cote(c: str):
    return [int(x) for x in re.findall(r"\d+", c)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--natifs", required=True, type=Path)
    ap.add_argument("--sortie", required=True, type=Path)
    ap.add_argument("--cotes", default="")
    ap.add_argument("--ecrire", action="store_true")
    a = ap.parse_args()

    natifs = a.natifs.expanduser()
    sortie = a.sortie.expanduser()
    manifeste = json.loads((natifs / "manifeste.json").read_text(encoding="utf8"))
    racines, sous = lire_bordereau(BORDEREAU)
    choix = {c.strip() for c in a.cotes.split(",") if c.strip()}

    if a.ecrire:
        if sortie.exists() and any(sortie.iterdir()):
            sys.exit(f"Le dossier de sortie doit être absent ou vide : {sortie}")
        sortie.mkdir(parents=True, exist_ok=True)

    groupes = collections.OrderedDict()
    for e in manifeste["cotes"]:
        if e["statut"] == "exclue":
            continue
        groupes.setdefault(e["cote_racine"], []).append(e)

    horodatage = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    resultat = {"schema": "rendus-pieces/1", "dossier": DOSSIER, "produit_le": horodatage,
                "natifs": str(natifs), "bordereau": str(BORDEREAU.relative_to(RACINE)),
                "cotes": []}
    total_anomalies = 0

    for racine in sorted(groupes, key=cle_cote):
        if choix and racine not in choix:
            continue
        lignes = groupes[racine]
        date, desc = racines.get(racine, ("", lignes[0]["description"]))
        doc = fitz.open()
        anomalies, remplaces, sources, invisibles, alleges = [], [], [], [], []
        plusieurs = len(lignes) > 1

        if racine in SANS_NATIF:
            juillet = JUILLET / f"{racine}.pdf"
            donnees = juillet.read_bytes()
            corps = fitz.open("pdf", donnees)
            doc.insert_pdf(corps, from_page=1)
            sources.append({"fichier": f"pieces_pdf/{racine}.pdf", "pages_reprises": f"2-{corps.page_count}",
                            "sha256": sha256(donnees)})
            note = ("Transcription intégrale de la séquence de messages, en ordre chronologique, avec son annexe "
                    "d'identifiants et d'horodatages d'origine. Cette pièce n'a pas d'autre fichier natif. "
                    "Corps repris de l'assemblage du 27 juillet 2026 ; page de garde refaite.")
            natifs_garde = []
        else:
            note = ("Rendu lisible produit à partir des fichiers natifs ci-dessus par "
                    "legal/instance/outils/rendre_pieces.py. En cas de divergence, le fichier natif fait foi.")
            natifs_garde = []
            for e in lignes:
                titre = None
                if plusieurs:
                    sd, sdesc = sous.get(e["cote"], ("", ""))
                    titre = " — ".join(x for x in (e["cote"], sd, sdesc) if x)
                photos = []
                for f in e["fichiers"]:
                    chemin = natifs / f["sortie"]
                    natifs_garde.append((f["sortie"], f["sha256_copie"]))
                    sources.append({"fichier": f["sortie"], "sha256": f["sha256_copie"]})
                    ext = chemin.suffix.lower()
                    if ext == ".eml" or (ext == "" and f["modele"] == "email_manager.Email"):
                        d, an, rp, inv = rendre_courriel(chemin, titre)
                        titre = None
                        doc.insert_pdf(d)
                        anomalies += [f"{f['sortie']} : {x}" for x in an]
                        remplaces += rp
                        if inv:
                            invisibles.append(f"{f['sortie']} : {' '.join(inv)}")
                    elif ext == ".pdf":
                        if titre:
                            doc.insert_pdf(story_pdf(f'<p class="sous">{gras(titre)}</p>'))
                            titre = None
                        if chemin.stat().st_size > SEUIL_ALLEGEMENT:
                            inserer_pdf_allege(doc, fitz.open(chemin))
                            alleges.append(f["sortie"])
                        else:
                            doc.insert_pdf(fitz.open(chemin))
                    elif ext in (".jpg", ".jpeg", ".png"):
                        leg = f"{(titre + ' — ') if titre else ''}{f['sortie']} — {date_exif(f)}"
                        photos.append((chemin.read_bytes(), leg))
                    else:
                        anomalies.append(f"{f['sortie']} : format non rendu ({ext or 'sans extension'})")
                if photos:
                    if e["objet"].startswith("events.event"):
                        planche(doc, photos)
                    else:
                        for donnees, leg in photos:
                            page_image(doc, donnees, leg)

        if alleges:
            note += (" Copie de lecture allégée (pages numérisées rendues à 150 ppp) pour : "
                     + ", ".join(alleges) + ".")
        garde = page_de_garde(racine, date, desc, natifs_garde, note)
        an_garde = controle_caracteres(" ".join((date, desc)).replace("**", ""), garde)
        anomalies += [f"page de garde : {x}" for x in an_garde]
        doc.insert_pdf(garde, start_at=0)
        pieds_de_page(doc, racine)
        doc.set_metadata({"title": f"Pièce {racine} — dossier {DOSSIER}", "author": "Louis-Philippe David"})
        octets = doc.tobytes(garbage=3, deflate=True)
        if a.ecrire:
            (sortie / f"{racine}.pdf").write_bytes(octets)
        total_anomalies += len(anomalies)
        resultat["cotes"].append({"cote": racine, "date": date, "description": desc,
                                  "rendu": f"{racine}.pdf", "pages": doc.page_count,
                                  "sha256": sha256(octets), "octets": len(octets),
                                  "sources": sources, "anomalies": anomalies,
                                  "marqueurs_hors_bmp": remplaces,
                                  "invisibles_non_reproduits": invisibles,
                                  "pdf_alleges_150ppp": alleges})
        print(f"{racine:7} {doc.page_count:4} p  {len(octets) / 1e6:6.1f} Mo  "
              f"anomalies {len(anomalies)}  marqueurs {len(remplaces)}")
        for x in anomalies:
            print("        ⚠", x)

    # index
    lignes_idx = "".join(
        f'<tr><td class="c">{c["cote"]}</td><td class="d">{gras(c["date"])}</td>'
        f'<td>{gras(c["description"])}</td><td>{c["pages"]} p.</td></tr>'
        for c in resultat["cotes"])
    index = story_pdf(
        f'{ENTETE}<p class="cote" style="font-size:16pt">INDEX DES PIÈCES COMMUNIQUÉES</p>'
        f'<p>Pièces au soutien de la demande introductive d\'instance déposée le 24 juillet 2026, '
        f'sous la numérotation du bordereau déposé. P-86 n\'est pas communiquée.</p>'
        f'<p class="petit">Chaque pièce est livrée deux fois : le <b>fichier natif</b> (dossier « natifs », '
        f'avec ses empreintes SHA-256), qui fait foi, et un <b>rendu lisible</b> en PDF (dossier « rendus »). '
        f'Les photographies conservent leurs métadonnées EXIF ; les courriels, leurs en-têtes.</p>'
        f'<table class="idx">{lignes_idx}</table>')
    pieds_de_page(index, "index")
    resultat["total_anomalies"] = total_anomalies
    if a.ecrire:
        (sortie / "00_Index_des_pieces.pdf").write_bytes(index.tobytes(garbage=3, deflate=True))
        (sortie / "manifeste_rendus.json").write_text(json.dumps(resultat, ensure_ascii=False, indent=1),
                                                      encoding="utf8")
        sommes = [f"{c['sha256']}  {c['rendu']}" for c in resultat["cotes"]]
        (sortie / "SHA256SUMS").write_text("\n".join(sommes) + "\n", encoding="utf8")
    print(f"\n{len(resultat['cotes'])} cotes rendues ; {total_anomalies} anomalie(s) ; "
          f"{'écrit dans ' + str(sortie) if a.ecrire else 'rien écrit (sans --ecrire)'}")


if __name__ == "__main__":
    main()
