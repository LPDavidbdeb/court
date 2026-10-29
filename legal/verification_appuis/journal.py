"""VA06 : journal JSONL en ajout seulement, avec verrou et chaîne de versions."""
import fcntl
import json
import os

from .commun import Refus, chemin_sortie
from .observations import valider_observation

AUTEUR_AGENT = "CODEX"


def cle_cible(o):
    return tuple(sorted(o["liens"]))


def ajouter_version(chemin, o):
    valider_observation(o)
    p = chemin_sortie(chemin)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a+b") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0)
        avant = f.read()
        anciennes = [valider_observation(json.loads(ligne)) for ligne in avant.splitlines()]
        if any(a["id"] == o["id"] for a in anciennes):
            raise Refus("ID de version déjà enregistré")
        cible = [a for a in anciennes if cle_cible(a) == cle_cible(o)]
        attendu = cible[-1]["id"] if cible else None
        if o.get("remplace") != attendu:
            raise Refus(f"Version précédente attendue : {attendu}")
        if avant and not avant.endswith(b"\n"):
            raise Refus("Journal incomplet : dernière ligne sans terminaison")
        ligne = (json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
        f.seek(0, os.SEEK_END)
        f.write(ligne)
        f.flush()
        os.fsync(f.fileno())
    return o


def proposer(chemin, observation, constat=None):
    if observation.get("avancement") != "PROPOSE" or observation.get("auteur") != AUTEUR_AGENT:
        raise Refus("Cette voie ajoute uniquement une proposition de CODEX")
    if constat is not None:
        from .liasses import verifier_rattachement
        verifier_rattachement(observation, constat)
    elif len(observation["liens"]) > 1:
        raise Refus("Le constat est obligatoire pour une observation de liasse")
    return ajouter_version(chemin, observation)
