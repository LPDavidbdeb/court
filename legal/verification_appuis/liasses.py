"""VA10 : couverture exacte des seuls membres effectivement examinés."""
import copy
from .commun import Refus, index_unique
from .observations import valider_observation


def preparer_liasse(constat, liens_vises, membres, base):
    liens, cotes = index_unique(constat["liens"]), index_unique(constat["cotes"])
    if not liens_vises or any(i not in liens for i in liens_vises):
        raise Refus("Liasse : liens visés absents ou inconnus")
    selection = [liens[i] for i in liens_vises]
    if any(not l["via_liasse"] for l in selection):
        raise Refus("Une sous-cote nommée exige son propre examen")
    if (len({l["statement_id"] for l in selection}) != 1
            or len({l["cote_citee"] for l in selection}) != 1
            or len({cotes[l["entree_id"]]["cote_racine"] for l in selection}) != 1):
        raise Refus("Une observation de liasse exige un même paragraphe et une même liasse citée")
    par_membre = index_unique(membres, "lien_id")
    if not par_membre or not par_membre.keys() <= set(liens_vises):
        raise Refus("Manifeste de membres vide ou hors sélection")
    for identifiant, membre in par_membre.items():
        if membre.get("entree_id") != liens[identifiant]["entree_id"] or not membre.get("supports"):
            raise Refus("Membre : identité et supports examinés exigés")
    ordre = sorted(par_membre, key=lambda i: (cotes[liens[i]["entree_id"]].get("sous_rang") or 0, i))
    o = copy.deepcopy(base)
    o.update(nature="LIASSE", liens=ordre, membres=[par_membre[i] for i in ordre],
             liens_non_examines=[i for i in liens_vises if i not in par_membre],
             supports=[s for i in ordre for s in par_membre[i]["supports"]])
    valider_observation(o)
    return o


def verifier_rattachement(o, constat):
    liens = index_unique(constat["liens"])
    if any(i not in liens for i in o["liens"]):
        raise Refus("Observation visant un lien inconnu du constat")
    sids = {liens[i]["statement_id"] for i in o["liens"]}
    if len(sids) != 1:
        raise Refus("Une observation ne peut mélanger plusieurs paragraphes")
    enonce = index_unique(constat["enonces"])[next(iter(sids))]
    if o["empreinte_enonce"] != enonce["empreinte_texte"]:
        raise Refus("Empreinte de l'énoncé incompatible avec le lien")
    if o.get("nature") == "LIASSE" or len(o["liens"]) > 1:
        recalcule = preparer_liasse(constat, o["liens"], o.get("membres", []), o)
        if recalcule["liens"] != o["liens"] or recalcule["supports"] != o["supports"]:
            raise Refus("Manifeste de liasse différent des liens ou supports déclarés")
