"""Vérifie un courriel ENVOYÉ : destinataires, et chaque pièce jointe contre son original.

    python legal/instance/outils/verifier_envoi.py --message-id <id Gmail> \
        --attendu 00_Index_des_pieces.pdf=~/Documents/Envoi_.../00_Index_des_pieces.pdf \
        --attendu SHA256SUMS=~/Documents/Envoi_.../SHA256SUMS

    # ou, sans --attendu, pour simplement lister ce qui est parti :
    python legal/instance/outils/verifier_envoi.py --message-id <id> --lister

POURQUOI. Le contrôle doit porter sur le **MIME du message réellement parti**,
jamais sur le brouillon ni sur le fichier du disque. Le 5 novembre 2026, ce
contrôle a attrapé deux défauts qu'aucune autre vérification n'aurait vus :

1. Apple Mail convertissait `SHA256SUMS` — fichier **sans extension**, donc
   traité comme du texte — en remplaçant chaque LF par CRLF. 911 conversions,
   911 octets de plus, et une empreinte qui ne correspondait plus à celle que
   le bordereau atteste. La destinataire aurait lancé `shasum -c` et les
   911 lignes auraient échoué.
2. Le risque de croiser les bordereaux entre destinataires.

RÈGLE QUI EN DÉCOULE : ne jamais joindre un fichier texte sans extension depuis
un client de courrier de bureau ; passer par l'interface web, qui téléverse les
octets tels quels. Et vérifier après l'envoi, pas avant.

Lecture seule : le scope OAuth du projet est `gmail.readonly`.
"""
import argparse
import base64
import email
import hashlib
import os
import sys
from email import policy
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
RACINE = Path(__file__).resolve().parents[3]
TOKEN = RACINE / "storage/credentials/token.json"
CRLF = b"\r\n"


def service():
    creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN.write_text(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def message(mid):
    brut = service().users().messages().get(userId="me", id=mid, format="raw").execute()
    return email.message_from_bytes(base64.urlsafe_b64decode(brut["raw"]), policy=policy.default)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--message-id", required=True, help="id Gmail du message envoyé")
    ap.add_argument("--attendu", action="append", default=[],
                    help="nom_joint=chemin/vers/original (répétable)")
    ap.add_argument("--lister", action="store_true", help="lister sans comparer")
    a = ap.parse_args()

    refs = {}
    for brut in a.attendu:
        nom, _, chemin = brut.partition("=")
        if not chemin:
            sys.exit(f"--attendu veut nom=chemin, reçu : {brut}")
        refs[nom] = Path(chemin).expanduser()

    m = message(a.message_id)
    print(f"  Date   : {m.get('Date')}")
    print(f"  De     : {m.get('From')}")
    print(f"  À      : {m.get('To')}")
    print(f"  Cc     : {m.get('Cc')}   Cci : {m.get('Bcc')}")
    print(f"  Objet  : {m.get('Subject')}")
    print(f"  Message-ID : {m.get('Message-ID')}")
    print("\n  Pièces jointes :")

    vus, echecs = set(), 0
    for p in m.walk():
        nom = p.get_filename()
        if not nom:
            continue
        data = p.get_payload(decode=True)
        vus.add(nom)
        h = hashlib.sha256(data).hexdigest()
        ref = refs.get(nom)
        if a.lister or ref is None:
            etat = "— (pas d'original fourni)" if not a.lister else ""
        elif not ref.exists():
            etat = f"⚠ original introuvable : {ref}"
            echecs += 1
        else:
            o = ref.read_bytes()
            if data == o:
                etat = "✅ identique à l'original"
            else:
                ecart = len(data) - len(o)
                crlf = data.count(CRLF)
                etat = f"🔴 DIFFÈRE ({ecart:+d} octets"
                if crlf and not o.count(CRLF):
                    etat += f", {crlf} CRLF — conversion texte par le client de courrier"
                etat += ")"
                echecs += 1
        print(f"   - {nom:<56} {len(data):>8} o  {h[:16]}  {etat}")

    for nom in refs:
        if nom not in vus:
            print(f"   🔴 MANQUANTE : {nom}")
            echecs += 1

    print()
    if a.lister:
        print("  (mode liste : aucune comparaison)")
    elif echecs:
        sys.exit(f"  🔴 {echecs} écart(s). Ne pas considérer l'envoi comme conforme.")
    else:
        print("  ✅ Envoi conforme : destinataires et pièces jointes vérifiés sur le message parti.")


if __name__ == "__main__":
    main()
