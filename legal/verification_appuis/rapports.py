"""Restitutions dérivées, sans décision probatoire ou éditoriale automatique."""
from .decisions import courantes


def rapport_ecarts(historique):
    retenues = {}
    for etat in courantes(historique).values():
        for o in (etat["validee"], etat["derniere"]):
            if o is not None:
                retenues[o["id"]] = o
    return [{"observation_id": o["id"], "liens": o["liens"], "avancement": o["avancement"],
             "resultat": o["resultat"], **ecart}
            for o in retenues.values() for ecart in o.get("ecarts", [])]
