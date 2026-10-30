"""VA13 : fraîcheur calculée, sans réécrire l'historique des décisions."""
from .commun import empreinte, index_unique
from .fiches import support_autorise


def detecter_derives(constat, historique, courant=None):
    courant = courant or constat
    anciens_liens, liens = index_unique(constat["liens"]), index_unique(courant["liens"])
    anciennes_cotes, cotes = index_unique(constat["cotes"]), index_unique(courant["cotes"])
    enonces = index_unique(courant["enonces"])
    cache, details = {}, []
    for o in historique:
        raisons = []
        for identifiant in o["liens"]:
            ancien, nouveau = anciens_liens.get(identifiant), liens.get(identifiant)
            if ancien is None or nouveau != ancien:
                raisons.append(f"Lien {identifiant} supprimé ou modifié")
                continue
            e = enonces.get(nouveau["statement_id"])
            if e is None or empreinte(e["texte"].encode()) != o["empreinte_enonce"]:
                raisons.append(f"Texte de l'énoncé {nouveau['statement_id']} modifié ou absent")
            if anciennes_cotes.get(ancien["entree_id"]) != cotes.get(nouveau["entree_id"]):
                raisons.append(f"Identité de la cote {nouveau['entree_id']} modifiée")
        for s in o.get("supports", []):
            p = support_autorise(s["chemin"])
            if str(p) not in cache:
                cache[str(p)] = empreinte(p.read_bytes()) if p.is_file() else None
            if cache[str(p)] != s["sha256"]:
                raisons.append(f"Support modifié ou indisponible : {p.name}")
        if raisons:
            details.append({"observation_id": o["id"], "liens": o["liens"], "avancement_effectif": "A_REVOIR", "raisons": sorted(set(raisons))})
    return {"schema": "va-derives/1", "observations_a_revoir": sorted({d["observation_id"] for d in details}),
            "details": details, "fichiers_controles": len(cache)}
