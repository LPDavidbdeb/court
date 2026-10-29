"""VA02 : vérifier le constat conservé et refuser les états divergents."""
from pathlib import Path

from .commun import Refus, empreinte, index_unique, lire_json


def charger_constat(chemin):
    chemin = Path(chemin)
    attendu = (chemin.parent / "SHA256SUMS").read_text().strip()
    if attendu != f"{empreinte(chemin.read_bytes())}  {chemin.name}":
        raise Refus("Empreinte de l'instantané conservé invalide")
    return lire_json(chemin)


def differences(ancien, courant):
    ecarts = []
    for collection in ("enonces", "liens", "cotes"):
        a, b = index_unique(ancien[collection]), index_unique(courant[collection])
        for identifiant in sorted(a.keys() | b.keys()):
            if a.get(identifiant) != b.get(identifiant):
                champs = sorted(k for k in (a.get(identifiant, {}).keys() | b.get(identifiant, {}).keys())
                                if a.get(identifiant, {}).get(k) != b.get(identifiant, {}).get(k))
                ecarts.append({"collection": collection, "id": identifiant, "champs": champs,
                               "nature": "ajout" if identifiant not in a else "suppression" if identifiant not in b else "modification"})
    for cle in ("document_id", "concordance_empreinte", "acces"):
        if ancien.get(cle) != courant.get(cle):
            ecarts.append({"collection": "contexte", "id": cle, "champs": [cle], "nature": "modification"})
    return ecarts


def exiger_ancrage(ancien, courant):
    ecarts = differences(ancien, courant)
    if ecarts:
        raise Refus("Ancrage divergent : " + "; ".join(f"{e['collection']} {e['id']} ({e['nature']})" for e in ecarts))
