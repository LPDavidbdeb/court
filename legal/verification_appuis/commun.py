"""Formats déterministes et écritures limitées aux nouveaux artefacts."""
import hashlib
import json
from pathlib import Path
import tempfile

RACINE = Path(__file__).resolve().parents[2]
ARTEFACTS = RACINE / "legal/verification_appuis"


class Refus(ValueError):
    """Un prérequis n'est pas satisfait ; aucune réparation implicite."""


def octets_json(objet):
    return (json.dumps(objet, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def empreinte(octets):
    return hashlib.sha256(octets).hexdigest()


def lire_json(chemin):
    return json.loads(Path(chemin).read_text(encoding="utf-8"))


def chemin_sortie(chemin):
    cible = Path(chemin).resolve()
    if not any(cible.is_relative_to(p.resolve()) for p in (ARTEFACTS, Path(tempfile.gettempdir()))):
        raise Refus("Sortie autorisée uniquement dans legal/verification_appuis/ ou le temporaire de test")
    return cible


def ecrire_identique_ou_nouveau(chemin, contenu):
    cible = chemin_sortie(chemin)
    cible.parent.mkdir(parents=True, exist_ok=True)
    if cible.exists():
        if cible.read_bytes() != contenu:
            raise Refus(f"Artefact existant différent, écrasement refusé : {cible.name}")
        return
    with cible.open("xb") as f:
        f.write(contenu)


def index_unique(lignes, champ="id"):
    resultat = {}
    for ligne in lignes:
        cle = ligne[champ]
        if cle in resultat:
            raise Refus(f"Identifiant dupliqué : {champ}={cle}")
        resultat[cle] = ligne
    return resultat
