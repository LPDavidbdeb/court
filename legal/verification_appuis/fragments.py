"""VA15 : inventaire issu de fragments validés, sans décision de scission."""
from .commun import Refus, index_unique


def liste_paragraphes_fragments(constat, fragments):
    enonces = index_unique(constat["enonces"])
    index_unique(fragments)
    groupes = {}
    for f in fragments:
        if f.get("statut") != "VALIDE":
            continue
        if f.get("auteur") != "LP" or not f.get("decision_reference"):
            raise Refus("Fragment validé : décision explicite LP exigée")
        e = enonces.get(f["statement_id"])
        if e is None or f.get("empreinte_enonce") != e["empreinte_texte"]:
            raise Refus("Fragment : énoncé absent ou empreinte périmée")
        a, b = f["debut"], f["fin"]
        if not (isinstance(a, int) and isinstance(b, int) and 0 <= a < b <= len(e["texte"])):
            raise Refus("Fragment : bornes invalides")
        if e["texte"][a:b] != f.get("extrait"):
            raise Refus("Fragment : extrait non littéral")
        groupes.setdefault(e["id"], []).append(f)
    return {"schema": "va-paragraphes-fragments/1", "fragments_valides": sum(map(len, groupes.values())),
            "paragraphes": [{"statement_id": sid, "numero_imprime": enonces[sid]["numero_imprime"],
                              "texte": enonces[sid]["texte"], "fragments": fs}
                             for sid, fs in groupes.items() if len(fs) > 1],
            "portee": "Liste à examiner à partir des seuls fragments validés ; aucune décision de scission."}
