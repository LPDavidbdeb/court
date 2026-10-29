"""VA03 : liste complète, sans reconstruire ni étendre les renvois du dépôt."""
from .commun import index_unique


def liste_travail(constat):
    par_cote = index_unique(constat["cotes"])
    par_enonce = index_unique(constat["enonces"])
    par_statement = {}
    for lien in constat["liens"]:
        par_statement.setdefault(lien["statement_id"], []).append(lien)

    def priorite(enonce):
        numero = enonce["numero_imprime"]
        racines = {par_cote[l["entree_id"]]["cote_racine"] for l in par_statement.get(enonce["id"], [])}
        if numero in ("234", "235", "236"):
            return 0
        if racines & {"P-19", "P-40", "P-42"}:
            return 1
        if numero and numero.isdecimal() and 200 <= int(numero) <= 217:
            return 2
        return 3

    lignes, sans_reference = [], []
    for e in sorted(par_enonce.values(), key=lambda e: (priorite(e), e["ordre"], e["id"])):
        commun = {"statement_id": e["id"], "numero_imprime": e["numero_imprime"],
                  "ordre": e["ordre"], "priorite": priorite(e), "texte": e["texte"]}
        liens = par_statement.get(e["id"], [])
        if not liens:
            sans_reference.append({**commun, "nature": "SANS_REFERENCE"})
        for lien in sorted(liens, key=lambda l: l["id"]):
            cote = par_cote[lien["entree_id"]]
            lignes.append({**commun, "lien_id": lien["id"], "entree_id": cote["id"],
                           "cote": cote["cote"], "cote_citee": lien["cote_citee"],
                           "via_liasse": lien["via_liasse"], "avancement": "NON_EXAMINE"})
    return {"schema": "va-travail/1", "liens": lignes, "sans_reference": sans_reference,
            "totaux": {"liens": len(lignes), "sans_reference": len(sans_reference),
                       "sans_reference_numero_propre": sum(e["numero_imprime"] is not None for e in sans_reference),
                       "lignes": len(lignes) + len(sans_reference)}}


def markdown_travail(travail):
    lignes = ["# Liste de travail", "", f"Effectifs : {travail['totaux']}", "", "| Priorité | § imprimé | Lien | Cote citée | Pièce |", "|---|---|---|---|---|"]
    for l in travail["liens"]:
        lignes.append(f"| {l['priorite']} | {l['numero_imprime'] or 'sans numéro propre'} | {l['lien_id']} | {l['cote_citee']} | {l['cote']} |")
    lignes += ["", "## Énoncés sans référence", ""]
    for e in travail["sans_reference"]:
        lignes.append(f"- Énoncé {e['statement_id']}, § {e['numero_imprime'] or 'sans numéro propre'} : {e['texte']}")
    return "\n".join(lignes) + "\n"
