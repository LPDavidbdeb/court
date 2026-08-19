"""
Axe « Cours de danse de la demanderesse — prise en charge par le défendeur ».

    python manage.py axe_danse --dry-run
    python manage.py axe_danse

Conteste quatre allégations de la Requête du 19 novembre 2015 :

    § 6  — « le défendeur ne s'impliquait que minimalement dans les soins
            d'Alexia, laissant toute la responsabilité à la demanderesse »
    § 7  — « il est ressorti que le défendeur avait de la difficulté à assumer
            son rôle de père et s'investir »
    § 15 — « le défendeur était rarement disponible pour prendre soins d'eux »
    § 16 — « C'est la demanderesse qui s'occupait des enfants, qui allait aux
            activités, etc...... »

LE RAISONNEMENT N'EST PAS ARITHMÉTIQUE

L'axe n'additionne pas une photo et un courriel pour en tirer trente semaines.
Il combine quatre ordres de preuve : la biographie établit la CONTINUITÉ de
l'activité ; le calendrier de l'école établit qu'il s'agit de cours RÉGULIERS
par sessions ; l'échange de 2016 établit une FRÉQUENCE d'un à trois soirs par
semaine ; les communications contemporaines établissent l'EXÉCUTION concrète —
le père auprès des enfants pendant que la mère est au cours.

Le fait 5 est écrit pour neutraliser d'avance l'objection « vous n'avez pas
démontré que la session de 2012 avait les mêmes dates que celle de 2026 ». Ce
n'est pas ce qui est allégué : le calendrier est invoqué pour le caractère
récurrent du fonctionnement par sessions, jamais pour attribuer rétroactivement
des dates à une année donnée.
"""
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from argument_manager.models import Axe, AppuiFait, Fait, RoleAppui
from document_manager.models import Statement
from email_manager.models import Email
from events.models import Event
from pdf_manager.models import PDFDocument
from photos.models import PhotoDocument

R = RoleAppui
NOM = "Cours de danse de la demanderesse — prise en charge par le défendeur"

# Statements visés. Le § 7 est un cas particulier : la phrase utile — « il est
# ressorti que le défendeur avait de la difficulté à assumer son rôle de père »
# — n'est pas dans le paragraphe lui-même (Statement 10) mais dans sa
# CONTINUATION de profondeur 3 (Statement 11). C'est l'un des cinq nœuds que
# `verifier_schemas` signale comme hétérogènes au niveau 3 du doc 1 : le schéma
# y déclare SOUS_ITEM, mais cinq de ces nœuds sont des paragraphes de suite.
# Viser le § 7 entier aurait raté l'énoncé contesté.
CIBLES = [9, 11, 19, 20]      # § 6, § 7 (continuation), § 15, § 16

FAITS = [
    (1, "Pendant la cohabitation des parties, la demanderesse a poursuivi de façon "
        "continue des cours de danse en soirée.",
     [
         (PDFDocument, 59, R.ATTESTATION,
          "Biographie publiée par le studio : « jusqu'en 2016 ». Établit la "
          "continuité de l'activité sur la période pertinente."),
     ]),
    (2, "L'école fonctionne par inscriptions à des cours réguliers offerts à jour et "
        "heure fixes pour la durée d'une session, et non par cours ponctuels suivis "
        "à l'unité.",
     [
         (PhotoDocument, 4, R.CADRE,
          "Calendrier de session des Ballets Modernes — établit le fonctionnement "
          "par sessions, à jour et heure fixes."),
         (PhotoDocument, 15, R.CADRE,
          "Adresse de l'école — situe le déplacement qu'impose le cours du soir."),
     ]),
    (3, "Le calendrier de l'école comporte une session d'automne et une session "
        "d'hiver-printemps qui, ensemble, représentent plus de trente semaines de "
        "cours au cours d'une année type.",
     [
         (PhotoDocument, 4, R.CADRE,
          "Deux grandes sessions, automne puis hiver-printemps, totalisant plus de "
          "trente semaines."),
     ]),
    (4, "Les dates exactes de début et de fin des sessions peuvent varier d'une année "
        "à l'autre ; le calendrier est invoqué pour établir le caractère récurrent et "
        "prolongé du fonctionnement par sessions, et non pour attribuer "
        "rétroactivement à chacune des années de cohabitation exactement les mêmes "
        "dates ou le même nombre de semaines.",
     [
         (PhotoDocument, 4, R.ILLUSTRATION,
          "RÉSERVE EXPRESSE. Le calendrier ne date pas des années de cohabitation : "
          "il vaut pour la forme récurrente de l'activité, pas pour le calendrier "
          "d'une année déterminée. Déclaré ILLUSTRATION à ce titre précis."),
     ]),
    (5, "Selon le nombre de cours auxquels elle était inscrite au cours d'une session, "
        "les engagements de danse de la demanderesse variaient d'un à trois soirs par "
        "semaine.",
     [
         (Email, 7, R.ATTESTATION,
          "16 septembre 2016 — le défendeur : « quand tu allais a tes cours de dance "
          "le soir, auxquels tu allais de une a trois fois semaine »."),
         (Email, 100, R.ATTESTATION,
          "9 décembre 2010 — le défendeur à sa mère : « je t'ai déjà dit que les "
          "mardi et mercredi Élise dansait ». Nomme les jours, contemporain des faits."),
     ]),
    (6, "Dans sa réponse immédiate, la demanderesse contestait expressément d'autres "
        "affirmations contenues dans ce message — notamment celles relatives à "
        "l'alcool et à une participation de 50 % — sans rectifier l'existence de ses "
        "cours du soir ni la fréquence d'une à trois fois par semaine.",
     [
         (Email, 306, R.ATTESTATION,
          "16 septembre 2016, 20 h 50, onze minutes après : « je n'ai pas dit que tu "
          "passais ton temps à te saouler mais je ne pense pas que j'aille tort de "
          "dire que non tu ne t'en occupais pas 50 % du temps ». Elle relève deux "
          "points et laisse la danse intacte."),
     ]),
    (7, "Lorsque la demanderesse quittait le domicile afin d'assister à ses cours de "
        "danse pendant la cohabitation, le défendeur assumait la prise en charge des "
        "enfants.",
     [
         (Email, 81, R.ATTESTATION,
          "7 décembre 2010 — la grand-mère : « J'aimerais aller voir Alexia LORSQUE "
          "ÉLISE SERA À LA DANSE […] si Élise n'est pas là demain soir, j'aimerais "
          "passer ». Une soirée de danse est une période où la mère est absente et "
          "le père auprès de l'enfant."),
         (Email, 80, R.ATTESTATION,
          "9 décembre 2010 — « J'ai adoré ma visite hier avec Alexia ». La visite "
          "s'est réalisée : l'arrangement a été exécuté."),
         (Email, 66, R.ATTESTATION,
          "15 mars 2011 — la grand-mère coordonne sa visite au moment où le père "
          "donne le bain : « Appelle moi quand tu entres la petite dans le bain »."),
         (Email, 116, R.ATTESTATION, "15 mars 2011 — réponse du défendeur."),
         (Email, 115, R.ATTESTATION, "15 mars 2011 — suite de l'échange."),
         (Email, 347, R.ATTESTATION,
          "6 mars 2012 — le défendeur : il doit être « à la maison de bonne heure ce "
          "soir parce que tu danses » et s'organise « de m'occuper d'Alexia ». Le "
          "lien est explicite et contemporain."),
         (Event, 220, R.ATTESTATION,
          "16 décembre 2012 — le défendeur au cours de danse d'Alexia, 7 photos."),
     ]),

    # ------------------------------------------------------------------
    # Fait 8 — la règle a tenu pendant la séparation temporaire de 2011.
    #
    # POURQUOI UN FAIT DISTINCT PLUTÔT QU'UN ÉLARGISSEMENT DU FAIT 7.
    # Le fait 7 énonce une règle du fonctionnement familial pendant la vie
    # commune. Y agréger la période de résidence distincte diluerait une règle
    # récurrente dans une exception et affaiblirait les deux. Séparé, l'épisode
    # devient un fait autonome dont la force est PLUS grande que celle de la
    # règle : le père traversait la ville pour l'exécuter.
    #
    # CE QUE LE DÉPÔT ÉTABLIT DÉJÀ (§ 16-17) : compte d'électricité au 311, rue
    # Riverside du 1er février au 29 mai 2011 — environ quatre mois, à 1,6 km
    # de la résidence familiale — le défendeur demeurant par ailleurs titulaire
    # ou responsable du compte de celle-ci ; thérapie de couple de février 2011
    # à janvier 2012, poursuivie après la reprise de la vie commune.
    #
    # CE QUE LE FAIT OPPOSE. La Requête allègue au § 7 que « les parties ont
    # vécu séparées pendant un (1) an ». Le fait ne conteste pas seulement la
    # DURÉE (quatre mois de compte distinct, non douze) mais la NATURE de la
    # période : les soins du soir de l'enfant se sont poursuivis à la résidence
    # familiale, le père s'y déplaçant.
    #
    # ⚠️ RESTER SUR LE TERRAIN PARENTAL. Le § 7 rattache la séparation à une
    # infidélité. Ce motif est hors du critère parental et il n'y a aucun
    # intérêt à y ramener le débat : le fait porte sur la continuité des soins,
    # jamais sur la cause de la séparation.
    (8, "Pendant la période de résidence distincte du 1er février au 29 mai 2011, "
        "le défendeur a continué d'assurer la routine du soir d'Alexia à la "
        "résidence familiale les soirs où la demanderesse était à ses cours de "
        "danse, en s'y déplaçant depuis son logement.",
     [
         (Event, 46, R.ATTESTATION,
          "Mercredi 9 février 2011, 19 h 03 à 19 h 33 — bain puis après-bain "
          "d'Alexia, alors âgée de seize mois. Le mercredi est l'un des deux "
          "créneaux de danse établis pour cette session par P-48."),
         (Event, 52, R.ATTESTATION,
          "Mercredi 16 février 2011, 18 h 02 à 18 h 40 — même séquence, une "
          "semaine plus tard, 12 photographies. La répétition à sept jours "
          "d'intervalle sur le même créneau est ce qui fait la récurrence."),
         (Email, 66, R.ATTESTATION,
          "Mardi 15 mars 2011 — la grand-mère cale sa visite sur le moment du "
          "bain : « Appelle moi quand tu entres la petite dans le bain ». Un "
          "tiers organise sa venue autour d'une routine que le père exécute, "
          "à l'intérieur de la période de résidence distincte."),
     ]),
]


class Command(BaseCommand):
    help = "Enregistre l'axe des cours de danse."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        # On vérifie que les cibles sont bien les allégations visées, plutôt que
        # de se fier à des pk notés de mémoire.
        ATTENDU = {
            9: "ne s'impliquait que minimalement",
            11: "difficulté à assume",     # continuation du § 7, profondeur 3
            19: "rarement disponible",
            20: "qui s'occupait des enfants",
        }
        cibles = []
        for pk, fragment in ATTENDU.items():
            s = Statement.objects.filter(pk=pk).first()
            if s is None:
                raise CommandError(f"Statement {pk} introuvable")
            if fragment.lower() not in (s.text or "").lower():
                raise CommandError(
                    f"Statement {pk} ne contient pas « {fragment} » — "
                    f"il porte : « {(s.text or '')[:80]} »")
            cibles.append(s)

        self.stdout.write("=" * 80)
        self.stdout.write(f"AXE — {NOM}")
        self.stdout.write("=" * 80)
        for s in cibles:
            self.stdout.write(f"  conteste  Statement {s.pk} — « {(s.text or '')[:64]} »")

        total, problemes = 0, []
        for ordre, enonce, appuis in FAITS:
            self.stdout.write("")
            self.stdout.write(f"  FAIT {ordre}. {enonce[:96]}")
            for modele, pk, role, note in appuis:
                obj = modele.objects.filter(pk=pk).first()
                if obj is None:
                    problemes.append(f"{modele.__name__} {pk}")
                    self.stdout.write(self.style.ERROR(
                        f"      {role:<13} {modele.__name__} {pk} — INTROUVABLE"))
                    continue
                total += 1
                self.stdout.write(f"      {role:<13} {modele.__name__} {pk} — "
                                  f"{str(obj)[:48]}")

        self.stdout.write("")
        self.stdout.write(f"  {len(FAITS)} faits, {total} appuis")
        if problemes:
            raise CommandError("Appuis introuvables : " + ", ".join(problemes))

        if options["dry_run"]:
            self.stdout.write("")
            self.stdout.write("--dry-run : rien n'a été écrit.")
            return

        with transaction.atomic():
            axe, _ = Axe.objects.update_or_create(
                nom=NOM,
                defaults={
                    "description":
                        "Répond partiellement à l'allégation de désengagement historique. "
                        "Les seuls engagements de danse entraînaient déjà, sur une part "
                        "substantielle de chaque année et plusieurs années de cohabitation, "
                        "des périodes récurrentes de prise en charge par le défendeur — "
                        "composante répétitive, non interventions occasionnelles. Les "
                        "autres catégories (repas, bains, couchers, garderie, présence "
                        "quotidienne) s'ajouteront comme composantes indépendantes.",
                    "fenetre_debut": datetime.date(2010, 12, 7),
                    "fenetre_fin": datetime.date(2016, 9, 16),
                })
            axe.cibles.set(cibles)

            # RECONSTRUCTION SANS PERTE. La commande rebâtit l'axe à chaque
            # passage, mais trois champs de `Fait` ne viennent PAS d'ici :
            # `statement` (le paragraphe plaidé), `nature` et `raison` sont
            # écrits par `differentiel_axes`. Un `delete()` suivi d'un
            # `create()` les effacerait silencieusement — et ferait perdre le
            # rattachement à l'exposé. On apparie donc sur `ordre` et on
            # préserve. Les appuis, eux, sont bien définis ici : ils se
            # refont à neuf.
            existants = {f.ordre: f for f in axe.faits.all()}
            gardes = set()

            for ordre, enonce, appuis in FAITS:
                fait = existants.get(ordre)
                if fait is None:
                    fait = Fait.objects.create(ordre=ordre, enonce=enonce)
                else:
                    fait.enonce = enonce
                    fait.save(update_fields=["enonce"])
                fait.axes.add(axe)
                gardes.add(fait.pk)

                fait.appuis.all().delete()
                for i, (modele, pk, role, note) in enumerate(appuis, start=1):
                    AppuiFait.objects.create(
                        fait=fait, ordre=i,
                        content_type=ContentType.objects.get_for_model(modele),
                        object_id=pk, role=role, note=note)

            # Un fait retiré de la liste se détache de CET axe ; il n'est
            # supprimé que s'il ne sert plus aucun autre axe.
            for fait in list(axe.faits.all()):
                if fait.pk in gardes:
                    continue
                fait.axes.remove(axe)
                if not fait.axes.exists():
                    fait.delete()

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Axe {axe.pk} — {axe.faits.count()} faits, "
            f"{AppuiFait.objects.filter(fait__axes=axe).count()} appuis, "
            f"{axe.cibles.count()} allégations visées."))
