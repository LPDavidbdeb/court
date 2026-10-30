"""Transcriptions et observations proposées après lecture des sept originaux.

Les citations EML sont prélevées dans le corps MIME texte, avec seule
normalisation CRLF→LF. Les citations PDF sont transcrites après lecture visuelle
des pages rendues depuis les scans dont les empreintes sont conservées.
"""
from datetime import datetime, timezone
from email import policy
from email.parser import BytesParser
from pathlib import Path

from legal.verification_appuis.commun import ARTEFACTS, Refus, lire_json, octets_json, ecrire_identique_ou_nouveau
from legal.verification_appuis.pilote import fiches_pilote, verifier_perimetre_pilote
from legal.verification_appuis.source_django import verifier_accord


def corps(fiche):
    p = Path(fiche["supports"][0]["chemin"])
    m = BytesParser(policy=policy.default).parsebytes(p.read_bytes())
    return m.get_body(preferencelist=("plain",)).get_content().replace("\r\n", "\n")


def extrait(texte, debut, fin):
    a = texte.index(debut)
    b = texte.index(fin, a)
    return texte[a:b].rstrip()


def preparer():
    verifier_accord(ARTEFACTS / "accords.json", "VA16")
    fs = {f["lien"]["id"]: f for f in fiches_pilote(lire_json(ARTEFACTS / "fiches/fiches.json"))}
    date = datetime.now(timezone.utc).isoformat()
    ps = []
    def ajouter(lien, element, localisation, raison, portee, limites, ecarts=None, autres=None):
        f = fs[lien]
        o = {"schema": "va-observation/1", "id": f"VA16-L{lien}-v1", "liens": [lien], "remplace": None,
             "auteur": "CODEX", "avancement": "PROPOSE", "date": date,
             "empreinte_enonce": f["enonce"]["empreinte_texte"], "supports": f["supports"],
             "resultat": "RELATION_REPEREE", "element_observe": element, "localisation": localisation,
             "raison": raison, "portee": portee, "limites": limites, "ecarts": ecarts or [],
             "perimetre_lu": "PDF original, toutes les pages, lecture visuelle des rendus" if f["supports"][0]["chemin"].endswith(".pdf") else "En-têtes From/To/Date/Subject et intégralité du corps MIME texte, y compris les messages antérieurs cités",
             "methode_verbatim": "transcription visuelle du scan, à valider par LP" if f["supports"][0]["chemin"].endswith(".pdf") else "extrait du texte MIME décodé ; CRLF normalisés en LF uniquement",
             "passages_supplementaires": autres or []}
        if portee == "EN_ETABLIT_UNE_PARTIE":
            o["reste_sans_piece"] = limites
        ps.append(o)

    ajouter(468, "Affirmé solennellement devant moi\nà Saint-Lambert, ce 21 juillet 2023",
            "P-40, page 4/5, jurat ; titre p. 1, énoncé 8 p. 2 et date de signature p. 3 également lus.",
            "Le scan porte une déclaration sous serment datée du 21 juillet 2023. Son titre concerne la compétence territoriale ; son énoncé 8 contient une déclaration sur le travail du demandeur. Ces éléments se rapportent à la date et au contenu de la dénonciation décrits au §234.",
            "EN_ETABLIT_UNE_PARTIE",
            "Ce scan ne date pas la connaissance du demandeur, la réception par sa procureure ou l'inscription au plumitif. Il ne tranche pas les qualifications et effets de prescription allégués, l'intention de nuire ni le préjudice.",
            autres=[{"texte": "Le demandeur a fait le choix de ne pas travailler pour subvenir aux besoins de ses enfants;", "localisation": "P-40, page 2/5, énoncé 8"}])

    t = corps(fs[469])
    ajouter(469, extrait(t, "Nous avons reçu ce document", "Nous aurons l’occasion"),
            "P-105, Date: Tue, 25 Jul 2023 13:57:20 +0000 ; From Luneedka Lili Philémon, To Louis Philippe David ; premier paragraphe du corps. Message antérieur cité : Envoyé : 21 juillet 2023 16:49.",
            "Le courriel daté du 25 juillet est adressé au demandeur et lui communique la demande de transfert. Le même corps reproduit un envoi de Me Ayoub à Me Philémon daté du 21 juillet. Il documente donc la communication au client du 25 juillet et distingue cet événement de l'envoi antérieur à la procureure.",
            "EN_ETABLIT_UNE_PARTIE",
            "La date précise à laquelle la procureure a effectivement reçu le document n'est pas indiquée par la phrase Nous avons reçu. Le courriel ne prouve pas, à lui seul, l'absence de connaissance antérieure du demandeur ni l'heure de sa lecture. Le plumitif et les effets juridiques ne sont pas établis par cette pièce.",
            ecarts=[{"type": "DATE", "description": "Le §234 rattache au 25 juillet la réception par la procureure et la connaissance du demandeur. La pièce distingue un envoi à la procureure le 21 juillet et le courriel au client le 25 ; elle ne dit pas explicitement reçu par la procureure le 25. C'est une distinction documentaire à valider, sans déduire la date effective de réception ou de connaissance."}],
            autres=[{"texte": "Envoyé : 21 juillet 2023 16:49", "localisation": "En-tête reproduit du message antérieur dans le corps de P-105"}])

    ajouter(470, "Attendu que les parties, après le début de l’audition, se sont entendues à ce qu’un jugement soit rendu avec les conclusions suivantes:",
            "P-34, page 3/3, premier attendu ; date 2019-11-04 au pied de la page 1 et en-tête des pages 2–3.",
            "Le procès-verbal du 4 novembre 2019 contient expressément la mention d'une entente des parties. La page 2 rapporte également une restriction des propos portant sur les événements antérieurs à 2016. La relation porte sur ces mentions documentaires effectivement présentes.",
            "EN_ETABLIT_UNE_PARTIE",
            "La pièce n'établit pas que personne ne reconnaît l'entente mentionnée, ni à elle seule la fermeture de toute voie normale de contestation. Elle ne documente pas les conditions économiques de 2020 ou les effets juridiques invoqués au §235.",
            autres=[{"texte": "Le Tribunal informe Monsieur de ne pas parler de ce qui s’est passé avant 2016.", "localisation": "P-34, page 2/3, repère 10h17:04"}])

    t = corps(fs[471])
    ajouter(471, extrait(t, "suite au dernier jugement", ", penses-tu"),
            "P-37, Date: Mon, 17 Feb 2020 12:53:16 -0500 ; Louis Philippe David à Marie-Josée Ayoub ; premier paragraphe après Salut MJ.",
            "Le demandeur écrit en février 2020 que son compte a été saisi et annonce une annulation prochaine de son passeport qui l'empêcherait de travailler. Cette déclaration datée éclaire le contexte financier et professionnel du §235.",
            "ECLAIRE_SEULEMENT",
            "La pièce constate ces propos du demandeur ; elle ne mesure pas ses revenus, ne constate pas une absence de domicile ou des prestations de dernier recours et ne démontre pas l'impossibilité en fait d'agir alléguée.")

    t = corps(fs[472])
    ajouter(472, extrait(t, "J'arrives", "\n\nIl va"),
            "P-38, Date: Fri, 17 Apr 2020 15:38:02 -0400 ; Louis Philippe David à Marie-Josée Ayoub ; premier paragraphe.",
            "Le courriel contient les déclarations du demandeur sur la fin de ses économies et de son bail, ainsi que sur le travail recherché. Ces propos contemporains éclairent le contexte de précarité allégué pour 2020.",
            "ECLAIRE_SEULEMENT",
            "Le courriel ne constate pas à lui seul la perte effective du logement, le niveau exact des revenus, des mesures de dernier recours ou l'impossibilité d'agir. La proposition d'entente qu'il contient en avril 2020 n'est pas identifiée à l'entente de 2019 mentionnée au jugement.",
            autres=[{"texte": extrait(t, "Il va être temps", "\n\nJe penses"), "localisation": "P-38, deuxième paragraphe du corps"}])

    t = corps(fs[473])
    ajouter(473, extrait(t, "Vu les circonstances", "\n\nPuisque"),
            "P-99.1, membre de P-99 citée en bloc ; Date: Wed, 25 Mar 2020 12:43:54 -0400 ; Louis Philippe David à Katie Desbiens ; premier paragraphe.",
            "Le demandeur annonce à la destinataire qu'il ne serait pas en mesure de maintenir son occupation du logement dont il se dit alors locataire. La pièce documente cette démarche et ce propos au sujet du logement en mars 2020.",
            "ECLAIRE_SEULEMENT",
            "Cette annonce au conditionnel ne date pas un départ effectif et ne constate pas une absence de domicile fixe. Elle ne documente ni les prestations de dernier recours ni l'impossibilité d'agir.",
            ecarts=[{"type": "SENS", "description": "Le texte parle d'une occupation à maintenir au conditionnel et se présente comme locataire au moment de l'envoi ; il n'énonce pas une absence de domicile déjà réalisée. Portée documentaire limitée au regard de l'état allégué au §235."}])

    t = corps(fs[474])
    ajouter(474, extrait(t, "Votre bail a été renouvelé", "\nJe sais"),
            "P-99.2, membre de P-99 citée en bloc ; Date: Fri, 08 May 2020 11:26:32 -0400 ; Katie Desbiens à Louis Philippe David ; deux premières phrases après la salutation.",
            "La destinataire répond que le bail a été renouvelé et prend fin le 30 juin 2021 ; elle décrit ensuite une tentative de relocation pour juillet permettant de libérer le locataire. La relation porte sur cet échange de logement, pas sur une conclusion de fait sur sa situation ultérieure.",
            "ECLAIRE_SEULEMENT",
            "La réponse ne constate ni le départ effectif, ni sa date, ni l'absence de domicile fixe ou de revenu suffisant. Elle ne démontre pas l'impossibilité d'agir alléguée.",
            ecarts=[{"type": "SENS", "description": "La réponse décrit un bail en cours et une démarche possible de relocation ; ce contenu ne doit pas être présenté comme une attestation d'absence de domicile. Il ne suffit pas non plus à exclure une perte ultérieure du logement."}],
            autres=[{"texte": extrait(t, "Il est d’accord", "\nIl serait bien"), "localisation": "P-99.2, paragraphe sur le concierge et la relocation"}])

    verifier_perimetre_pilote(lire_json(ARTEFACTS / "constat/constat.json"), ps)
    ecrire_identique_ou_nouveau(ARTEFACTS / "pilote/propositions.json", octets_json(ps))
    return ps


if __name__ == "__main__":
    print(f"{len(preparer())} propositions préparées, aucune validation LP")
