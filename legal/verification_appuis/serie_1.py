"""Série autorisée : exactement les quarante premiers liens de priorité 1."""
from collections import Counter

from .commun import Refus, empreinte
from .fiches import support_autorise
from .journal import proposer
from .liasses import verifier_rattachement
from .observations import lire_observations, valider_observation, DEGRES_ECART
from .source_django import verifier_accord

ORDRE_DEGRES = {"CONTREDIT":0, "ETABLIT_EN_CADRANT_AUTREMENT":1, "NE_L_ETABLIT_PAS":2}


def selection_serie(travail):
    selection = [l for l in travail["liens"] if l["priorite"] == 1][:40]
    if len(selection) != 40:
        raise Refus("La série exige les 40 premiers liens de priorité 1")
    return selection


def verifier_serie(constat, travail, propositions):
    attendus = [x["lien_id"] for x in selection_serie(travail)]
    if [o.get("liens") for o in propositions] != [[i] for i in attendus]:
        raise Refus("Périmètre ou ordre différent des 40 liens de la série")
    for o in propositions:
        if o.get("auteur") != "CODEX" or o.get("avancement") != "PROPOSE" or o.get("decision_reference"):
            raise Refus("Série : propositions CODEX seulement")
        if o.get("grille_version") != "1.1":
            raise Refus("Grille 1.1 exigée pour la série")
        valider_observation(o)
        verifier_rattachement(o, constat)
    return attendus


def enregistrer_serie(accord, constat, travail, propositions, journal):
    verifier_accord(accord, "VA06")
    attendus = verifier_serie(constat, travail, propositions)
    hist = lire_observations(journal)
    if any(set(o["liens"]) & set(attendus) for o in hist):
        raise Refus("Un lien de la série a déjà une observation : reprise explicite nécessaire")
    # Toute erreur de source arrête avant le premier ajout.
    controles = {}
    for o in propositions:
        for s in o["supports"]:
            p = support_autorise(s["chemin"])
            if str(p) not in controles:
                controles[str(p)] = empreinte(p.read_bytes()) if p.is_file() else None
            if controles[str(p)] != s["sha256"]:
                raise Refus("Support de la série modifié ou absent")
    for o in propositions:
        proposer(journal, o, constat)
    return len(propositions), len(controles)


def tableau_ecarts(propositions):
    ecarts = [{"lien":o["liens"][0],"observation":o["id"],**e} for o in propositions for e in o["ecarts"]]
    ordre = {o["liens"][0]:i for i,o in enumerate(propositions)}
    return sorted(ecarts, key=lambda e:(ORDRE_DEGRES[e["degre"]],ordre[e["lien"]],e["type"]))


def dossier_serie(constat, travail, propositions):
    verifier_serie(constat, travail, propositions)
    ecarts = tableau_ecarts(propositions)
    comptes = Counter(e["degre"] for e in ecarts)
    liens = {l["id"]:l for l in constat["liens"]}
    enonces = {e["id"]:e for e in constat["enonces"]}
    lignes = ["# Série 1 — 40 propositions à valider par LP", "",
              "**40 PROPOSE, auteur CODEX ; aucune décision LP sur cette série.**", "",
              "## Écarts seuls, du plus grave au moins grave", "",
              "| Degré | Lien | § imprimé | Cote | Type | Écart proposé |",
              "|---|---|---|---|---|---|"]
    for e in ecarts:
        lien=liens[e["lien"]];eno=enonces[lien["statement_id"]]
        desc=e["description"].replace("|","\\|").replace("\n"," ")
        lignes.append(f"| {e['degre']} | [{e['lien']}](#lien-{e['lien']}) | {eno['numero_imprime']} | {lien['cote_citee']} | {e['type']} | {desc} |")
    lignes += ["", "Comptage des écarts (plusieurs écarts possibles par lien) : " +
               " ; ".join(f"{degre} = {comptes[degre]}" for degre in ORDRE_DEGRES) + ".", "",
               "Les écarts sont des propositions documentaires. Une contribution limitée reste utile ; l'absence d'un fait dans une pièce ne tranche pas sa vérité objective. Aucune appréciation cumulative ni relecture VA14/VA17 n'est produite.", "",
               "## Périmètre", "", "L'ordre est celui des 40 premiers liens de priorité 1 de VA03. Ce groupe comprend tous les liens des paragraphes citant P-19, P-40 ou P-42, y compris leurs autres cotes. Le quarantième lien est 277 ; aucun lien suivant n'est examiné.", ""]
    precedent=None
    for o in propositions:
        lien=liens[o["liens"][0]];e=enonces[lien["statement_id"]]
        if e["id"]!=precedent:
            lignes += [f"## §{e['numero_imprime']} — texte intégral du constat", "",e["texte"],""]
            precedent=e["id"]
        lignes += [f"<a id=\"lien-{lien['id']}\"></a>", f"### Lien {lien['id']} — {lien['cote_citee']} — {o['id']}", "",
                   f"**PROPOSE — CODEX — {o['resultat']} — {o['portee']}**", "",
                   "Passage observé :", ""]
        lignes += ["> "+t for t in o["element_observe"].splitlines()]
        lignes += ["", "Localisation : "+o["localisation"], "", "Relation : "+o["raison"], "", "Limites : "+o["limites"], ""]
        for p in o.get("passages_supplementaires",[]):
            lignes += ["Passage complémentaire — "+p["localisation"], ""]+["> "+t for t in p["texte"].splitlines()]+[""]
        for ec in o["ecarts"]:
            lignes += [f"Écart **{ec['degre']} — {ec['type']}** : {ec['description']}", ""]
        lignes += ["Contrôle d'attribution : "+o["controle_attribution"], "", "Périmètre lu : "+o["perimetre_lu"], "", "Méthode : "+o["methode_verbatim"], ""]
        for s in o["supports"]:
            lignes += [f"Support : `{s['chemin']}`", f"SHA-256 : `{s['sha256']}`",f"Qualification : {s['qualification']}", ""]
        lignes += [f"Décision LP pour {o['id']} : **en attente**.", ""]
    # Seule la présentation Markdown perd ses espaces de fin de ligne ; les
    # passages canoniques dans les observations JSONL restent inchangés.
    return "\n".join(l.rstrip() for l in lignes).rstrip()+"\n"
