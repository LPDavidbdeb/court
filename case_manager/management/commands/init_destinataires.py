"""Peupler le registre des destinataires et de leurs fenêtres de validité.

    python manage.py init_destinataires --ecrire

Les trois lignes ci-dessous ne sont pas des réglages : ce sont des FAITS, chacun
établi par un acte au dossier, et c'est leur succession qui justifie le registre.
L'adresse de la seconde défenderesse a changé deux fois en trois semaines —
domicile, puis étude, puis avocats — et une adresse périmée ne se signale pas
toute seule dans un fichier Markdown.

La commande est idempotente : elle ne crée que ce qui manque.
"""

from datetime import date

from django.core.management.base import BaseCommand

from case_manager.models import DestinataireInstance

REGISTRE = [
    dict(
        partie="Élise Marie Ayoub", qualite="PARTIE",
        courriel="elise.ayoub@gmail.com",
        adresse_postale="245, rue Macaulay\nSaint-Lambert (Québec) J4R 2H1",
        valide_du=date(2026, 9, 29), valide_au=None,
        source="Réponse à l'assignation du 29 septembre 2026 (§ 1 et page 2).",
    ),
    dict(
        partie="Me Marie-Josée Ayoub", qualite="PARTIE",
        courriel="mjayoub@ayoubavocats.ca",
        adresse_postale="Ayoub Avocats Inc.\n425, rue Saint-Sulpice\nMontréal (Québec) H2Y 2V7",
        valide_du=date(2026, 9, 29), valide_au=date(2026, 10, 4),
        source="Réponse à l'assignation du 29 septembre 2026 — FERMÉE par l'avis "
               "de substitution du 5 octobre 2026.",
    ),
    dict(
        partie="Timmons Séguin Tremblay (Me Patricia Timmons)", qualite="AVOCAT",
        pour_le_compte_de="Me Marie-Josée Ayoub",
        courriel="patricia.timmons@farpbq.ca",
        adresse_postale="445, boul. Saint-Laurent, bureau 300\nMontréal (Québec) H2Y 3T8",
        valide_du=date(2026, 10, 5), valide_au=None,
        source="Avis de substitution d'avocats du 5 octobre 2026 (art. 194 C.p.c.), "
               "signifié le 7 octobre 2026. Leur dossier 26-0393 PAT.",
    ),
]


class Command(BaseCommand):
    help = "Peuple le registre des destinataires de l'instance."

    def add_arguments(self, parser):
        parser.add_argument("--ecrire", action="store_true")

    def handle(self, *args, **o):
        for ligne in REGISTRE:
            existe = DestinataireInstance.objects.filter(
                partie=ligne["partie"], courriel=ligne["courriel"],
                valide_du=ligne["valide_du"],
            ).first()
            if existe:
                self.stdout.write(f"= déjà présent : {existe}")
                continue
            if o["ecrire"]:
                d = DestinataireInstance.objects.create(**ligne)
                self.stdout.write(self.style.SUCCESS(f"+ créé : {d}"))
            else:
                self.stdout.write(f"+ à créer : {ligne['partie']} <{ligne['courriel']}>")
        if not o["ecrire"]:
            self.stdout.write(self.style.WARNING("\nRelancer avec --ecrire."))
