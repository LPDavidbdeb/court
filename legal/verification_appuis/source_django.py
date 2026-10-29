"""Lecture réelle opt-in : session PostgreSQL et transaction en lecture seule."""
import os
from pathlib import Path

from .commun import Refus, lire_json


def verifier_accord(chemin, story):
    if not chemin:
        raise Refus(f"{story} : accord explicite de LP absent pour les données réelles")
    accord = lire_json(chemin)
    entree = accord.get("stories", {}).get(story, {})
    if (accord.get("schema") != "va-accords/1" or entree.get("auteur") != "LP"
            or entree.get("mode") != "LECTURE_SEULE" or not entree.get("reference_message")):
        raise Refus(f"{story} : accord LP de lecture seule non attesté")
    return entree


def lire_source_reelle(accord, story="VA01"):
    verifier_accord(accord, story)  # Avant import, configuration ou connexion.
    os.environ["PGOPTIONS"] = (os.environ.get("PGOPTIONS", "") + " -c default_transaction_read_only=on").strip()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    import django
    from django.conf import settings
    configuration = settings.DATABASES["default"]
    if (configuration.get("NAME") != "court_project_pg"
            or configuration.get("ENGINE") != "django.db.backends.postgresql"):
        raise Refus("Seule la base PostgreSQL locale court_project_pg est autorisée")
    # Le mandat interdit le réseau : utiliser exclusivement le socket Unix.
    repertoire_socket = Path("/tmp")
    port = str(configuration.get("PORT") or "5432")
    if not (repertoire_socket / f".s.PGSQL.{port}").exists():
        raise Refus("Socket Unix PostgreSQL local indisponible ; aucun repli réseau")
    configuration["HOST"] = str(repertoire_socket)
    configuration["OPTIONS"] = {"options": "-c default_transaction_read_only=on", "connect_timeout": 5}
    os.environ.pop("PGHOSTADDR", None)
    django.setup()
    from django.db import connection, connections, transaction
    from django.contrib.contenttypes.models import ContentType
    from case_manager.models import AppuiDepotJuillet, BordereauDepotJuillet
    from document_manager.models import Document, LibraryNode, Statement

    if connection.vendor != "postgresql":
        raise Refus("L'adaptateur réel exige PostgreSQL et sa transaction READ ONLY")
    try:
        with transaction.atomic():
            with connection.cursor() as curseur:
                curseur.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY")
                curseur.execute("SHOW transaction_read_only")
                if curseur.fetchone()[0] != "on":
                    raise Refus("Lecture seule PostgreSQL non active")
                curseur.execute("SELECT current_database()")
                if curseur.fetchone()[0] != "court_project_pg":
                    raise Refus("Nom de base réelle non autorisé")
            # get(), sans get_for_model() qui pourrait créer un ContentType.
            ct = ContentType.objects.get(app_label="document_manager", model="statement")
            Document.objects.get(pk=9)
            noeuds = list(LibraryNode.objects.filter(document_id=9, content_type_id=ct.pk)
                          .order_by("path").values("id", "path", "item", "paragraph_number", "object_id"))
            textes = dict(Statement.objects.filter(pk__in=[n["object_id"] for n in noeuds])
                          .values_list("id", "text"))
            enonces = {}
            for ordre, noeud in enumerate(noeuds):
                sid = noeud["object_id"]
                if sid not in textes:
                    raise Refus(f"Occurrence {noeud['id']} sans énoncé")
                occurrence = {"id": noeud["id"], "path": noeud["path"], "item": noeud["item"],
                              "numero_stocke": noeud["paragraph_number"]}
                if sid not in enonces:
                    enonces[sid] = {"id": sid, "occurrence_id": noeud["id"], "ordre": ordre,
                                    "numero_md": noeud["item"], "numero_stocke": noeud["paragraph_number"],
                                    "texte": textes[sid] or "", "occurrences": []}
                enonces[sid]["occurrences"].append(occurrence)
            liens = list(AppuiDepotJuillet.objects.filter(statement_id__in=enonces)
                         .order_by("id").values("id", "statement_id", "entree_id", "cote_citee", "via_liasse"))
            lignes = list(BordereauDepotJuillet.objects.filter(cote__isnull=False).exclude(cote="")
                          .order_by("id").values("id", "cote", "cote_racine", "rang", "sous_rang",
                                                 "content_type__app_label", "content_type__model", "object_id",
                                                 "source_type", "source_ref", "date_libelle", "description"))
            cotes = []
            for ligne in lignes:
                app, modele = ligne.pop("content_type__app_label"), ligne.pop("content_type__model")
                ligne["source_modele"] = f"{app}.{modele}" if app and modele else None
                ligne["source_id"] = ligne.pop("object_id")
                cotes.append(ligne)
            return {"origine": "django-lecture-seule", "document_id": 9,
                    "acces": {"base": "court_project_pg", "transport": "socket Unix",
                              "transaction_read_only": "on", "isolation": "repeatable read"},
                    "enonces": list(enonces.values()), "liens": liens, "cotes": cotes}
    finally:
        connections.close_all()
