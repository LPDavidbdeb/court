"""
Réglages Django de la bascule du régime des citations.

La base visée est donnée explicitement par BASCULE_BASE, quel que soit le .env de l'arbre :
les mêmes commandes servent à la base d'essai et à la base réelle, et la cible ne dépend d'aucune
variable implicite. La base réelle n'est acceptée qu'avec BASCULE_REELLE_CONFIRMEE=oui.
L'hôte, le port et les identifiants viennent des réglages locaux ; bascule_fumee.py vérifie
ensuite, par la connexion elle-même, la base, le port et l'identifiant du serveur.

Plan : docs/modele_preuve/BASCULE_REGIME_ETAPE1.md.
"""
import os

from mysite.settings import *  # noqa: F401,F403

NOM = os.environ.get("BASCULE_BASE")
if not NOM:
    raise RuntimeError("BASCULE_BASE absent : aucune base visée")
if NOM == "court_project_pg" and os.environ.get("BASCULE_REELLE_CONFIRMEE") != "oui":
    raise RuntimeError("la base réelle n'est visée qu'avec BASCULE_REELLE_CONFIRMEE=oui")
DATABASES["default"]["NAME"] = NOM  # noqa: F405
DATABASES["default"]["TEST"] = {"NAME": "test_" + NOM}  # noqa: F405
