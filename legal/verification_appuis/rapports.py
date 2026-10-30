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


def image_depot(constat, historique, a_revoir=(), numeros=None):
    par_etat = {e["lien_id"]: e for e in etats_liens(constat, historique, a_revoir)}
    paragraphes = []
    for enonce in constat["enonces"]:
        if numeros is not None and enonce["numero_imprime"] not in numeros:
            continue
        liens = [l for l in constat["liens"] if l["statement_id"] == enonce["id"]]
        validees, attentes, restes = {}, {}, []
        for lien in liens:
            etat = par_etat[lien["id"]]
            if etat["validee"]:
                validees[etat["validee"]["id"]] = etat["validee"]
            else:
                restes.append({"lien_id": lien["id"], "avancement": etat["avancement"]})
            if etat["attente"]:
                attentes[etat["attente"]["id"]] = etat["attente"]
        paragraphes.append({"statement_id": enonce["id"], "numero_imprime": enonce["numero_imprime"],
                           "texte": enonce["texte"], "references": liens,
                           "observations_validees": list(validees.values()),
                           "propositions_en_attente": list(attentes.values()), "restes": restes,
                           "sans_reference": not bool(liens)})
    return {"schema": "va-image/1", "paragraphes": paragraphes}


def markdown_image(image):
    lignes = ["# Image du dépôt — observations validées et travail restant", ""]
    for p in image["paragraphes"]:
        lignes += [f"## § {p['numero_imprime'] or 'sans numéro propre'} — énoncé {p['statement_id']}", "", p["texte"], ""]
        for l in p["references"]:
            lignes.append(f"- Lien {l['id']} : {l['cote_citee']} ; entrée {l['entree_id']} ; via liasse : {l['via_liasse']}.")
        for o in p["observations_validees"]:
            lignes += [f"- Observation validée {o['id']} : {o['resultat']} ; portée {o.get('portee') or 'sans objet'}.",
                       f"  Élément observé : {o.get('element_observe', '')}", f"  Localisation : {o.get('localisation', '')}",
                       f"  Raison : {o['raison']}"]
        for o in p["propositions_en_attente"]:
            lignes.append(f"- Proposition en attente {o['id']} ; auteur {o['auteur']}. Aucun résultat validé acquis par cette proposition.")
        for r in p["restes"]:
            lignes.append(f"- Reste : lien {r['lien_id']} — {r['avancement']}.")
        if p["sans_reference"]:
            lignes.append("- Aucune référence citée dans cet énoncé.")
        lignes.append("")
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
