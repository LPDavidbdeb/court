"""VA16 : lecture et propositions limitées aux §§ imprimés 234–236."""
from email import policy
from email.parser import BytesParser
from pathlib import Path

from .commun import ARTEFACTS, Refus, empreinte, lire_json, octets_json, ecrire_identique_ou_nouveau
from .fiches import support_autorise
from .source_django import verifier_accord

NUMEROS_PILOTE = {"234", "235", "236"}


def fiches_pilote(fiches):
    return [f for f in fiches["fiches"] if f["enonce"]["numero_imprime"] in NUMEROS_PILOTE]


def preparer_lectures(accord, chemin_fiches):
    verifier_accord(accord, "VA16")
    fiches = fiches_pilote(lire_json(chemin_fiches))
    repertoire = ARTEFACTS / "pilote/lectures"
    repertoire.mkdir(parents=True, exist_ok=True)
    inventaire = []
    for f in fiches:
        if f["obstacles"]:
            raise Refus(f"Lien pilote {f['lien']['id']} : support indisponible")
        for s in f["supports"]:
            p = support_autorise(s["chemin"])
            contenu = p.read_bytes()
            if empreinte(contenu) != s["sha256"]:
                raise Refus(f"Support pilote modifié : {p.name}")
            cote = f["cote"]["cote"]
            if p.suffix.lower() == ".eml":
                message = BytesParser(policy=policy.default).parsebytes(contenu)
                partie = message.get_body(preferencelist=("plain",))
                if partie is None:
                    raise Refus(f"{cote} : texte brut absent ; lecture HTML à prévoir explicitement")
                texte = "\n".join(f"{k}: {message.get(k, '')}" for k in ("From", "To", "Date", "Subject"))
                texte += "\n\n" + partie.get_content()
                ecrire_identique_ou_nouveau(repertoire / f"{cote}.txt", texte.encode())
                inventaire.append({"cote": cote, "source": s, "lecture": str(repertoire / f"{cote}.txt"), "type": "eml-texte-brut"})
            elif p.suffix.lower() == ".pdf":
                import fitz
                with fitz.open(p) as document:
                    textes = []
                    for numero, page in enumerate(document, 1):
                        textes.append(f"PAGE {numero}\n{page.get_text()}")
                        image = repertoire / f"{cote}-page-{numero}.png"
                        if not image.exists():
                            page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(image)
                    ecrire_identique_ou_nouveau(repertoire / f"{cote}.txt", "\n\n".join(textes).encode())
                    inventaire.append({"cote": cote, "source": s, "pages": len(document), "type": "pdf-original-rendu-pour-lecture"})
    ecrire_identique_ou_nouveau(repertoire / "inventaire.json", octets_json(inventaire))
    return inventaire


def verifier_perimetre_pilote(constat, propositions):
    from .observations import valider_observation
    from .liasses import verifier_rattachement
    sids = {e["id"] for e in constat["enonces"] if e["numero_imprime"] in NUMEROS_PILOTE}
    attendus = {l["id"] for l in constat["liens"] if l["statement_id"] in sids}
    couverts = []
    for o in propositions:
        if o.get("auteur") != "CODEX" or o.get("avancement") != "PROPOSE" or o.get("decision_reference"):
            raise Refus("Le pilote contient uniquement des propositions CODEX, sans décision LP")
        valider_observation(o)
        verifier_rattachement(o, constat)
        couverts.extend(o["liens"])
    if len(couverts) != len(set(couverts)) or set(couverts) != attendus:
        raise Refus(f"Périmètre pilote différent : attendus {sorted(attendus)}, proposés {sorted(couverts)}")
    return sorted(attendus)


def enregistrer_pilote(accord, constat, propositions, journal):
    from .journal import proposer
    from .observations import lire_observations
    verifier_accord(accord, "VA16")
    verifier_perimetre_pilote(constat, propositions)
    # Tout contrôler avant le premier ajout ; aucune nouvelle source n'est cherchée.
    for o in propositions:
        for s in o["supports"]:
            p = support_autorise(s["chemin"])
            if not p.is_file() or empreinte(p.read_bytes()) != s["sha256"]:
                raise Refus(f"Support pilote changé ou absent : {p.name}")
    existantes = {o["id"]: o for o in lire_observations(journal)}
    for o in propositions:
        if o["id"] in existantes:
            if existantes[o["id"]] != o:
                raise Refus("Version pilote déjà enregistrée avec un contenu différent")
        else:
            proposer(journal, o, constat)
    return len(propositions)


def dossier_validation(constat, propositions):
    verifier_perimetre_pilote(constat, propositions)
    lignes = ["# Pilote VA16 — propositions à valider par LP", "",
              "**7 propositions CODEX ; aucune observation validée ou rejetée par LP.**", "",
              "Chaque observation porte sur un lien existant examiné séparément. La relecture globale reste différée.", "",
              "| Lien | § imprimé | Cote | Portée proposée | Écarts proposés |", "|---|---|---|---|---|"]
    par_lien = {l["id"]: l for l in constat["liens"]}
    for o in propositions:
        lien = par_lien[o["liens"][0]]
        e = next(e for e in constat["enonces"] if e["id"] == lien["statement_id"])
        lignes.append(f"| {lien['id']} | {e['numero_imprime']} | {lien['cote_citee']} | {o['portee']} | {', '.join(x['type'] for x in o['ecarts']) or '—'} |")
    for e in constat["enonces"]:
        if e["numero_imprime"] not in NUMEROS_PILOTE:
            continue
        lignes += ["", f"## §{e['numero_imprime']} — texte intégral déposé", "", e["texte"], ""]
        observations = [o for o in propositions if par_lien[o["liens"][0]]["statement_id"] == e["id"]]
        if not observations:
            lignes.append("Aucune pièce citée : aucune observation de lien créée. Cet énoncé reste visible comme tel.")
        for o in observations:
            lien = par_lien[o["liens"][0]]
            lignes += [f"### Lien {lien['id']} — {lien['cote_citee']} — {o['id']}", "",
                       f"Auteur : **{o['auteur']}**. Avancement : **{o['avancement']}**. Résultat proposé : **{o['resultat']}**.", "",
                       f"**Portée proposée : {o['portee']}**", "", "Passage observé :", ""]
            lignes += ["> " + l for l in o["element_observe"].splitlines()]
            lignes += ["", "Localisation : " + o["localisation"], "", "Relation observée : " + o["raison"], "",
                       "Limites : " + o["limites"], ""]
            for p in o.get("passages_supplementaires", []):
                lignes += ["Passage complémentaire — " + p["localisation"], ""]
                lignes += ["> " + l for l in p["texte"].splitlines()]
                lignes.append("")
            for ecart in o["ecarts"]:
                lignes += [f"Écart proposé **{ecart['type']}** : {ecart['description']}", ""]
            for s in o["supports"]:
                lignes += [f"Support : `{s['chemin']}`", f"SHA-256 : `{s['sha256']}`", f"Qualification : {s['qualification']}", ""]
            lignes += ["Périmètre lu : " + o["perimetre_lu"], "Méthode : " + o["methode_verbatim"], "",
                       "**Décision de LP : en attente.**", ""]
    lignes += ["## Point d'arrêt", "", "Les sept liens ont une proposition. Le taux de validation LP reste **0 %**.",
               "Aucune autre série, aucune relecture VA14 ou VA17 et aucune phase 1 ne sont exécutées."]
    return "\n".join(lignes).rstrip() + "\n"
