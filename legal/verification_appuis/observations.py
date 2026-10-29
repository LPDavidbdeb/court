"""VA04 : contrat va-observation/1, sans appréciation automatique des pièces."""
from datetime import datetime
import json
import re

from .commun import Refus

RESULTATS = {"RELATION_REPEREE", "AUCUNE_RELATION_REPEREE", "INDETERMINE"}
AVANCEMENTS = {"NON_EXAMINE", "PROPOSE", "VALIDE", "REJETE", "A_REVOIR"}
PORTEES = {"ETABLIT_L_ENONCE", "EN_ETABLIT_UNE_PARTIE", "ECLAIRE_SEULEMENT"}
TYPES_ECART = {"DATE", "CITATION", "ATTRIBUTION", "SENS", "IDENTITE_PIECE"}


def valider_observation(o):
    if o.get("schema") != "va-observation/1":
        raise Refus("schema : va-observation/1 exigé")
    for champ in ("id", "auteur", "date", "empreinte_enonce"):
        if not o.get(champ):
            raise Refus(f"{champ} : obligatoire")
    if not re.fullmatch(r"[0-9a-f]{64}", o["empreinte_enonce"]):
        raise Refus("empreinte_enonce : SHA-256 attendu")
    if not isinstance(o.get("liens"), list) or not o["liens"] or len(set(o["liens"])) != len(o["liens"]):
        raise Refus("liens : liste non vide sans doublon exigée")
    if not all(isinstance(i, int) and not isinstance(i, bool) and i > 0 for i in o["liens"]):
        raise Refus("liens : identifiants entiers positifs exigés")
    try:
        date = datetime.fromisoformat(o["date"])
        if date.tzinfo is None:
            raise ValueError()
    except (ValueError, TypeError):
        raise Refus("date : ISO 8601 avec fuseau exigée")
    avancement = o.get("avancement")
    if avancement not in AVANCEMENTS:
        raise Refus("avancement : inconnu")
    if avancement in {"VALIDE", "REJETE"}:
        if o["auteur"] != "LP":
            raise Refus("auteur LP obligatoire pour VALIDE ou REJETE")
        if not o.get("decision_reference"):
            raise Refus("decision_reference LP obligatoire")
    resultat = o.get("resultat")
    if avancement == "NON_EXAMINE":
        if resultat is not None:
            raise Refus("NON_EXAMINE : aucun résultat permis")
        return o
    if resultat not in RESULTATS:
        raise Refus("resultat : inconnu ou absent")
    if resultat == "RELATION_REPEREE" and (not o.get("element_observe") or not o.get("localisation")):
        raise Refus("RELATION_REPEREE : élément observé et localisation obligatoires")
    if resultat == "AUCUNE_RELATION_REPEREE" and not o.get("perimetre_lu"):
        raise Refus("AUCUNE_RELATION_REPEREE : périmètre lu obligatoire")
    if resultat == "INDETERMINE" and not o.get("obstacle"):
        raise Refus("INDETERMINE : obstacle obligatoire")
    if not o.get("raison"):
        raise Refus("raison : obligatoire")
    if not isinstance(o.get("supports"), list):
        raise Refus("supports : liste exigée, éventuellement vide si INDETERMINE")
    if resultat != "INDETERMINE" and not o["supports"]:
        raise Refus("supports : au moins un fichier examiné exigé")
    for support in o["supports"]:
        if not support.get("chemin") or not re.fullmatch(r"[0-9a-f]{64}", support.get("sha256", "")):
            raise Refus("support : chemin et SHA-256 exigés")
    if resultat == "RELATION_REPEREE":
        if o.get("portee") not in PORTEES:
            raise Refus("portee : portée documentaire obligatoire et fermée")
        if o["portee"] == "EN_ETABLIT_UNE_PARTIE" and not o.get("reste_sans_piece"):
            raise Refus("reste_sans_piece : obligatoire pour une portée partielle")
    if not isinstance(o.get("ecarts", []), list):
        raise Refus("ecarts : liste exigée")
    for ecart in o.get("ecarts", []):
        if ecart.get("type") not in TYPES_ECART or not ecart.get("description"):
            raise Refus("ecart : type fermé et description obligatoires")
    return o


def lire_observations(chemin):
    from pathlib import Path
    p = Path(chemin)
    if not p.exists():
        return []
    lignes = []
    for numero, texte in enumerate(p.read_text().splitlines(), 1):
        try:
            lignes.append(valider_observation(json.loads(texte)))
        except (Refus, ValueError) as e:
            raise Refus(f"Ligne {numero} : {e}")
    return lignes
