#!/usr/bin/env python
"""Extraire les pièces cotées au dépôt du 24 juillet 2026 vers un dossier de livraison.

    .venv/bin/python legal/instance/outils/extraire_pieces.py --sortie ~/Documents/Pieces_2026-11-06
    .venv/bin/python legal/instance/outils/extraire_pieces.py --sortie ... --cote P-43 --cote P-2
    .venv/bin/python legal/instance/outils/extraire_pieces.py --sortie ... --ecrire

POURQUOI CE SCRIPT EXISTE. Le protocole notifié le 29 octobre engage le
demandeur à communiquer ses pièces au plus tard le 6 novembre 2026 (rubrique
36). Les lettres du 16 octobre ont promis une transmission « dans leur format
électronique, sans conversion ni réencodage », avec un index et les empreintes
SHA-256. Ce script produit exactement cela, et rien d'autre.

CE QU'IL ÉVITE — chaque règle vient d'une erreur déjà faite ou d'un piège
déjà repéré dans ce dossier (spécification : `../prompt_agent_extraction_pieces.md`) :

  • Copier des octets, jamais réenregistrer. Aucune image n'est ouverte par
    PIL : réenregistrer détruit l'EXIF, et l'EXIF date la photographie.
  • Prouver la fidélité : SHA-256 de la SOURCE et de la COPIE, tailles égales.
    Hacher la seule sortie ne prouverait rien.
  • Résoudre chaque ligne en direct (`content_object`). Le champ `resolu` est
    un constat d'import : P-86 le portait alors que son objet avait disparu.
  • Ne jamais inventer une cote. Une ligne du bordereau = une cote = une entrée.
    Les sous-cotes (P-43.7) viennent de la table, dans l'ordre du bordereau
    gelé (vérifié le 29 oct. : `README_extraction_pieces.md`).
  • Une cote n'est « produite » que si TOUS ses fichiers sont copiés et
    vérifiés. Jamais de livraison partielle d'une liasse.
  • Les photographies en base sont des DÉRIVÉS (≤ 1600 px, JPEG q90, EXIF
    réinjecté), pas les originaux : le manifeste le dit, fichier par fichier.

SANS `--ecrire`, le script ne crée ni ne modifie RIEN : il bâtit le plan,
hache les sources et rapporte.

Outil autonome de l'instance (décision de LP du 29 oct. 2026) : il lit la base
sans la modifier et n'écrit que dans le dossier de sortie.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django  # noqa: E402

django.setup()

import exifread  # noqa: E402
from django.conf import settings  # noqa: E402

from case_manager.models import BordereauDepotJuillet  # noqa: E402

SCHEMA = "extraction-pieces/1"
DOSSIER = "505-17-016235-261"

EXCLUSIONS = {
    "P-86": (
        "Retirée du bordereau amendé — décision du 26 octobre 2026, consignée à "
        "legal/amendements/01_avant_notification/journal_modifications.md, rubrique "
        "« 26 octobre 2026 — Retrait de P-86 du bordereau amendé ». Son objet "
        "n'existe plus et elle n'appuyait aucun paragraphe. La ligne de la table "
        "est conservée telle quelle."
    ),
}

QUALIF_PHOTO = (
    "photographie en base : dérivé produit par PhotoProcessingService "
    "(largeur ≤ 1600 px, JPEG qualité 90, EXIF réinjecté), et non le fichier "
    "d'origine — voir legal/instance/constat_photos_reencodees.md"
)
QUALIF_NATIF = "fichier tel que conservé en base"

EXT_EXIF = {".jpg", ".jpeg", ".tif", ".tiff", ".heic", ".png", ".webp"}
MOTIF_COTE = re.compile(r"^P-\d+(\.\d+)?$")

# Répertoires où le script ne doit jamais écrire.
INTERDITS = [RACINE / "legal" / "depots", Path(settings.MEDIA_ROOT), RACINE / "storage"]


class Echec(Exception):
    """La cote ne peut pas être produite. Le motif est rapporté, rien n'est réparé."""


class ARendre(Exception):
    """Rendu volontairement différé (transcription de ChatSequence)."""


# ---------------------------------------------------------------------------
def sha256(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def exif(chemin):
    """Lecture seule, par la méthode du projet (process_photos.py)."""
    with open(chemin, "rb") as f:
        tags = exifread.process_file(f, details=False)
    return {k: str(v) for k, v in tags.items()}


def chemin_local(valeur):
    if not valeur:
        return None
    p = Path(valeur)
    return p if p.is_absolute() else RACINE / p


def source(fieldfile, secours, champ, champ_secours):
    """Choisit la source sans la transformer : le FileField d'abord, le chemin
    en repli. Deux sources accessibles et différentes = ambiguïté = échec."""
    principal = None
    if fieldfile and getattr(fieldfile, "name", ""):
        try:
            p = Path(fieldfile.path)
            if p.is_file():
                principal = p
        except (NotImplementedError, ValueError):
            principal = None
    repli = chemin_local(secours)
    repli = repli if repli and repli.is_file() else None

    if principal and repli and principal.resolve() != repli.resolve():
        if sha256(principal) != sha256(repli):
            raise Echec(f"ambiguïté : {champ} et {champ_secours} existent et diffèrent")
    if principal:
        return {"chemin": principal, "champ": champ, "repli": None}
    if repli:
        return {"chemin": repli, "champ": champ_secours,
                "repli": f"{champ} vide ou inaccessible"}
    raise Echec(f"original absent : ni {champ} ni {champ_secours} ne résolvent")


def cle_photo(photo):
    d = photo.datetime_original
    return (d is None, d.isoformat() if d else "", photo.pk)


def cle_courriel(email):
    d = email.date_sent
    return (d is None, d.isoformat() if d else "", email.pk)


def membre_photo(photo):
    s = source(photo.file, photo.file_path, "file", "file_path")
    return {"modele": "photos.Photo", "pk": photo.pk, "qualification": QUALIF_PHOTO, **s}


def membre_courriel(email):
    s = source(email.eml_file, email.eml_file_path, "eml_file", "eml_file_path")
    return {"modele": "email_manager.Email", "pk": email.pk, "qualification": QUALIF_NATIF, **s}


def membres(obj, modele):
    """Les fichiers d'une ligne, dans un ordre total et reproductible."""
    if modele == "chatsequence":
        raise ARendre("transcription de la séquence à produire séparément")
    if modele in ("event", "photodocument"):
        rel = obj.linked_photos if modele == "event" else obj.photos
        photos = sorted(rel.all(), key=cle_photo)
        if not photos:
            raise Echec("conteneur photographique vide")
        return [membre_photo(p) for p in photos]
    if modele == "photo":
        return [membre_photo(obj)]
    if modele == "email":
        return [membre_courriel(obj)]
    if modele == "emailthread":
        courriels = sorted(obj.emails.all(), key=cle_courriel)
        if not courriels:
            raise Echec("fil sans courriel")
        return [membre_courriel(e) for e in courriels]
    if modele == "pdfdocument":
        s = source(obj.file, None, "file", "—")
        return [{"modele": "pdf_manager.PDFDocument", "pk": obj.pk,
                 "qualification": QUALIF_NATIF, **s}]
    if modele == "document":
        s = source(obj.file_source, None, "file_source", "—")
        return [{"modele": "document_manager.Document", "pk": obj.pk,
                 "qualification": QUALIF_NATIF, **s}]
    raise Echec(f"modèle non pris en charge : {modele}")


# ---------------------------------------------------------------------------
def selection(cotes_demandees):
    base = BordereauDepotJuillet.objects.exclude(cote__isnull=True)
    if not cotes_demandees:
        lignes = list(base)
    else:
        mal = [c for c in cotes_demandees if not MOTIF_COTE.match(c)]
        if mal:
            raise SystemExit(f"Cote mal formée : {', '.join(mal)}")
        lignes, vues = [], set()
        for c in cotes_demandees:
            qs = base.filter(cote=c) if "." in c else base.filter(cote_racine=c)
            trouvees = list(qs)
            if not trouvees:
                raise SystemExit(f"Cote inconnue ou non déposée en juillet : {c}")
            for r in trouvees:
                if r.pk not in vues:
                    vues.add(r.pk)
                    lignes.append(r)
    lignes.sort(key=lambda r: (r.rang or 0, r.sous_rang is not None, r.sous_rang or 0, r.pk))
    return lignes


def verifier_sortie(sortie, ecrire):
    s = sortie.resolve()
    for interdit in INTERDITS:
        i = interdit.resolve()
        if s == i or i in s.parents:
            raise SystemExit(f"Dossier de sortie interdit (source ou archive) : {s}")
    if ecrire and s.exists() and any(s.iterdir()):
        raise SystemExit(
            f"Le dossier de sortie n'est pas vide : {s}\n"
            "Une première extraction se fait dans un dossier absent ou vide. "
            "Rien n'a été écrit.")


def nommer(cote, plan):
    if len(plan) == 1:
        return [f"{cote}{Path(plan[0]['chemin'].name).suffix}"]
    return [f"{cote}/{cote}-{i:02d}{Path(m['chemin'].name).suffix}"
            for i, m in enumerate(plan, 1)]


def copier_cote(cote, plan, noms, sortie):
    """Copie dans un espace temporaire, vérifie tout, puis publie d'un bloc."""
    tmp = sortie / ".en_cours" / cote
    tmp.mkdir(parents=True, exist_ok=False)
    try:
        for m, nom in zip(plan, noms):
            dest = tmp / Path(nom).name
            shutil.copy2(m["chemin"], dest)
            m["octets_copie"] = dest.stat().st_size
            m["sha256_copie"] = sha256(dest)
            if m["sha256_copie"] != m["sha256_source"] or m["octets_copie"] != m["octets_source"]:
                raise Echec(f"copie infidèle : {nom}")
            if Path(nom).suffix.lower() in EXT_EXIF:
                try:
                    a, b = exif(m["chemin"]), exif(dest)
                except Exception as err:  # format lu par exifread ou non
                    m["exif"] = f"contrôle EXIF non disponible ({err!r}) ; l'égalité des empreintes couvre le fichier"
                    continue
                if a != b:
                    raise Echec(f"EXIF différent entre source et copie : {nom}")
                m["exif"] = ("identique ; DateTimeOriginal = " + a["EXIF DateTimeOriginal"]
                             if "EXIF DateTimeOriginal" in a else
                             "identique ; aucun EXIF ni dans la source ni dans la copie"
                             if not a else "identique ; sans DateTimeOriginal")
            else:
                m["exif"] = "sans objet pour ce format ; l'égalité des empreintes couvre le fichier"
        if len(noms) == 1:
            os.replace(tmp / Path(noms[0]).name, sortie / noms[0])
            tmp.rmdir()
        else:
            os.replace(tmp, sortie / cote)
    except Exception:
        shutil.rmtree(tmp, ignore_errors=True)
        raise
    finally:
        try:
            (sortie / ".en_cours").rmdir()
        except OSError:
            pass


# ---------------------------------------------------------------------------
def traiter(lignes, sortie, ecrire):
    resultats = []
    for r in lignes:
        entree = {"cote": r.cote, "cote_racine": r.cote_racine,
                  "objet": f"{r.content_type.app_label}.{r.content_type.model}:{r.object_id}",
                  "description": r.description, "fichiers": []}
        resultats.append(entree)
        if r.cote in EXCLUSIONS:
            entree.update(statut="exclue", motif=EXCLUSIONS[r.cote])
            continue
        try:
            obj = r.content_object
            if obj is None:
                raise Echec("objet introuvable : la ligne ne se résout plus")
            plan = membres(obj, r.content_type.model)
            noms = nommer(r.cote, plan)
            for i, (m, nom) in enumerate(zip(plan, noms), 1):
                m["rang_interne"] = i
                m["nom_source"] = m["chemin"].name
                m["sortie"] = nom
                m["octets_source"] = m["chemin"].stat().st_size
                m["sha256_source"] = sha256(m["chemin"])
            if ecrire:
                copier_cote(r.cote, plan, noms, sortie)
                entree["statut"] = "produite"
            else:
                for m in plan:
                    m["octets_copie"] = m["sha256_copie"] = None
                    m["exif"] = "non vérifié (simulation)"
                entree["statut"] = "prévue"
            entree["fichiers"] = [{k: (str(v) if isinstance(v, Path) else v)
                                   for k, v in m.items()} for m in plan]
        except ARendre as e:
            entree.update(statut="à rendre", motif=str(e))
        except Echec as e:
            entree.update(statut="échec", motif=str(e))
        except Exception as e:  # une ligne en échec n'arrête pas les autres
            entree.update(statut="échec", motif=f"erreur inattendue : {e!r}")
    return resultats


def decomptes(resultats):
    n = lambda s: sum(1 for e in resultats if e["statut"] == s)  # noqa: E731
    d = {"sélectionnées": len(resultats), "exclues": n("exclue"),
         "produites": n("produite"), "prévues": n("prévue"),
         "à rendre": n("à rendre"), "en échec": n("échec")}
    d["attendues"] = d["sélectionnées"] - d["exclues"]
    assert d["attendues"] == d["produites"] + d["prévues"] + d["à rendre"] + d["en échec"]
    return d


def rapport_texte(d, resultats, ecrire):
    l = [f"Extraction des pièces — dossier {DOSSIER} — "
         + ("ÉCRITURE" if ecrire else "SIMULATION (rien n'est écrit)"),
         "",
         f"cotées en juillet sélectionnées : {d['sélectionnées']:>4}",
         f"exclues                         : {d['exclues']:>4}",
         f"attendues                       : {d['attendues']:>4}",
         f"{'produites' if ecrire else 'prévues  '}                       : "
         f"{d['produites'] if ecrire else d['prévues']:>4}",
         f"à rendre                        : {d['à rendre']:>4}",
         f"en échec                        : {d['en échec']:>4}"]
    for statut in ("exclue", "à rendre", "échec"):
        lot = [e for e in resultats if e["statut"] == statut]
        if lot:
            l += ["", f"— {statut} —"] + [f"  {e['cote']} ({e['objet']}) : {e['motif']}" for e in lot]
    return "\n".join(l)


def desc(e):
    return (e["description"] or "").replace("|", "\\|").replace("\n", " ")


def ecrire_manifestes(sortie, d, resultats, cotes_demandees):
    manifeste = {
        "schema": SCHEMA, "dossier": DOSSIER,
        "source": "case_manager.BordereauDepotJuillet, lignes à cote de juillet, "
                  "résolues en direct par content_object",
        "concordance_verrou": "identité des 106 cotes vérifiée contre "
                              "legal/depots/2026-07-24_initial/cotes.lock.json le 29 oct. 2026 ; "
                              "ordre des liasses : bordereau gelé "
                              "(legal/instance/outils/README_extraction_pieces.md)",
        "selection": cotes_demandees or "toutes les cotes de juillet",
        "exclusions": EXCLUSIONS, "decomptes": d, "cotes": resultats,
    }
    (sortie / "manifeste.json").write_text(
        json.dumps(manifeste, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [f"# Index des pièces — dossier {DOSSIER}", "",
          "Chaque fichier est transmis tel qu'il est conservé, sans conversion ni "
          "réencodage. Son empreinte SHA-256 permet d'en vérifier l'intégrité.", "",
          "**Photographies** : " + QUALIF_PHOTO + ".", "",
          "| Cote | Description | Fichier | Octets | SHA-256 |", "|---|---|---|---|---|"]
    for e in resultats:
        if e["statut"] == "produite":
            for f in e["fichiers"]:
                md.append(f"| {e['cote']} | {desc(e)} | `{f['sortie']}` | "
                          f"{f['octets_copie']} | `{f['sha256_copie']}` |")
        else:
            md.append(f"| {e['cote']} | {desc(e)} | *{e['statut']}* — "
                      f"{e.get('motif', '')} | | |")
    md += ["", "## Décomptes", ""] + [f"- {k} : {v}" for k, v in d.items()]
    (sortie / "manifeste.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    sommes = [f"{f['sha256_copie']}  {f['sortie']}"
              for e in resultats if e["statut"] == "produite" for f in e["fichiers"]]
    (sortie / "SHA256SUMS").write_text("\n".join(sommes) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--sortie", required=True, type=lambda p: Path(p).expanduser())
    ap.add_argument("--cote", action="append", default=[])
    ap.add_argument("--ecrire", action="store_true")
    a = ap.parse_args()

    lignes = selection(a.cote)  # erreurs d'argument : avant toute écriture
    verifier_sortie(a.sortie, a.ecrire)
    if a.ecrire:
        a.sortie.mkdir(parents=True, exist_ok=True)

    resultats = traiter(lignes, a.sortie, a.ecrire)
    d = decomptes(resultats)
    print(rapport_texte(d, resultats, a.ecrire))
    if a.ecrire:
        ecrire_manifestes(a.sortie, d, resultats, a.cote)
        print(f"\nManifestes : {a.sortie / 'manifeste.md'} · manifeste.json · SHA256SUMS")
    sys.exit(1 if d["en échec"] else 0)


if __name__ == "__main__":
    main()
