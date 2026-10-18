"""
Contrôle de fumée de la bascule du régime des citations.

    python bascule_fumee.py cible
    python bascule_fumee.py fumee --courriel N --pdf M

Lancé par bascule.sh, depuis la racine de l'arbre cible, dans un environnement propre et
explicite : DJANGO_SETTINGS_MODULE=settings_bascule, PYTHONPATH=<dossier de ce script>,
BASCULE_BASE, BASCULE_PORT, BASCULE_SYSID. Si l'une manque, le script refuse de tourner : il ne
devine rien.

cible — vérifie, par la connexion Django elle-même, la base (current_database), le port du
serveur (inet_server_port) et l'identifiant système du serveur (pg_control_system).

fumee — après « cible » :
  1. comptes : toutes les citations sont HERITE, toutes visibles par l'ancien système, aucune
     n'est PHRASE, et leur nombre est celui de la sauvegarde B2 (--courriel, --pdf) ;
  2. dans une transaction annulée : connexion d'un superutilisateur ; 14 pages de l'ancien système
     et de l'administration (filtre PHRASE : 0 résultat) ; puis une écriture de l'ancien régime,
     une citation de courriel et une citation PDF créées par l'ORM avec une PK explicite, hors de la
     plage existante. La colonne id est une identité « BY DEFAULT » : une PK explicite ne consomme
     pas la séquence. Rien ne subsiste après l'annulation ;
  3. après l'annulation : les deux citations d'essai n'existent plus.
  bascule.sh compare en outre la base avant et après ce contrôle (contenu des tables et séquences).

Garde-fous : réseau sortant bloqué (PostgreSQL passe par libpq, en C, et n'est pas concerné) ;
toute écriture de fichier par un stockage Django est refusée ; les deux garde-fous sont éprouvés
au début du contrôle. Code de sortie : 0 si tout est conforme, 1 si un contrôle échoue, 2 si le
contrôle n'a pas pu s'exécuter.
"""
import argparse
import os
import socket
import sys

_LOCAL = {"localhost", "127.0.0.1", "::1"}
REQUISES = ("DJANGO_SETTINGS_MODULE", "BASCULE_BASE", "BASCULE_PORT", "BASCULE_SYSID")


def bloquer_reseau():
    connect = socket.socket.connect

    def garde(self, adresse):
        if isinstance(adresse, tuple) and adresse and adresse[0] not in _LOCAL:
            raise ConnectionRefusedError(f"réseau bloqué pendant le contrôle : {adresse[0]}")
        return connect(self, adresse)

    socket.socket.connect = garde
    getaddrinfo = socket.getaddrinfo

    def garde_dns(hote, *a, **k):
        if hote is not None and hote not in _LOCAL:
            raise socket.gaierror(f"réseau bloqué pendant le contrôle : {hote}")
        return getaddrinfo(hote, *a, **k)

    socket.getaddrinfo = garde_dns


def interdire_fichiers():
    from django.core.files.storage import FileSystemStorage, Storage

    def refus(self, name, *args, **kwargs):
        raise PermissionError(f"écriture de fichier refusée pendant le contrôle : {name}")

    Storage.save = refus
    FileSystemStorage._save = refus


class Controle:

    def __init__(self):
        self.ok = True

    def verifier(self, condition, message):
        print(("OK      " if condition else "ÉCHEC   ") + message, flush=True)
        self.ok = self.ok and bool(condition)
        return condition

    def cible(self):
        from django.db import connection
        attendu = (os.environ["BASCULE_BASE"], int(os.environ["BASCULE_PORT"]), int(os.environ["BASCULE_SYSID"]))
        self.verifier(connection.settings_dict["NAME"] == attendu[0],
                      f"réglage Django : base {connection.settings_dict['NAME']}")
        with connection.cursor() as c:
            c.execute("select current_database(), inet_server_port(), system_identifier from pg_control_system()")
            vu = c.fetchone()
        self.verifier(tuple(vu) == attendu, f"cible (Django) : {vu[0]}|{vu[1]}|{vu[2]}, attendu {'|'.join(map(str, attendu))}")

    def garde_fous(self):
        # Deux barrières, éprouvées séparément : la résolution de nom, puis la connexion elle-même.
        for nom, essai in (("résolution de nom", lambda: socket.getaddrinfo("example.com", 80)),
                           ("connexion directe", lambda: socket.socket().connect(("192.0.2.1", 9)))):
            try:
                essai()
                self.verifier(False, f"garde-fou réseau ({nom}) : un accès sortant a été permis")
            except OSError as e:
                self.verifier("réseau bloqué" in str(e), f"garde-fou réseau ({nom}) : accès sortant refusé")
        from django.core.files.base import ContentFile
        from django.core.files.storage import default_storage
        try:
            default_storage.save("bascule_fumee_essai.txt", ContentFile(b"x"))
            self.verifier(False, "garde-fou fichiers : une écriture a été permise")
        except PermissionError:
            self.verifier(not default_storage.exists("bascule_fumee_essai.txt"),
                          "garde-fou fichiers : écriture refusée, aucun fichier créé")

    def fumee(self, n_courriel, n_pdf):
        from django.contrib.auth import get_user_model
        from django.db import transaction
        from django.db.models import Max
        from django.test import Client
        from django.test.utils import setup_test_environment

        from argument_manager.models import TrameNarrative
        from email_manager.models import Quote as EQ
        from pdf_manager.models import Quote as PQ

        setup_test_environment()
        self.garde_fous()

        for modele, nom, attendu in ((EQ, "courriel", n_courriel), (PQ, "PDF", n_pdf)):
            tous, visibles, phrase = modele.all_objects.count(), modele.objects.count(), modele.phrase_objects.count()
            self.verifier(tous == attendu, f"citations {nom} : {tous} au total, {attendu} attendues (sauvegarde B2)")
            self.verifier(visibles == attendu and phrase == 0,
                          f"citations {nom} : {visibles} visibles par l'ancien système, {phrase} PHRASE")
            self.verifier(not modele.all_objects.exclude(regime="HERITE").exists(), f"citations {nom} : toutes HERITE")

        email = (EQ.objects.select_related("email__thread")
                 .filter(email__thread__protagonist__isnull=False).order_by("pk").first())
        pdf = PQ.objects.order_by("pk").first()
        trame = TrameNarrative.objects.filter(citations_courriel__isnull=False).order_by("pk").first()
        utilisateur = get_user_model()._base_manager.filter(is_superuser=True, is_active=True).order_by("pk").first()
        if not self.verifier(all((email, pdf, trame, utilisateur)),
                             "objets de contrôle trouvés (citation de courriel, citation PDF, trame, superutilisateur)"):
            return
        urls = ["/", "/emails/quotes/", f"/emails/email/{email.email_id}/", f"/emails/thread/{email.email.thread_id}/",
                f"/emails/quote/{email.pk}/", f"/pdfs/pdf/{pdf.pdf_document_id}/", f"/pdfs/quote/{pdf.pk}/",
                f"/arguments/{trame.pk}/", f"/arguments/{trame.pk}/affidavit/",
                "/arguments/ajax/all-quotes-for-tinymce/",
                "/admin/email_manager/quote/", "/admin/pdf_manager/quote/",
                "/admin/email_manager/quote/?regime__exact=PHRASE", "/admin/pdf_manager/quote/?regime__exact=PHRASE"]
        pk_essai = {}
        with transaction.atomic():
            client = Client(raise_request_exception=False)
            client.force_login(utilisateur)
            for url in urls:
                r = client.get(url)
                if "regime__exact=PHRASE" in url and r.status_code == 200:
                    n = len(r.context["cl"].result_list)
                    self.verifier(n == 0, f"GET {url} → {r.status_code} ({n} citation PHRASE)")
                else:
                    self.verifier(r.status_code == 200, f"GET {url} → {r.status_code}")
            for modele, nom, champs in ((EQ, "courriel", {"email_id": email.email_id}),
                                        (PQ, "PDF", {"pdf_document_id": pdf.pdf_document_id, "page_number": 1})):
                pk = (modele.all_objects.aggregate(m=Max("pk"))["m"] or 0) + 1_000_000
                modele(pk=pk, quote_text="contrôle de fumée — annulé", **champs).save(force_insert=True)
                pk_essai[modele] = pk
                self.verifier(modele.all_objects.get(pk=pk).regime == "HERITE" and modele.objects.filter(pk=pk).exists(),
                              f"écriture de l'ancien régime ({nom}, PK explicite {pk}) : HERITE, visible par l'ancien système")
            transaction.set_rollback(True)
        for modele, pk in pk_essai.items():
            self.verifier(not modele.all_objects.filter(pk=pk).exists(),
                          f"après annulation : la citation d'essai {modele._meta.label} {pk} n'existe plus")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["cible", "fumee"])
    ap.add_argument("--courriel", type=int)
    ap.add_argument("--pdf", type=int)
    args = ap.parse_args()
    manquantes = [v for v in REQUISES if not os.environ.get(v)]
    if manquantes:
        print(f"ÉCHEC   variables absentes : {', '.join(manquantes)} (lancer par bascule.sh)", flush=True)
        return 2
    if args.mode == "fumee" and (args.courriel is None or args.pdf is None):
        print("ÉCHEC   fumee exige --courriel et --pdf (nombres de la sauvegarde B2)", flush=True)
        return 2
    sys.path.insert(0, os.getcwd())
    bloquer_reseau()
    try:
        import django
        django.setup()
        interdire_fichiers()
        controle = Controle()
        controle.cible()
        if args.mode == "fumee" and controle.ok:
            controle.fumee(args.courriel, args.pdf)
    except Exception as e:  # noqa: BLE001
        print(f"ÉCHEC   le contrôle n'a pas pu s'exécuter : {type(e).__name__}: {e}", flush=True)
        return 2
    print(("FUMÉE : RÉUSSIE" if args.mode == "fumee" else "CIBLE : CONFORME") if controle.ok
          else "ÉCHEC — critère d'arrêt", flush=True)
    return 0 if controle.ok else 1


if __name__ == "__main__":
    sys.exit(main())
