"""VA07 : décisions explicites de LP et lecture des versions acquises."""
import copy

from .commun import Refus
from .journal import ajouter_version, cle_cible, proposer
from .observations import lire_observations


def decider(chemin, decision):
    if (decision.get("auteur") != "LP" or not decision.get("reference")
            or decision.get("action") not in {"VALIDER", "REJETER"}):
        raise Refus("Décision explicite de LP avec référence et action exigée")
    historique = lire_observations(chemin)
    par_id = {o["id"]: o for o in historique}
    if decision.get("observation_id") not in par_id:
        raise Refus("Observation visée inconnue")
    precedent = par_id[decision["observation_id"]]
    courant = [o for o in historique if cle_cible(o) == cle_cible(precedent)][-1]
    if courant["id"] != precedent["id"] or precedent["avancement"] != "PROPOSE":
        raise Refus("La décision LP doit viser la dernière proposition de cette cible")
    nouvelle = copy.deepcopy(precedent)
    nouvelle.update(id=decision["version_id"], remplace=precedent["id"], auteur="LP", date=decision["date"],
                    avancement="VALIDE" if decision["action"] == "VALIDER" else "REJETE", decision_reference=decision["reference"])
    return ajouter_version(chemin, nouvelle)


def corriger(chemin, version_id, date, changements):
    historique = lire_observations(chemin)
    if not historique:
        raise Refus("Journal vide")
    precedent = next((o for o in reversed(historique) if o["id"] == changements.get("remplace")), None)
    if precedent is None:
        raise Refus("Version remplacée inconnue")
    if {"id", "auteur", "avancement", "liens", "decision_reference"} & changements.keys():
        raise Refus("Une correction ne peut usurper la décision ou changer de cible")
    nouvelle = copy.deepcopy(precedent)
    nouvelle.update(changements)
    nouvelle.pop("decision_reference", None)
    nouvelle.update(id=version_id, date=date, auteur="CODEX", avancement="PROPOSE")
    return proposer(chemin, nouvelle)


def courantes(historique):
    par_lien = {}
    for o in historique:
        for lien in o["liens"]:
            etat = par_lien.setdefault(lien, {"validee": None, "derniere": None})
            etat["derniere"] = o
            if o["avancement"] == "VALIDE":
                etat["validee"] = o
    return par_lien
