"""
Fusionne des trames narratives dans l'une d'elles, sans perdre un seul lien.

    python manage.py fusionner_trames 6 36 7 --dans 56               # simulation
    python manage.py fusionner_trames 6 36 7 --dans 56 --appliquer

Contrairement aux autres commandes du dossier, la simulation est le mode PAR
DÉFAUT et il faut `--appliquer` pour écrire : une fusion supprime des trames,
et une suppression de trame ne se rejoue pas.

CE QU'UNE TRAME PORTE

Supprimer une trame absorbée sans rien déplacer ferait perdre plus que son
titre. Un inventaire complet des liens, vérifié sur la base :

  1. Six relations de preuve — evenements, citations_courriel, citations_pdf,
     photo_documents, source_statements, citations_chat.
  2. targeted_statements — les allégations que la trame attaque.
  3. supported_contestations — le lien vers les PerjuryContestation, donc vers
     le bordereau : c'est par là qu'une trame donne ses pièces à un dossier.
  4. PerjuryArgument — OneToOne, supprimé en cascade avec la trame.
  5. LibraryNode — relation GÉNÉRIQUE, sans contrainte en base. 34 nœuds de
     l'Affidavit (document 6) pointent vers une trame. Rien n'empêche de
     supprimer la trame sous le nœud : il reste, et pointe dans le vide. Trois
     nœuds sont déjà dans cet état (trames 21, 22 et 45, supprimées avant que
     cette commande existe). C'est le lien qu'on perd sans s'en apercevoir.

Les relations 1 à 3 sont réunies (add), jamais remplacées (set). Le nœud de
bibliothèque est repointé sur la survivante. Le PerjuryArgument est déplacé s'il
n'y a pas de conflit, et la fusion s'arrête s'il y en a un — ce cas se tranche à
la main, pas par une règle.

Le titre et le résumé de l'absorbée sont versés à la fin du résumé de la
survivante, derrière un marqueur « — Absorbé de T<pk> — » suivi du titre : rien n'est
réécrit ni résumé au passage, l'argumentation rédigée survit intégralement à la
trame qui la portait. Condenser les résumés réunis est une passe manuelle
ultérieure, dans l'éditeur ; le marqueur est là pour la rendre repérable.

Chaque trame absorbée est écrite dans un fichier JSON avant sa suppression,
avec toutes ses clés étrangères. Le fichier n'est pas un mécanisme de
restauration automatique, mais il contient de quoi refaire la trame à
l'identique.
"""

import json
from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from argument_manager.models import PerjuryArgument, TrameNarrative
from document_manager.models import LibraryNode

M2M_A_REUNIR = TrameNarrative.EVIDENCE_FIELDS + ('targeted_statements',)


def etat(trame):
    """Toutes les clés étrangères d'une trame, telles qu'elles sont maintenant."""
    ct = ContentType.objects.get_for_model(TrameNarrative)
    donnees = {
        'pk': trame.pk,
        'titre': trame.titre,
        'resume': trame.resume,
        'type_argument': trame.type_argument,
        'ai_analysis_json': trame.ai_analysis_json,
        'contestations': sorted(trame.supported_contestations.values_list('pk', flat=True)),
        'library_nodes': sorted(
            LibraryNode.objects.filter(content_type=ct, object_id=trame.pk).values_list('pk', flat=True)
        ),
    }
    for champ in M2M_A_REUNIR:
        donnees[champ] = sorted(getattr(trame, champ).values_list('pk', flat=True))
    argument = PerjuryArgument.objects.filter(trame=trame).first()
    donnees['perjury_argument'] = argument.pk if argument else None
    return donnees


class Command(BaseCommand):
    help = "Fusionne une ou plusieurs trames narratives dans une trame survivante."

    def add_arguments(self, parser):
        parser.add_argument('absorbees', nargs='+', type=int,
                            help="pk des trames à absorber puis supprimer")
        parser.add_argument('--dans', type=int, required=True, dest='survivante',
                            help="pk de la trame qui reçoit tout et survit")
        parser.add_argument('--appliquer', action='store_true',
                            help="écrit en base ; sans ce drapeau, la commande ne fait que simuler")
        parser.add_argument('--sauvegarde', default=None,
                            help="chemin du JSON de sauvegarde (défaut : backup_fusion_trames_<horodatage>.json)")

    def handle(self, *args, **options):
        survivante_pk = options['survivante']
        absorbees_pk = [pk for pk in options['absorbees'] if pk != survivante_pk]
        appliquer = options['appliquer']

        try:
            survivante = TrameNarrative.objects.get(pk=survivante_pk)
        except TrameNarrative.DoesNotExist:
            raise CommandError(f"La trame survivante {survivante_pk} n'existe pas.")

        absorbees = list(TrameNarrative.objects.filter(pk__in=absorbees_pk))
        manquantes = set(absorbees_pk) - {t.pk for t in absorbees}
        if manquantes:
            raise CommandError(f"Trames introuvables : {sorted(manquantes)}")
        if not absorbees:
            raise CommandError("Aucune trame à absorber.")

        ct = ContentType.objects.get_for_model(TrameNarrative)
        avant = etat(survivante)
        sauvegarde = [etat(t) for t in absorbees]

        # Un PerjuryArgument des deux côtés ne se fusionne pas : le champ est un
        # OneToOne et les quatre textes sont rédigés, pas calculés.
        conflits = [
            t.pk for t in absorbees
            if PerjuryArgument.objects.filter(trame=t).exists()
            and PerjuryArgument.objects.filter(trame=survivante).exists()
        ]
        if conflits:
            raise CommandError(
                f"T{survivante_pk} et T{conflits} ont chacune un PerjuryArgument. "
                "Reprendre le texte à la main dans l'un des deux, le supprimer de "
                "l'autre, puis relancer."
            )

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"\nFusion dans T{survivante_pk} « {survivante.titre[:70]} »"
            + ("" if appliquer else "   [SIMULATION]")
        ))

        gains = {champ: set() for champ in M2M_A_REUNIR}
        gains_contestations = set()
        noeuds_a_repointer = []
        arguments_a_deplacer = []

        for trame in absorbees:
            self.stdout.write(f"\n  T{trame.pk} « {trame.titre[:66]} »")
            for champ in M2M_A_REUNIR:
                nouveaux = set(getattr(trame, champ).values_list('pk', flat=True)) - set(avant[champ])
                gains[champ] |= nouveaux
                deja = len(getattr(trame, champ).all()) - len(nouveaux)
                if nouveaux or deja:
                    self.stdout.write(
                        f"      {champ:<22} +{len(nouveaux):<3} nouveaux, {deja} déjà présents"
                    )
            nouvelles_c = set(trame.supported_contestations.values_list('pk', flat=True)) - set(avant['contestations'])
            gains_contestations |= nouvelles_c
            if nouvelles_c:
                self.stdout.write(self.style.WARNING(
                    f"      contestations          +{len(nouvelles_c)} : {sorted(nouvelles_c)}"
                ))
            noeuds = list(LibraryNode.objects.filter(content_type=ct, object_id=trame.pk).select_related('document'))
            for noeud in noeuds:
                jumeau = LibraryNode.objects.filter(
                    content_type=ct, object_id=survivante_pk, document=noeud.document
                ).exists()
                noeuds_a_repointer.append(noeud)
                self.stdout.write(self.style.WARNING(
                    f"      LibraryNode {noeud.pk} (doc {noeud.document_id} « {noeud.document.title[:28]} »)"
                    f" → T{survivante_pk}" + ("   ⚠ le document pointe déjà vers la survivante" if jumeau else "")
                ))
            argument = PerjuryArgument.objects.filter(trame=trame).first()
            if argument:
                arguments_a_deplacer.append(argument)
                self.stdout.write(self.style.WARNING(f"      PerjuryArgument {argument.pk} → T{survivante_pk}"))

        total_avant = sum(len(avant[c]) for c in TrameNarrative.EVIDENCE_FIELDS)
        total_gain = sum(len(gains[c]) for c in TrameNarrative.EVIDENCE_FIELDS)
        self.stdout.write(
            f"\n  Preuves de T{survivante_pk} : {total_avant} → {total_avant + total_gain}"
            f"   (+{total_gain})"
        )
        self.stdout.write(f"  Trames supprimées à la fin : {sorted(t.pk for t in absorbees)}")

        if not appliquer:
            self.stdout.write(self.style.NOTICE(
                "\n  Rien n'a été écrit. Relancer avec --appliquer pour exécuter.\n"
            ))
            return

        chemin = options['sauvegarde'] or (
            f"backup_fusion_trames_{datetime.now().strftime('%Y-%m-%d_%H%M')}.json"
        )
        with open(chemin, 'w') as f:
            json.dump({'survivante': avant, 'absorbees': sauvegarde}, f, ensure_ascii=False, indent=2)
        self.stdout.write(f"\n  Sauvegarde : {chemin}")

        with transaction.atomic():
            for trame in absorbees:
                for champ in M2M_A_REUNIR:
                    getattr(survivante, champ).add(*getattr(trame, champ).all())
                for contestation in trame.supported_contestations.all():
                    contestation.supporting_narratives.add(survivante)
                # Séparateur en <p><strong>, pas en <hr> : la liste
                # BLEACH_ALLOWED_TAGS du projet ne contient pas hr, et un
                # résumé qui repasserait un jour par un filtre de nettoyage
                # perdrait ses séparations. Le marqueur reste repérable tel
                # quel pour la passe de condensation qui suivra.
                # Le repère « — Absorbé de T<pk> — » se ferme sur lui-même et ne
                # dépend pas du titre : plusieurs titres contiennent déjà des
                # guillemets, et un marqueur qui les emploierait comme
                # délimiteurs ne se relirait plus. Le titre suit, en clair.
                survivante.resume = (survivante.resume or '') + (
                    f'<p><strong>— Absorbé de T{trame.pk} —</strong> '
                    f'<em>{trame.titre}</em></p>'
                    f'{trame.resume or ""}'
                )
            LibraryNode.objects.filter(
                content_type=ct, object_id__in=[t.pk for t in absorbees]
            ).update(object_id=survivante_pk)
            for argument in arguments_a_deplacer:
                argument.trame = survivante
                argument.save(update_fields=['trame'])
            survivante.save(update_fields=['resume'])
            for trame in absorbees:
                trame.delete()

        apres = etat(survivante)
        total_apres = sum(len(apres[c]) for c in TrameNarrative.EVIDENCE_FIELDS)
        self.stdout.write(self.style.SUCCESS(
            f"  Fait. T{survivante_pk} porte {total_apres} preuves, "
            f"{len(apres['contestations'])} contestation(s), "
            f"{len(apres['library_nodes'])} nœud(s) de bibliothèque."
        ))
        restantes = TrameNarrative.objects.filter(pk__in=[t.pk for t in absorbees])
        if restantes.exists():
            raise CommandError(f"Trames non supprimées : {list(restantes.values_list('pk', flat=True))}")
