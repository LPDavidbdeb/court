"""
Enregistre l'axe « Soccer d'Alexia — été 2013 », ses quatre faits et leurs appuis.

    python manage.py axe_soccer_2013 --dry-run
    python manage.py axe_soccer_2013

Cet axe conteste deux allégations de la Requête du 19 novembre 2015 :

    § 9  — « En 2013, le défendeur est parti tout l'été et a laissé la
            demanderesse seule avec les deux (2) enfants. »          Statement 13
    § 16 — « C'est la demanderesse qui s'occupait des enfants, qui allait
            aux activités, etc...... »                               Statement 20

Il est délibérément PARTIEL : quatre faits ne suffisent pas à réfuter deux
allégations d'extension. D'autres axes porteront sur la même période et
convergeront sur les mêmes allégations.

LE RÔLE DE CHAQUE APPUI EST LA DONNÉE PRINCIPALE.

Les deux PDF de l'association datent de 2026 : ils montrent la forme récurrente
d'une saison, ils ne prouvent pas le calendrier de 2013. Les déclarer
ILLUSTRATION empêche qu'un assemblage leur fasse porter un fait qu'ils ne
portent pas — c'est précisément la distinction que l'adversaire ferait à notre
place si elle n'était pas faite ici.
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from argument_manager.models import Axe, AppuiFait, Fait, RoleAppui
from document_manager.models import Statement
from email_manager.models import Email
from events.models import Event
from pdf_manager.models import PDFDocument

R = RoleAppui

NOM = "Soccer d'Alexia — été 2013"

CIBLES = [13, 20]          # Statement pk, dans la Requête du 19 novembre 2015

FAITS = [
    (1, "À l'été 2013, Alexia suivait les cours de soccer de l'Association de "
        "soccer de Saint-Lambert.",
     [
         (Event, 239, R.ATTESTATION,
          "28 mai 2013 — le défendeur au Parc Préville avec Alexia, 7 photos. "
          "Dix jours après le début de la session."),
         (Event, 263, R.ATTESTATION,
          "24 août 2013 — remise des médailles de soccer, avec Alexia, 2 photos. "
          "Cinq jours avant la fête de fin de saison."),
     ]),
    (2, "La demanderesse agissait comme coach bénévole de l'association.",
     [
         (Email, 634, R.VERIFICATION,
          "Fil « Liste des coach à l'été 2013 » — l'association peut confirmer "
          "avec certitude la participation de la demanderesse comme coach "
          "bénévole cet été-là. Reste à obtenir l'affectation d'équipe."),
         (Email, 635, R.VERIFICATION, "Suite du fil — réponse de l'association."),
         (Email, 637, R.VERIFICATION, "Suite du fil — réponse de l'association."),
         (Email, 640, R.VERIFICATION, "Suite du fil — réponse de l'association."),
     ]),
    (3, "La session s'étendait de mai à août, à raison de deux séances par semaine.",
     [
         (PDFDocument, 91, R.ILLUSTRATION,
          "Calendrier de l'association : début 18 mai, fin 29 août, pauses les "
          "23 mai, 24 juin et 25-31 juillet, fête de fin de saison le 29 août. "
          "Document de 2026 — montre la forme récurrente de la saison, ne prouve "
          "pas le calendrier de 2013."),
         (PDFDocument, 90, R.ILLUSTRATION,
          "Grille horaire : tarification « 1 séance » ou « 2 séances », deux "
          "créneaux hebdomadaires par catégorie. Document de 2026, même réserve."),
         (Event, 239, R.ATTESTATION,
          "28 mai — tombe dans la session telle que le calendrier la décrit."),
         (Event, 263, R.ATTESTATION,
          "24 août — tombe dans la session telle que le calendrier la décrit."),
     ]),
    (4, "Pendant cette période, le défendeur assumait la garde de Nicolas, "
        "alors âgé de six mois.",
     [
         (Event, 247, R.ATTESTATION,
          "8 juillet — le défendeur seul au domicile avec Nicolas."),
         (Event, 251, R.ATTESTATION,
          "11 juillet — le défendeur seul au domicile avec Nicolas."),
         (Event, 253, R.ATTESTATION,
          "12 juillet — le défendeur seul au domicile avec Nicolas."),
         (Event, 259, R.ATTESTATION,
          "14 août — le défendeur seul avec Nicolas à Cape Cod."),
         (Email, 33, R.INFERENCE,
          "29 juillet, la mère du défendeur : « Si tu viens demain AVEC NICHOLAS "
          "on passera chez Josée ». Elle ne demande pas s'il aura Nicolas : elle "
          "organise autour du fait qu'il l'a."),
         (Email, 32, R.INFERENCE,
          "30 juillet, le défendeur : « Y a pas de soccer demain MAIS je passerai "
          "peut-être ». Le « mais » écarte la condition : la venue avec Nicolas "
          "ne dépend pas du calendrier de soccer."),
     ]),
]


class Command(BaseCommand):
    help = "Enregistre l'axe « Soccer d'Alexia — été 2013 »."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        cibles = list(Statement.objects.filter(pk__in=CIBLES))
        if len(cibles) != len(CIBLES):
            manquants = set(CIBLES) - {s.pk for s in cibles}
            raise CommandError(f"Statement introuvable(s) : {manquants}")

        self.stdout.write("=" * 78)
        self.stdout.write(f"AXE — {NOM}")
        self.stdout.write("=" * 78)
        self.stdout.write("  conteste :")
        for s in cibles:
            self.stdout.write(f"    Statement {s.pk} — « {(s.text or '')[:66]} »")

        total = 0
        problemes = []
        for ordre, enonce, appuis in FAITS:
            self.stdout.write("")
            self.stdout.write(f"  FAIT {ordre}. {enonce}")
            for modele, pk, role, note in appuis:
                obj = modele.objects.filter(pk=pk).first()
                if obj is None:
                    problemes.append(f"{modele.__name__} {pk} absent de la base")
                    self.stdout.write(self.style.ERROR(
                        f"      {role:<13} {modele.__name__} {pk} — INTROUVABLE"))
                    continue
                total += 1
                self.stdout.write(f"      {role:<13} {modele.__name__} {pk} — "
                                  f"{str(obj)[:52]}")
                self.stdout.write(f"                    {note[:88]}")

        self.stdout.write("")
        self.stdout.write(f"  {len(FAITS)} faits, {total} appuis")
        if problemes:
            raise CommandError("Appuis introuvables : " + "; ".join(problemes))

        if options["dry_run"]:
            self.stdout.write("")
            self.stdout.write("--dry-run : rien n'a été écrit.")
            return

        with transaction.atomic():
            axe, _ = Axe.objects.update_or_create(
                nom=NOM,
                defaults={
                    "description":
                        "Réfute par le remplissage deux allégations d'extension de la "
                        "Requête du 19 novembre 2015. Axe partiel : d'autres portent "
                        "sur la même période.",
                    "fenetre_debut": __import__("datetime").date(2013, 5, 18),
                    "fenetre_fin": __import__("datetime").date(2013, 8, 29),
                })
            axe.cibles.set(cibles)
            axe.faits.all().delete()          # rebâti à l'identique à chaque passage

            for ordre, enonce, appuis in FAITS:
                fait = Fait.objects.create(ordre=ordre, enonce=enonce)
                fait.axes.add(axe)
                for i, (modele, pk, role, note) in enumerate(appuis, start=1):
                    AppuiFait.objects.create(
                        fait=fait, ordre=i,
                        content_type=ContentType.objects.get_for_model(modele),
                        object_id=pk, role=role, note=note)

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Axe {axe.pk} — {axe.faits.count()} faits, "
            f"{AppuiFait.objects.filter(fait__axes=axe).count()} appuis, "
            f"{axe.cibles.count()} allégations visées."))
