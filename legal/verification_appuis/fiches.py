"""VA05 : fiche fidèle au lien, au manifeste et aux octets disponibles."""
from pathlib import Path

from .commun import ARTEFACTS, RACINE, Refus, empreinte, index_unique

EXTRACTION = Path.home() / "Documents/Pieces_505-17-016235-261_2026-11-06"
TRANSCRIPTIONS_LP = {f"P-{i}" for i in range(58, 65)}


def support_autorise(chemin):
    p = Path(chemin).resolve()
    transcription_lp = p.parent == (RACINE / "pieces_pdf").resolve() and p.name in {f"{c}.pdf" for c in TRANSCRIPTIONS_LP}
    if not transcription_lp and not any(p.is_relative_to(r.resolve()) for r in (RACINE / "media", RACINE / "storage", EXTRACTION, ARTEFACTS)):
        raise Refus(f"Support hors des racines autorisées : {p.name}")
    return p


def construire_fiches(constat, manifeste):
    enonces, cotes = index_unique(constat["enonces"]), index_unique(constat["cotes"])
    par_cote = index_unique(manifeste["cotes"], "cote")
    cache, fiches = {}, []
    for lien in constat["liens"]:
        cote, enonce = cotes[lien["entree_id"]], enonces[lien["statement_id"]]
        entree = par_cote.get(cote["cote"], {})
        supports, obstacles = [], []
        for fichier in entree.get("fichiers", []):
            p = support_autorise(fichier["chemin"])
            if cote.get("source_modele", "").lower().endswith((".email", ".document", ".pdfdocument")):
                if fichier.get("pk") is not None and (fichier["pk"] != cote["source_id"] or fichier.get("modele", "").lower() != cote["source_modele"].lower()):
                    raise Refus(f"{cote['cote']} : identité du manifeste divergente du constat")
            if p.parent == (RACINE / "pieces_pdf").resolve():
                import fitz
                with fitz.open(p) as document:
                    attendues = list(range(2, len(document) + 1))
                if (p.stem != cote["cote"] or not attendues or fichier.get("pages_lues") != attendues
                        or fichier.get("pages_exclues") != [1] or not fichier.get("decision_support")):
                    raise Refus("Transcription LP : pages 2 et suivantes seulement, garde exclue et décision exigée")
            if cote["cote_racine"] in {"P-19", "P-40", "P-42"} and fichier.get("champ") != "file_source":
                raise Refus(f"{cote['cote']} : le scan file_source est exigé")
            if not p.is_file():
                obstacles.append(f"Support indisponible : {p}")
                continue
            if str(p) not in cache:
                cache[str(p)] = empreinte(p.read_bytes())
            digest = cache[str(p)]
            if digest != fichier["sha256_source"]:
                raise Refus(f"{cote['cote']} : empreinte du support divergent du manifeste ({p.name})")
            support = {"chemin": str(p), "sha256": digest, "qualification": fichier.get("qualification", "non précisée"),
                             "champ": fichier.get("champ"), "rang_interne": fichier.get("rang_interne"),
                             "identite": {"modele": fichier.get("modele"), "pk": fichier.get("pk")}}
            for champ in ("pages_lues", "pages_exclues", "decision_support"):
                if champ in fichier:
                    support[champ] = fichier[champ]
            supports.append(support)
        if not entree.get("fichiers"):
            obstacles.append(f"Aucun fichier au manifeste : {entree.get('statut', 'entrée absente')}")
        fiches.append({"schema": "va-fiche/1", "lien": lien, "enonce": enonce, "cote": cote,
                       "supports": supports, "obstacles": obstacles,
                       "empreinte_piece": empreinte(__import__('json').dumps(supports, sort_keys=True, ensure_ascii=False).encode())})
    return {"schema": "va-fiches/1", "fiches": fiches, "fichiers_lus": len(cache),
            "liens_avec_obstacle": [f["lien"]["id"] for f in fiches if f["obstacles"]]}


def markdown_fiche(f):
    e, l = f["enonce"], f["lien"]
    lignes = [f"## Lien {l['id']} — § {e['numero_imprime'] or 'sans numéro propre'} — {f['cote']['cote']}", "",
              e["texte"], "", f"Référence telle que citée : **{l['cote_citee']}** ; via liasse : {l['via_liasse']}.", ""]
    for s in f["supports"]:
        lignes += [f"- Support : `{s['chemin']}`", f"- SHA-256 : `{s['sha256']}`", f"- Qualification : {s['qualification']}"]
        if "pages_lues" in s:
            lignes += [f"- Pages admises à la lecture : {s['pages_lues']} ; pages exclues : {s['pages_exclues']}",
                       f"- Décision de support : {s['decision_support']}"]
    for obstacle in f["obstacles"]:
        lignes.append(f"- À résoudre : {obstacle}")
    return "\n".join(lignes) + "\n"
