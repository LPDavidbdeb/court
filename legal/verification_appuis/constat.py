"""VA01 : capture sans interprétation et sans mutation de la source."""
import copy
from contextlib import closing
import json
from pathlib import Path
import re
import sqlite3
import unicodedata

from .commun import Refus, empreinte, ecrire_identique_ou_nouveau, index_unique, octets_json


def normaliser_appariement(texte):
    # Utilisé uniquement pour l'appariement ; le texte capturé reste intact.
    texte = unicodedata.normalize("NFC", texte or "")
    return " ".join(re.sub(r"[*_`#]", "", texte).split()).casefold()


def numero_imprime(enonce, concordance):
    texte = normaliser_appariement(enonce["texte"])
    candidats = [ligne for ligne in concordance["lignes"]
                 if texte.startswith(normaliser_appariement(ligne["incipit"]))]
    if len(candidats) > 1:
        raise Refus(f"Appariement imprimé ambigu pour l'énoncé {enonce['id']}")
    if not candidats:
        return None
    numero = str(candidats[0]["numero_imprime"])
    stocke = enonce.get("numero_stocke")
    if stocke and str(stocke) != numero:
        raise Refus(f"Numéro stocké divergent pour l'énoncé {enonce['id']} : {stocke} / {numero}")
    return numero


def capturer(source, concordance):
    enonces = copy.deepcopy(source["enonces"])
    liens = copy.deepcopy(source["liens"])
    cotes = copy.deepcopy(source["cotes"])
    par_enonce, par_cote = index_unique(enonces), index_unique(cotes)
    index_unique(liens)
    for enonce in enonces:
        enonce["numero_imprime"] = numero_imprime(enonce, concordance)
        enonce["empreinte_texte"] = empreinte(enonce["texte"].encode())
    for lien in liens:
        if lien["statement_id"] not in par_enonce or lien["entree_id"] not in par_cote:
            raise Refus(f"Lien {lien['id']} hors du constat")
    return {
        "schema": "va-constat/1", "document_id": source.get("document_id", 9),
        "origine": source.get("origine", "fixture-synthetique"),
        "concordance_empreinte": empreinte(octets_json(concordance)),
        "enonces": sorted(enonces, key=lambda e: (e["ordre"], e["id"])),
        "liens": sorted(liens, key=lambda e: e["id"]),
        "cotes": sorted(cotes, key=lambda e: (e.get("rang") or 0, e.get("sous_rang") or 0, e["id"])),
    }


def enregistrer_constat(constat, repertoire):
    contenu = octets_json(constat)
    repertoire = Path(repertoire)
    ecrire_identique_ou_nouveau(repertoire / "constat.json", contenu)
    ecrire_identique_ou_nouveau(repertoire / "SHA256SUMS",
                              f"{empreinte(contenu)}  constat.json\n".encode())
    return empreinte(contenu)


def lire_fixture(chemin):
    """Une base SQLite synthétique, ouverte par le moteur en lecture seule."""
    uri = Path(chemin).resolve().as_uri() + "?mode=ro"
    with closing(sqlite3.connect(uri, uri=True)) as connexion:
        return {nom: [json.loads(row[0]) for row in connexion.execute(f"SELECT contenu FROM {nom} ORDER BY id")]
                for nom in ("enonces", "liens", "cotes")}
