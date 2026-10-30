"""Entrée autonome : python -m legal.verification_appuis.outil --help."""
import argparse
import sys

from .commun import Refus, lire_json
from .constat import capturer, enregistrer_constat, lire_fixture


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commandes = parser.add_subparsers(dest="commande", required=True)
    p = commandes.add_parser("instantane", help="VA01 : générer un instantané déterministe")
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument("--fixture")
    source.add_argument("--reel", action="store_true")
    p.add_argument("--accord")
    p.add_argument("--concordance", required=True)
    p.add_argument("--sortie", required=True)
    p = commandes.add_parser("proposer", help="VA06 : ajouter une proposition CODEX")
    p.add_argument("--observation", required=True)
    p.add_argument("--fichier", required=True)
    p.add_argument("--accord", required=True)
    p = commandes.add_parser("decision_lp", help="VA07 : appliquer une décision fournie par LP")
    p.add_argument("--decision", required=True)
    p.add_argument("--fichier", required=True)
    p = commandes.add_parser("couverture", help="VA11 : avancement sans validation inventée")
    p.add_argument("--constat", required=True)
    p.add_argument("--observations", required=True)
    p.add_argument("--accord", required=True)
    p.add_argument("--sortie", required=True)
    p.add_argument("--paragraphes", nargs="*")
    p = commandes.add_parser("image", help="VA12 : exports JSON et Markdown cohérents")
    p.add_argument("--constat", required=True)
    p.add_argument("--observations", required=True)
    p.add_argument("--accord", required=True)
    p.add_argument("--sortie", required=True)
    p.add_argument("--paragraphes", nargs="*")
    p = commandes.add_parser("derives", help="VA13 : fraîcheur des textes, liens et supports")
    p.add_argument("--constat", required=True)
    p.add_argument("--observations", required=True)
    p.add_argument("--accord", required=True)
    p.add_argument("--sortie", required=True)
    p.add_argument("--reel", action="store_true")
    p.add_argument("--concordance")
    p = commandes.add_parser("paragraphes_fragments", help="VA15 : liste issue des fragments validés")
    p.add_argument("--constat", required=True)
    p.add_argument("--fragments", required=True)
    p.add_argument("--accord", required=True)
    p.add_argument("--sortie", required=True)
    p = commandes.add_parser("valider_fichier", help="VA04 : contrôler la forme des observations")
    p.add_argument("--fichier", required=True)
    p = commandes.add_parser("fiches", help="VA05 : préparer les fiches et vérifier les octets")
    p.add_argument("--constat", required=True)
    p.add_argument("--manifeste", required=True)
    p.add_argument("--accord", required=True)
    p.add_argument("--sortie", required=True)
    p = commandes.add_parser("verifier_ancrage", help="VA02 : refuser les écarts au constat")
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument("--fixture")
    source.add_argument("--reel", action="store_true")
    p.add_argument("--accord")
    p.add_argument("--concordance", required=True)
    p.add_argument("--constat", required=True)
    p = commandes.add_parser("liste_travail", help="VA03 : inventaire priorisé")
    p.add_argument("--constat", required=True)
    p.add_argument("--accord", required=True)
    p.add_argument("--sortie", required=True)
    args = parser.parse_args(argv)
    try:
        if args.commande == "paragraphes_fragments":
            import json
            from .source_django import verifier_accord
            from .ancrage import charger_constat
            from .fragments import liste_paragraphes_fragments
            from .commun import ecrire_identique_ou_nouveau, octets_json
            from pathlib import Path
            verifier_accord(args.accord, "VA15")
            p = Path(args.fragments)
            fragments = [json.loads(l) for l in p.read_text().splitlines()] if p.exists() else []
            r = liste_paragraphes_fragments(charger_constat(args.constat), fragments)
            p = Path(args.sortie)
            ecrire_identique_ou_nouveau(p / "paragraphes_fragments.json", octets_json(r))
            ecrire_identique_ou_nouveau(p / "paragraphes_fragments.md", ("# Liste issue des fragments validés\n\n" + str(r) + "\n").encode())
            print(f"VA15 : {r['fragments_valides']} fragments validés ; {len(r['paragraphes'])} paragraphes à examiner")
            return 0
        if args.commande == "derives":
            from .source_django import verifier_accord, lire_source_reelle
            from .ancrage import charger_constat
            from .observations import lire_observations
            from .derives import detecter_derives
            from .commun import ecrire_identique_ou_nouveau, octets_json
            from pathlib import Path
            verifier_accord(args.accord, "VA13")
            ancien = charger_constat(args.constat)
            actuel = capturer(lire_source_reelle(args.accord, "VA13"), lire_json(args.concordance)) if args.reel else ancien
            r = detecter_derives(ancien, lire_observations(args.observations), actuel)
            p = Path(args.sortie)
            ecrire_identique_ou_nouveau(p / "derives.json", octets_json(r))
            ecrire_identique_ou_nouveau(p / "derives.md", ("# Dérives et historique\n\n" + str(r) + "\n").encode())
            print(f"VA13 : {len(r['observations_a_revoir'])} observations à revoir ; {r['fichiers_controles']} supports contrôlés")
            return 0
        if args.commande == "image":
            from .source_django import verifier_accord
            from .ancrage import charger_constat
            from .observations import lire_observations
            from .rapports import image_depot, markdown_image
            from .commun import ecrire_identique_ou_nouveau, octets_json
            from pathlib import Path
            verifier_accord(args.accord, "VA12")
            from .derives import detecter_derives
            c, h = charger_constat(args.constat), lire_observations(args.observations)
            d = detecter_derives(c, h)
            image = image_depot(c, h, d["observations_a_revoir"], numeros=args.paragraphes)
            p = Path(args.sortie)
            ecrire_identique_ou_nouveau(p / "image.json", octets_json(image))
            ecrire_identique_ou_nouveau(p / "image.md", markdown_image(image).encode())
            print(f"VA12 : {len(image['paragraphes'])} énoncés ; observations validées et attentes séparées")
            return 0
        if args.commande == "couverture":
            from .source_django import verifier_accord
            from .ancrage import charger_constat
            from .observations import lire_observations
            from .rapports import couverture, markdown_couverture
            from .commun import ecrire_identique_ou_nouveau, octets_json
            from pathlib import Path
            verifier_accord(args.accord, "VA11")
            from .derives import detecter_derives
            c, h = charger_constat(args.constat), lire_observations(args.observations)
            d = detecter_derives(c, h)
            r = couverture(c, h, d["observations_a_revoir"], numeros=args.paragraphes)
            p = Path(args.sortie)
            ecrire_identique_ou_nouveau(p / "couverture.json", octets_json(r))
            ecrire_identique_ou_nouveau(p / "couverture.md", markdown_couverture(r).encode())
            print(f"VA11 : {r['denominateur']} liens ; {r['comptes']}")
            return 0
        if args.commande == "decision_lp":
            from .decisions import decider
            o = decider(args.fichier, lire_json(args.decision))
            print(f"VA07 : décision LP {o['id']} enregistrée")
            return 0
        if args.commande == "proposer":
            from .source_django import verifier_accord
            from .journal import proposer
            verifier_accord(args.accord, "VA06")
            o = proposer(args.fichier, lire_json(args.observation))
            print(f"VA06 : proposition {o['id']} ajoutée, auteur {o['auteur']}")
            return 0
        if args.commande == "fiches":
            from .source_django import verifier_accord
            from .ancrage import charger_constat
            from .fiches import construire_fiches, markdown_fiche
            from .commun import ecrire_identique_ou_nouveau, octets_json
            from pathlib import Path
            verifier_accord(args.accord, "VA05")
            resultat = construire_fiches(charger_constat(args.constat), lire_json(args.manifeste))
            p = Path(args.sortie)
            ecrire_identique_ou_nouveau(p / "fiches.json", octets_json(resultat))
            ecrire_identique_ou_nouveau(p / "fiches.md", ("# Fiches d'examen\n\n" + "\n".join(map(markdown_fiche, resultat["fiches"]))).encode())
            print(f"VA05 : {len(resultat['fiches'])} fiches ; {resultat['fichiers_lus']} fichiers lus ; {len(resultat['liens_avec_obstacle'])} liens avec obstacle explicite")
            return 0
        if args.commande == "valider_fichier":
            from .observations import lire_observations
            lignes = lire_observations(args.fichier)
            print(f"VA04 : {len(lignes)} observations conformes")
            return 0
        if args.commande == "liste_travail":
            from .source_django import verifier_accord
            from .ancrage import charger_constat
            from .travail import liste_travail, markdown_travail
            from .commun import ecrire_identique_ou_nouveau, octets_json
            from pathlib import Path
            verifier_accord(args.accord, "VA03")
            travail = liste_travail(charger_constat(args.constat))
            repertoire = Path(args.sortie)
            ecrire_identique_ou_nouveau(repertoire / "travail.json", octets_json(travail))
            ecrire_identique_ou_nouveau(repertoire / "travail.md", markdown_travail(travail).encode())
            print(f"VA03 : {travail['totaux']}")
            return 0
        if args.commande in ("instantane", "verifier_ancrage"):
            if args.reel:
                from .source_django import lire_source_reelle
                source = lire_source_reelle(args.accord, "VA01" if args.commande == "instantane" else "VA02")
                comptes = tuple(len(source[k]) for k in ("enonces", "liens", "cotes"))
                if comptes != (287, 515, 268):
                    raise Refus(f"VA01 : effectifs réels divergents : {comptes}, attendus (287, 515, 268)")
            else:
                source = lire_fixture(args.fixture)
            constat = capturer(source, lire_json(args.concordance))
            if args.commande == "verifier_ancrage":
                from .ancrage import charger_constat, exiger_ancrage
                exiger_ancrage(charger_constat(args.constat), constat)
                print("VA02 : ancrage conforme, 0 écart")
                return 0
            digest = enregistrer_constat(constat, args.sortie)
            print(f"VA01 : {len(constat['enonces'])} énoncés, {len(constat['liens'])} liens, {len(constat['cotes'])} cotes ; SHA-256 {digest}")
        return 0
    except (Refus, OSError, ValueError, KeyError) as erreur:
        print(f"REFUS : {erreur}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
