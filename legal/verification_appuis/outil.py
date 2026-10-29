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
    p = commandes.add_parser("verifier_ancrage", help="VA02 : refuser les écarts au constat")
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument("--fixture")
    source.add_argument("--reel", action="store_true")
    p.add_argument("--accord")
    p.add_argument("--concordance", required=True)
    p.add_argument("--constat", required=True)
    args = parser.parse_args(argv)
    try:
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
