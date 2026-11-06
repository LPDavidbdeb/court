"""Index des pièces communiquées, conforme au bordereau déposé le 24 juillet 2026.

Script autonome, comme `extraire_pieces.py` et `rendre_pieces.py` : il ne lit pas
la base. Il lit :

- le **bordereau déposé** (`bordereau_bloc_depot.md`) : cotes, dates et
  descriptions, reproduites sans changement, y compris celles de la table des
  sous-cotes ;
- le `manifeste.json` du dossier des pièces, **pour la liste des fichiers
  seulement**. Ses descriptions viennent de la base et ne concordent pas avec le
  bordereau : elles ne sont pas reprises (`communication_pieces.md` § 17) ;
- les **en-têtes des courriels** (`.eml`), pour la ligne de lecture : date à
  l'heure de Montréal, expéditeur, destinataire, objet.

L'index est aussi la table de lecture des cotes à plusieurs fichiers (§ 15).
Les empreintes ne s'y trouvent pas : elles sont dans `SHA256SUMS`.

Contrôle : chaque description et chaque nom de fichier doivent se retrouver dans
le rendu, dans l'ordre, et chaque caractère de la source doit y figurer.

Usage :
    .venv/bin/python legal/instance/outils/index_pieces.py \\
        --natifs ~/Documents/Pieces_505-17-016235-261_2026-11-06 [--ecrire]

Sans --ecrire, le script rend en mémoire, contrôle, et n'écrit rien. Avec
--ecrire, il écrit `00_Index_des_pieces.pdf` dans le dossier des pièces.
"""
from __future__ import annotations

import argparse
import email
import email.utils
import html
import json
import sys
from email import policy
from pathlib import Path

import fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rendre_pieces as R  # noqa: E402

NOM = "00_Index_des_pieces.pdf"
IMAGES = {".jpg", ".jpeg", ".png"}
CSS = R.CSS + """
p.ic { font-size: 10.5pt; margin: 10pt 0 1pt 0; }
p.id { margin: 0 0 2pt 0; }
p.is { font-size: 9.5pt; margin: 3pt 0 1pt 12pt; }
p.if { font-size: 8.5pt; margin: 0 0 1pt 24pt; color: #333; }
"""


def date_courriel(valeur: str) -> str:
    d = email.utils.parsedate_to_datetime(valeur)
    if d.tzinfo is not None:
        d = d.astimezone(R.MTL)
    jour = f"{d.day}{'er' if d.day == 1 else ''}"
    return f"{jour} {R.MOIS[d.month - 1]} {d.year}, {d.hour} h {d.minute:02d}"


def personnes(valeur: str) -> str:
    return ", ".join((n or a) for n, a in email.utils.getaddresses([valeur]) if n or a)


def ligne_courriel(chemin: Path) -> str:
    msg = email.message_from_bytes(chemin.read_bytes(), policy=policy.default)
    try:
        date = date_courriel(str(msg["Date"]))
    except (TypeError, ValueError):
        date = "date absente des en-têtes"
    de = personnes(str(msg["From"] or "")) or "expéditeur absent des en-têtes"
    a = personnes(str(msg["To"] or "")) or "destinataire absent des en-têtes"
    objet = str(msg["Subject"] or "").strip()
    ligne = f"courriel — {date} — {de} → {a}" + (f" — « {objet} »" if objet else "")
    jointes = [p.get_filename() for p in msg.walk()
               if p.get_filename() and p.get_content_maintype() != "multipart"]
    if jointes:
        ligne += f" — pièce{'s' if len(jointes) > 1 else ''} jointe{'s' if len(jointes) > 1 else ''} : " + ", ".join(jointes)
    return ligne


def lignes_fichiers(e: dict, natifs: Path) -> list[tuple[str, str]]:
    """(nom affiché, nature) pour chaque fichier d'une entrée du manifeste.
    Les images d'un même dossier tiennent sur une ligne."""
    fichiers = e["fichiers"]
    exts = {Path(f["sortie"]).suffix.lower() for f in fichiers}
    if len(fichiers) > 1 and exts <= IMAGES and len({Path(f["sortie"]).parent for f in fichiers}) == 1:
        dossier = Path(fichiers[0]["sortie"]).parent
        return [(f"{dossier}/", f"{len(fichiers)} images ({Path(fichiers[0]['sortie']).name} "
                                f"à {Path(fichiers[-1]['sortie']).name})")]
    out = []
    for f in fichiers:
        chemin = natifs / f["sortie"]
        ext = chemin.suffix.lower()
        if f["modele"] == "email_manager.Email":
            nature = ligne_courriel(chemin)
        elif f["modele"] == "googlechat_manager.ChatSequence":
            nature = f"extrait d'une conversation Google Chat — PDF, {fitz.open(chemin).page_count} p."
        elif ext == ".pdf":
            nature = f"PDF, {fitz.open(chemin).page_count} p."
        elif ext in IMAGES:
            nature = "image"
        else:
            nature = f"fichier {ext or 'sans extension'}"
        if f.get("caviardage"):  # copie masquée : dite, jamais tue (manifeste, « caviardage »)
            nature += f" — {f['caviardage']['mention']}"
        out.append((f["sortie"], nature))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--natifs", required=True, type=Path)
    ap.add_argument("--ecrire", action="store_true")
    a = ap.parse_args()
    natifs = a.natifs.expanduser()
    manifeste = json.loads((natifs / "manifeste.json").read_text(encoding="utf8"))
    racines, sous = R.lire_bordereau(R.BORDEREAU)

    par_racine: dict[str, list[dict]] = {}
    for e in manifeste["cotes"]:
        par_racine.setdefault(e["cote_racine"], []).append(e)

    # blocs de mise en page : une sous-cote avec ses fichiers, ou un fichier ;
    # l'en-tête d'une cote accompagne toujours son premier bloc
    blocs, attendu, source = [], [], []
    nb_fichiers = 0

    def ligne_fichier(nom: str, nature: str) -> str:
        nature_aff, _ = R.hors_bmp(nature)
        attendu.append(nom)
        source.append(nature_aff)
        return f'<p class="if">{html.escape(nom)} — {html.escape(nature_aff)}</p>'

    for racine, (date, desc) in racines.items():
        tete_cote = (f'<p class="ic"><b>{racine}</b>&#160;&#160;{R.gras(date)}</p>'
                     f'<p class="id">{R.gras(desc)}</p>')
        attendu += [racine, desc.replace("**", "")]
        source += [date, desc.replace("**", "")]
        entrees = par_racine.get(racine, [])
        if not entrees:
            sys.exit(f"{racine} : absente du manifeste")
        unites = []
        if all(e["statut"] == "exclue" for e in entrees):
            unites.append('<p class="if">Non communiquée : le demandeur retire cette pièce.</p>')
        else:
            for e in entrees:
                if e["statut"] != "produite":
                    sys.exit(f"{e['cote']} : statut « {e['statut']} » — l'index ne se fait que sur un dossier complet")
                lignes = lignes_fichiers(e, natifs)
                nb_fichiers += len(e["fichiers"])
                if e["cote"] in sous:
                    sd, sdesc = sous[e["cote"]]
                    attendu += [e["cote"], sdesc.replace("**", "")]
                    source += [sd, sdesc.replace("**", "")]
                    unites.append(f'<p class="is"><b>{e["cote"]}</b>&#160;&#160;{R.gras(sd)} — {R.gras(sdesc)}</p>'
                                  + "".join(ligne_fichier(n, x) for n, x in lignes))
                else:
                    unites += [ligne_fichier(n, x) for n, x in lignes]
        unites[0] = tete_cote + unites[0]
        blocs += unites

    tete = (f'{R.ENTETE}<p class="cote" style="font-size:16pt">INDEX DES PIÈCES COMMUNIQUÉES</p>'
            '<p>Pièces au soutien de la demande introductive d\'instance déposée le 24 juillet 2026. '
            'Les cotes, les dates et les descriptions sont celles du bordereau déposé, reproduites sans '
            'changement. Sous chaque cote figurent le ou les fichiers communiqués.</p>'
            # Les photographies sont des dérivés réencodés au versement en base, pas
            # les fichiers de l'appareil : `constat_photos_reencodees.md` ;
            # phrase approuvée par le demandeur le 4 nov. 2026.
            '<p class="petit">Les fichiers sont transmis tels qu\'ils sont conservés, sans conversion ni '
            'réencodage aux fins de la communication. Les photographies conservées sont des fichiers '
            'enregistrés de nouveau lors de leur versement (format JPEG, largeur d\'au plus 1 600 pixels, '
            'qualité 90), leurs métadonnées EXIF étant conservées. '
            'Les empreintes SHA-256 de tous les fichiers figurent dans le fichier SHA256SUMS joint. Pour chaque '
            'courriel, la ligne reprend les en-têtes du fichier : date (heure de Montréal), expéditeur, '
            'destinataire et objet.</p>')
    doc = R.pdf_par_blocs([tete] + blocs, CSS)

    # contrôle : tout ce qui est attendu figure dans le rendu, dans l'ordre
    # sans aucun blanc : une coupure de ligne après « / » ne doit pas compter comme écart
    plat = lambda t: "".join(t.split())  # noqa: E731
    rendu, pos, anomalies = plat(R.texte_pdf(doc)), 0, []
    for x in attendu:
        i = rendu.find(plat(x), pos)
        if i < 0:
            anomalies.append(f"absent ou hors d'ordre dans le rendu : {x[:80]}")
        else:
            pos = i
    anomalies += R.controle_caracteres(" ".join(source), doc)

    n = doc.page_count
    for i, page in enumerate(doc):
        t = f"N° {R.DOSSIER} - Index des pièces - page {i + 1} de {n}"
        page.insert_text((R.LETTRE.width - 54 - fitz.get_text_length(t, "helv", 7.5), R.LETTRE.height - 28),
                         t, fontsize=7.5, fontname="helv")
    doc.set_metadata({"title": f"Index des pièces — dossier {R.DOSSIER}", "author": "Louis-Philippe David"})

    print(f"{len(racines)} cotes, {len(sous)} sous-cotes du bordereau, {nb_fichiers} fichiers, {n} pages")
    for x in anomalies:
        print("  ⚠", x)
    print(f"{len(anomalies)} anomalie(s)")
    if a.ecrire and not anomalies:
        (natifs / NOM).write_bytes(doc.tobytes(garbage=3, deflate=True))
        print(f"écrit : {natifs / NOM}")
    elif a.ecrire:
        sys.exit("rien écrit : anomalies")


if __name__ == "__main__":
    main()
