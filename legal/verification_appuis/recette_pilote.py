"""Recette explicitement dictée par LP : six décisions, jamais celle du lien 472."""
import copy
from datetime import datetime, timezone
from email import policy
from email.parser import BytesParser

from .commun import RACINE, Refus, empreinte, octets_json
from .decisions import corriger, decider
from .journal import proposer
from .observations import lire_observations, valider_observation

REFERENCE_LP = "Message de LP du 29 octobre 2026 à l'agent d'exécution de l'épic VA — recette du pilote"
LIENS_VALIDES_LP = (468, 469, 470, 471, 473, 474)


def texte_date_dicte():
    prompt = (RACINE / "docs/verification_appuis/execution/PROMPT_SUITE_PILOTE_2026-10-29.md").read_text()
    bloc = prompt.split("**Texte de l'écart DATE du lien 469 (dicté) :**", 1)[1].split("**Pour la nouvelle proposition", 1)[0]
    return "\n".join(ligne[2:] for ligne in bloc.splitlines() if ligne.startswith("> "))


def ecarts_date_corriges(observation, texte):
    ecarts = copy.deepcopy(observation["ecarts"])
    dates = [e for e in ecarts if e["type"] == "DATE"]
    if len(dates) != 1 or not texte:
        raise Refus("Une seule description DATE doit être remplacée par la dictée")
    dates[0]["description"] = texte
    return ecarts


def nouvelle_472(fiche, precedent, constat, date):
    from .fiches import support_autorise
    if fiche["lien"]["id"] != 472 or fiche["cote"]["source_id"] != 4:
        raise Refus("La reprise 472 exige Email 4 dans le nouveau constat")
    support = fiche["supports"][0]
    p = support_autorise(support["chemin"])
    contenu = p.read_bytes()
    if empreinte(contenu) != support["sha256"]:
        raise Refus("Email 4 modifié depuis la fiche")
    m = BytesParser(policy=policy.default).parsebytes(contenu)
    corps = m.get_body(preferencelist=("plain",)).get_content().replace("\r\n", "\n")
    debut = corps.index("Nous avons procédé")
    fin = corps.index("Je ne comprends pas que", debut)
    passage = corps[debut:fin].rstrip()
    debut2 = corps.index("Il va être temps de finaliser")
    fin2 = corps.index("Je penses que", debut2)
    complement = corps[debut2:fin2].rstrip()
    o = copy.deepcopy(precedent)
    o.update(id="VA16-L472-v2", remplace=precedent["id"], auteur="CODEX", date=date,
             avancement="PROPOSE", grille_version="1.1", supports=fiche["supports"],
             empreinte_enonce=fiche["enonce"]["empreinte_texte"],
             empreintes_cotes={str(fiche["cote"]["id"]):empreinte(octets_json(fiche["cote"]))},
             element_observe=passage,
             localisation="Email 4, P-38 rattachée par LP le 29 octobre 2026 ; Me Ayoub à LP, 20 avril 2020, 11 h 37 -0400 ; paragraphe commençant ‘Nous avons procédé’. Courriel original local intégralement lu.",
             portee="EN_ETABLIT_UNE_PARTIE",
             raison="Me Ayoub affirme qu'il y a eu un jugement final et non une entente, et dit qu'elle ne fera aucune autre demande à la cour. La pièce établit cette déclaration de la procureure et sa réponse au demandeur ; elle documente sa position sur le jugement, sans établir que toute partie nie toute entente ni que toute voie de contestation soit fermée.",
             reste_sans_piece="L'universalité ‘aucune partie ne reconnaît’, la fermeture objective de la voie normale de contestation, l'impossibilité en fait d'agir et les conditions légales de suspension ne sont pas établies par cette seule réponse. Les déclarations sur économies, bail et emploi demeurent des propos du demandeur.",
             limites="La demande d'avril 2020 visant à ‘finaliser notre entente’ n'identifie pas sûrement cette entente à celle mentionnée au jugement de novembre 2019. Il faut conserver cette distinction ; le courriel établit les mots prononcés, sans arbitrer la vérité objective de toutes les circonstances ni leurs effets juridiques.",
             perimetre_lu="EML original Email 4 entier : en-têtes, réponse du 20 avril 2020 et message du demandeur du 17 avril reproduit. Aucune consultation Gmail.",
             methode_verbatim="Corps MIME text/plain de l'EML original, décodé ; CRLF ramenés à LF, autres caractères conservés.",
             passages_supplementaires=[{"texte":complement,"localisation":"Même Email 4, message de LP du 17 avril 2020 reproduit sous les en-têtes De/Date/À/Objet, deuxième paragraphe."}],
             ecarts=[
                 {"type":"SENS","degre":"NE_L_ETABLIT_PAS","description":"Le §235 dit ‘une entente qu’aucune partie ne reconnaît’. Le refus de qualification formulé par Me Ayoub documente sa propre position, sans établir l'absence de reconnaissance de toutes les parties. LP écrit au contraire ‘finaliser notre entente’ : ces mots empêchent d'en tirer cette proposition universelle, sans démontrer qu'il reconnaît l'entente précise de novembre 2019, l'identité des deux ententes restant indéterminée."},
                 {"type":"IDENTITE_PIECE","degre":"ETABLIT_EN_CADRANT_AUTREMENT","description":"Les mots de Me Ayoub sont dans email_manager.Email pk 4 (20 avril 2020), où le courriel du 17 avril est reproduit ; ils sont absents d'email_manager.Email pk 330, seul objet de la cote au verrou du dépôt. Le rattachement courant de P-38 a été changé par LP sur la ligne 377, 330 → 4, annoncé au journal du 29 octobre. Le nouveau support porte la réponse, mais sa provenance diffère du dépôt historique : cette correction ne doit pas faire croire que le verrou contenait déjà Email 4."}
             ])
    o.pop("decision_reference", None)
    valider_observation(o)
    return o


def appliquer_recette(journal, constat, proposition_472, date, reference=REFERENCE_LP, texte_date=None):
    """Exécuter seulement la liste dictée ; les décisions conservent leur auteur LP."""
    h = lire_observations(journal)
    par_id = {o["id"]:o for o in h}
    if proposition_472["liens"] != [472] or proposition_472["avancement"] != "PROPOSE":
        raise Refus("472 doit rester une proposition")
    for lien in (*LIENS_VALIDES_LP, 472):
        if f"VA16-L{lien}-v1" not in par_id:
            raise Refus("Versions initiales attendues absentes")
    futurs = {f"VA16-L{lien}-v2" for lien in (*LIENS_VALIDES_LP, 472)} | {"VA16-L469-v3"}
    if futurs & par_id.keys():
        raise Refus("Recette déjà commencée : relire le journal avant toute reprise")
    ecarts = ecarts_date_corriges(par_id["VA16-L469-v1"], texte_date or texte_date_dicte())
    corriger(journal, "VA16-L469-v2", date, {"remplace":"VA16-L469-v1", "ecarts":ecarts})
    decisions = []
    for lien in LIENS_VALIDES_LP:
        version = 2 if lien == 469 else 1
        d = {"auteur":"LP","action":"VALIDER","reference":reference,"date":date,
             "observation_id":f"VA16-L{lien}-v{version}","version_id":f"VA16-L{lien}-v{version+1}"}
        decider(journal, d)
        decisions.append(d)
    proposer(journal, proposition_472, constat)
    return decisions
