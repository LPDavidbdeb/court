"""Restitutions dérivées, sans décision probatoire ou éditoriale automatique."""
from .decisions import courantes
from .observations import AVANCEMENTS
from .travail import liste_travail


def etats_liens(constat, historique, a_revoir=()):
    index = courantes(historique)
    etats = []
    for lien in constat["liens"]:
        courant = index.get(lien["id"], {})
        validee, derniere = courant.get("validee"), courant.get("derniere")
        observation = validee or derniere
        avancement = observation["avancement"] if observation else "NON_EXAMINE"
        if observation and observation["id"] in a_revoir:
            avancement = "A_REVOIR"
        etats.append({"lien_id": lien["id"], "statement_id": lien["statement_id"], "avancement": avancement,
                       "resultat": observation.get("resultat") if observation and avancement not in {"NON_EXAMINE", "A_REVOIR"} else None,
                       "observation": observation, "validee": validee if avancement == "VALIDE" else None,
                       "attente": derniere if derniere and derniere["avancement"] == "PROPOSE" else None})
    return etats


def couverture(constat, historique, a_revoir=(), numeros=None):
    sids = {e["id"] for e in constat["enonces"] if numeros is None or e["numero_imprime"] in numeros}
    lignes = [e for e in etats_liens(constat, historique, a_revoir) if e["statement_id"] in sids]
    comptes = {a: sum(e["avancement"] == a for e in lignes) for a in sorted(AVANCEMENTS)}
    sans = [e for e in liste_travail(constat)["sans_reference"] if e["statement_id"] in sids]
    return {"schema": "va-couverture/1", "denominateur": len(lignes), "comptes": comptes,
            "pourcentage_valide": 100 * comptes["VALIDE"] / len(lignes) if lignes else None,
            "liens": lignes, "sans_reference": sans,
            "ecarts": [e for e in rapport_ecarts(historique) if any(l in {r["lien_id"] for r in lignes} for l in e["liens"])]}


def markdown_couverture(r):
    lignes = ["# Couverture et travail restant", "", f"Dénominateur : **{r['denominateur']} liens**.",
              f"Avancements : {r['comptes']}", f"Pourcentage validé : {r['pourcentage_valide']}", "",
              "| Lien | Avancement | Résultat (selon cet avancement) |", "|---|---|---|"]
    lignes += [f"| {e['lien_id']} | {e['avancement']} | {e['resultat'] or ''} |" for e in r["liens"]]
    lignes += ["", f"Énoncés sans référence : {len(r['sans_reference'])}", "", "## Écarts typés", ""]
    lignes += [f"- {e['observation_id']} ({e['avancement']}) — {e['type']} : {e['description']}" for e in r["ecarts"]]
    return "\n".join(lignes).rstrip() + "\n"


def rapport_ecarts(historique):
    retenues = {}
    for etat in courantes(historique).values():
        for o in (etat["validee"], etat["derniere"]):
            if o is not None:
                retenues[o["id"]] = o
    return [{"observation_id": o["id"], "liens": o["liens"], "avancement": o["avancement"],
             "resultat": o["resultat"], **ecart}
            for o in retenues.values() for ecart in o.get("ecarts", [])]
