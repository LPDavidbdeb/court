"""Préparer un envoi, le vérifier, en produire le bordereau de l'art. 134 C.p.c.

Ce module n'envoie rien. Il fait trois choses, et refuse d'en faire une
quatrième :

    empreinter    — SHA-256 de chaque fichier joint, parce que c'est
                    « l'information nécessaire pour permettre au destinataire de
                    vérifier l'intégrité de la transmission » (art. 134).
    verifier      — contrôler ce qui est mécaniquement contrôlable, SIGNALER ce
                    qui ne l'est qu'approximativement, et EXIGER une attestation
                    humaine pour ce qui relève du jugement.
    bordereau     — rendre le bordereau, provisoire avant l'envoi, définitif
                    après, une fois l'heure réelle connue.

LA DISTINCTION QUI PORTE TOUT LE MODULE. Un contrôle automatique qui prétend
couvrir un jugement humain est pire que pas de contrôle : il rassure. Les
vérifications sont donc de trois natures, jamais confondues :

    BLOCAGE       fait objectif, vérifiable sans interprétation. Rien ne part.
    SIGNALEMENT   indice lexical. Souvent un faux positif. On regarde, on passe.
    ATTESTATION   jugement que seule une personne peut porter. La commande ne
                  peut pas le vérifier ; elle peut refuser de continuer tant
                  qu'il n'est pas porté, nommément, par le demandeur.
"""

import hashlib
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from case_manager.models import DestinataireInstance

# Le délai de refroidissement de la règle n° 2 : « jamais de réponse sur le fond
# le jour même ». Mesuré entre la dernière écriture du fichier et l'envoi.
REFROIDISSEMENT_HEURES = 12

# Les attestations que la machine ne peut pas porter. Tirées de
# `legal/instance/sortants/README.md`.
ATTESTATIONS = {
    "delai": "Rien ne m'oblige à envoyer ceci aujourd'hui.",
    "relu_a_froid": "Relu à froid, pas dans la demi-heure de la rédaction.",
    "aucun_fait_nouveau": "Aucun fait nouveau qui ne soit déjà allégué ou appuyé par une pièce.",
    "aucun_engagement": "Aucun engagement de délai, de démarche ou de position décidé à chaud.",
    "ton": "Des actes datés, jamais des personnes. Relu en se demandant : cette phrase, citée seule dans leur requête en rejet, me nuit-elle ?",
}

# Signalements lexicaux. Chacun renvoie à la règle qu'il approche — jamais à une
# conclusion. La liste fermée est `legal/instance/pieges.md` § D.
SIGNALEMENTS = [
    (r"21\s+juillet\s+2023",
     "pieges § D.1 — le 21 juillet 2023 ne se traite jamais comme point de départ de la prescription."),
    (r"\b(annuler|révis\w+|rétract\w+)\b[^.]{0,80}\bjugement\b",
     "pieges § D.2 — la demande ne vise pas à annuler ni à réviser un jugement."),
    (r"\bjugement\b[^.]{0,80}\b(annuler|révis\w+|rétract\w+)",
     "pieges § D.2 — la demande ne vise pas à annuler ni à réviser un jugement."),
    (r"\bexercice normal\b",
     "pieges § D.3 — ne pas concéder que les actes relèveraient du seul exercice normal d'un mandat."),
    (r"\b(protect\w+|protég\w+)\b[^.]{0,60}\b(sans couch\w+|éviction)",
     "pieges § D.4 — ne jamais concéder un effet protecteur propre."),
    (r"\bdiffamation\b",
     "pieges § D.5 — toute caractérisation en diffamation pure fait basculer sous le délai d'un an."),
    (r"\b(Alexia|Nicolas)\b",
     "pieges § B — le canal des enfants est séparé. Aucune mention dans un écrit d'instance."),
    (r"!",
     "Ton. Un point d'exclamation dans une correspondance d'instance se cite seul."),
]


def empreinte(chemin):
    """SHA-256 d'un fichier, lu par blocs."""
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloc)
    return h.hexdigest()


def destinataires_valides(jour=None):
    """Les destinataires dont l'adresse est valide ce jour-là."""
    jour = jour or date.today()
    return [d for d in DestinataireInstance.objects.all() if d.est_valide_le(jour)]


def verifier(transmission, attestations=None, maintenant=None, fichiers=None, copies=None):
    """Produit le rapport de vérification préalable.

    `attestations` : les clés de ATTESTATIONS que le demandeur porte nommément.
    Les autres sont rapportées comme manquantes — ce qui bloque.
    """
    maintenant = maintenant or datetime.now(timezone.utc)
    attestations = set(attestations or [])
    blocages, signalements = [], []

    # --- BLOCAGE : l'adresse du destinataire est-elle valide aujourd'hui ? ---
    jour = maintenant.date()
    dest = transmission.destinataire
    if not dest.est_valide_le(jour):
        blocages.append(
            f"Adresse périmée : {dest.courriel} n'est plus l'adresse de "
            f"{dest.partie} au {jour.isoformat()} "
            f"(valide du {dest.valide_du} au {dest.valide_au or '—'})."
        )
        # La relève peut porter un AUTRE nom : quand une partie se fait représenter,
        # c'est le cabinet qui devient destinataire. On cherche donc aussi par
        # `pour_le_compte_de`, sans quoi on bloque sans dire où écrire.
        vise = dest.pour_le_compte_de or dest.partie
        for autre in DestinataireInstance.objects.all():
            if (autre.pour_le_compte_de or autre.partie) != vise:
                continue
            if autre.pk != dest.pk and autre.est_valide_le(jour):
                qui = (f"{autre.partie}, avocats de {autre.pour_le_compte_de}"
                       if autre.qualite == "AVOCAT" else autre.partie)
                blocages.append(
                    f"  → écrire plutôt à {qui} <{autre.courriel}> — {autre.source}")

    # --- BLOCAGE : le fichier source existe et porte le numéro de dossier ---
    source = Path(transmission.fichier_source)
    if not source.exists():
        blocages.append(f"Fichier source introuvable : {source}")
        texte = ""
    else:
        texte = source.read_text(encoding="utf-8")
        if transmission.dossier not in texte:
            blocages.append(
                f"Le numéro de dossier {transmission.dossier} n'apparaît pas dans le fichier source."
            )

    # --- BLOCAGE : pas de mise en copie croisée entre parties ---
    #
    # La vérification porte sur les DESTINATAIRES RÉELS, jamais sur le corps du
    # texte. La lettre à Élise cite l'adresse de Timmons Séguin Tremblay parce
    # que l'art. 147 al. 3 C.p.c. l'y oblige : « le demandeur est tenu d'informer
    # toutes les parties […] du nom des avocats qui les représentent ». Bloquer
    # sur une mention reviendrait à interdire d'exécuter une obligation.
    cible = dest.pour_le_compte_de or dest.partie
    etrangeres = set()
    for adresse in (copies or []):
        for d in DestinataireInstance.objects.all():
            if d.courriel.lower() == adresse.strip().lower():
                autre = d.pour_le_compte_de or d.partie
                if autre != cible:
                    etrangeres.add(autre)
    if etrangeres:
        blocages.append(
            "Mise en copie croisée : " + ", ".join(sorted(etrangeres))
            + f" figure en copie d'un envoi destiné à {cible}. "
            "Un envoi par partie, jamais de croisement."
        )

    # Mention d'une adresse étrangère dans le corps : signalement, pas blocage.
    adresses_du_texte = set(re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", texte))
    for d in DestinataireInstance.objects.all():
        autre = d.pour_le_compte_de or d.partie
        if d.courriel in adresses_du_texte and autre != cible:
            signalements.append({
                "motivation": f"Le corps cite l'adresse de {autre}. Légitime si c'est "
                              "l'information due par l'art. 147 al. 3 ; à vérifier sinon.",
                "extrait": d.courriel,
            })

    # --- BLOCAGE : refroidissement ---
    if source.exists():
        ecrit_le = datetime.fromtimestamp(source.stat().st_mtime, tz=timezone.utc)
        ecoule = maintenant - ecrit_le
        if ecoule < timedelta(hours=REFROIDISSEMENT_HEURES):
            reste = timedelta(hours=REFROIDISSEMENT_HEURES) - ecoule
            message = (
                f"Refroidissement : le fichier a été écrit il y a "
                f"{int(ecoule.total_seconds() // 3600)} h, soit moins que les "
                f"{REFROIDISSEMENT_HEURES} h de la règle n° 2 — reste "
                f"{int(reste.total_seconds() // 3600) + 1} h."
            )
            # L'horodatage du fichier est un indice, pas la vérité : une relecture
            # à froid suivie d'une coquille corrigée le remet à zéro. L'attestation
            # prime donc — mais le dépassement reste CONSIGNÉ au rapport, nommément.
            # Ce n'est pas un contournement : c'est le demandeur qui en répond.
            if "relu_a_froid" in attestations:
                signalements.append({
                    "motivation": message,
                    "extrait": "Levé par l'attestation « relu_a_froid », portée par le demandeur.",
                })
            else:
                blocages.append(message + " Ou porter l'attestation « relu_a_froid ».")

    # --- BLOCAGE : chaque fichier joint existe et son empreinte concorde ---
    if fichiers is None:
        fichiers = transmission.fichiers.all() if transmission.pk else []
    for f in fichiers:
        p = Path(f.chemin)
        if not p.exists():
            blocages.append(f"Pièce jointe introuvable : {f.chemin}")
        elif empreinte(p) != f.sha256:
            blocages.append(
                f"Empreinte divergente pour {f.nom_transmis} : le fichier a changé depuis la préparation."
            )

    # --- SIGNALEMENTS lexicaux ---
    for motif, motivation in SIGNALEMENTS:
        for m in re.finditer(motif, texte, flags=re.IGNORECASE):
            debut = max(0, m.start() - 60)
            signalements.append({
                "motivation": motivation,
                "extrait": " ".join(texte[debut:m.end() + 60].split()),
            })

    # --- ATTESTATIONS manquantes ---
    manquantes = [k for k in ATTESTATIONS if k not in attestations]
    for k in manquantes:
        blocages.append(f"Attestation non portée — « {ATTESTATIONS[k]} » (clé : {k})")

    return {
        "verifie_le": maintenant.isoformat(),
        "blocages": blocages,
        "signalements": signalements,
        "attestations_portees": sorted(attestations),
        "attestations_manquantes": manquantes,
    }


def bordereau(transmission, horodatage=None, fichiers=None):
    """Rend le bordereau de l'art. 134 C.p.c.

    `horodatage` absent → bordereau PROVISOIRE : l'heure de la transmission
    n'est pas encore connue, et le texte le dit plutôt que d'inventer.
    """
    d = transmission.destinataire
    definitif = horodatage is not None
    if definitif:
        local = horodatage.astimezone()
        # %B suit la locale du système (« October ») : le mois s'écrit à la main.
        mois = ("janvier", "février", "mars", "avril", "mai", "juin", "juillet",
                "août", "septembre", "octobre", "novembre", "décembre")[local.month - 1]
        quand = f"{local.day} {mois} {local.year}, {local.hour} h {local.minute:02d}"
        ligne_date = f"**Date et heure de la transmission** : le {quand}"
    else:
        ligne_date = (
            "**Date et heure de la transmission** : *(à estampiller après l'envoi — "
            "l'art. 134 exige l'heure et les minutes réelles)*"
        )

    qualite = (
        f"Avocats de {d.pour_le_compte_de}" if d.qualite == "AVOCAT"
        else "Défenderesse, agissant en son propre nom"
    )

    lignes = [
        "# BORDEREAU D'ENVOI PAR COURRIEL",
        "### (article 134 C.p.c.)",
        "",
        f"**Nature du document transmis** : {transmission.nature}",
        f"**Numéro de dossier** : {transmission.dossier}",
        "",
        "**Expéditeur**",
        "",
        "Louis-Philippe David, demandeur agissant en son propre nom",
        "465, avenue Curzon, Saint-Lambert (Québec) J4P 2V6",
        "louisphilippe.david@gmail.com",
        "*(Le demandeur n'a pas de téléphone ; le courriel est son seul moyen de communication.)*",
        "",
        "**Destinataire**",
        "",
        d.partie,
        qualite,
    ]
    if d.adresse_postale:
        lignes += [d.adresse_postale.strip()]
    lignes += [
        d.courriel,
        "",
        f"**Lieu de la transmission** : {transmission.lieu}",
        ligne_date,
        "",
    ]

    if fichiers is None:
        fichiers = transmission.fichiers.all() if transmission.pk else []
    fichiers = list(fichiers)
    if fichiers:
        lignes += [
            "**Vérification de l'intégrité de la transmission**",
            "",
            "Les empreintes SHA-256 ci-dessous permettent au destinataire de vérifier",
            "l'intégrité des fichiers transmis.",
            "",
            "| Cote | Fichier | Octets | SHA-256 |",
            "|---|---|---|---|",
        ]
        for f in fichiers:
            lignes.append(f"| {f.cote or '—'} | {f.nom_transmis} | {f.octets} | `{f.sha256}` |")
        lignes.append("")
    else:
        lignes += ["**Nombre de documents transmis** : aucune pièce jointe.", ""]

    lignes += [
        "Cet envoi vaut notification conformément aux articles 133 et 134 du Code",
        "de procédure civile.",
    ]
    if not definitif:
        lignes += ["", "> ⚠️ **BORDEREAU PROVISOIRE** — à régénérer après l'envoi."]
    return "\n".join(lignes)
