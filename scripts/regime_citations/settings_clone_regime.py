"""Réglages pointant sur le CLONE de la base du dossier — jamais la production.

Le .env du projet est chargé avec `override=True` : une variable d'environnement
ne peut pas changer DB_NAME. Ce module reprend les réglages locaux et ne change
que le nom de la base.
"""
import os

from mysite.settings import *  # noqa: F401,F403

NOM = os.environ.get("REGIME_CLONE_DB", "court_quote_regime_clone")
if NOM == "court_project_pg":
    raise RuntimeError("settings_clone_regime ne vise jamais la base réelle")
DATABASES["default"]["NAME"] = NOM  # noqa: F405
DATABASES["default"]["TEST"] = {"NAME": "test_" + NOM}  # noqa: F405
