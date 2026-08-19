"""
Remplit `Event.debut` et `Event.fin` à partir des photographies liées.

    python manage.py remplir_bornes --dry-run
    python manage.py remplir_bornes
    python manage.py remplir_bornes --forcer      # écrase les bornes saisies

L'intervalle vivait auparavant DANS le texte de `explanation`, sous forme d'un
préfixe « On 2012-03-31 between 14:46 and 16:26: ». Cette commande le rétablit
là où il appartient : dans deux colonnes.

CE QUI EST REPRIS À `cluster_photos`. Le calcul est identique — photographies
liées triées sur `datetime_original`, première et dernière. Le rapprochement
avec les préfixes archivés donne 302 intervalles identiques sur 305 comparables
(99,0 %).

CE QUI DIFFÈRE. Les bornes sont désormais MODIFIABLES. Les photographies
bornent l'événement par le bas : elles disent quand on a photographié, non
quand l'événement a eu lieu. `--forcer` mis à part, une borne déjà saisie n'est
jamais écrasée.

⚠️ FUSEAU. `Photo.datetime_original` porte l'étiquette UTC mais contient
l'heure locale au mur. La valeur est recopiée telle quelle, sans conversion :
convertir déplacerait 13 % des photographies en pleine nuit. Voir la note sur
`Event.debut`.
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from events.models import Event


class Command(BaseCommand):
    help = "Remplit debut/fin depuis les photographies liées."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--forcer", action="store_true",
                            help="écrase des bornes déjà saisies")

    def handle(self, *args, **options):
        evs = list(Event.objects.prefetch_related("linked_photos").all())

        a_ecrire, deja, sans_photo = [], [], []
        for e in evs:
            empan = e.empan_photographique
            if empan is None:
                sans_photo.append(e)
                continue
            if e.debut is not None and e.fin is not None and not options["forcer"]:
                deja.append(e)
                continue
            if (e.debut, e.fin) == empan:
                deja.append(e)
                continue
            a_ecrire.append((e, empan))

        self.stdout.write("=" * 76)
        self.stdout.write("REMPLISSAGE DES BORNES depuis les photographies liées")
        self.stdout.write("=" * 76)
        self.stdout.write(f"  événements                : {len(evs)}")
        self.stdout.write(f"  à écrire                  : {len(a_ecrire)}")
        self.stdout.write(f"  déjà conformes ou saisies : {len(deja)}")
        self.stdout.write(f"  sans photographie datée   : {len(sans_photo)}"
                          + (f" → {[x.pk for x in sans_photo]}" if sans_photo else ""))

        # Les événements dont la date ne correspond pas à celle des photos ne
        # sont pas corrigés ici : la date est une donnée saisie, et l'écart
        # peut être voulu. Il est signalé, pas résolu.
        ecarts_date = [(e.pk, e.date, d.date())
                       for e, (d, _) in a_ecrire if e.date != d.date()]
        if ecarts_date:
            self.stdout.write("")
            self.stdout.write(self.style.WARNING(
                f"  DATE DE L'ÉVÉNEMENT ≠ DATE DE LA 1re PHOTO : {len(ecarts_date)}"))
            for pk, d_ev, d_ph in ecarts_date:
                self.stdout.write(f"     E-{pk} : date={d_ev}  1re photo={d_ph}")
            self.stdout.write("     La date n'est PAS modifiée : c'est une saisie, "
                              "l'écart peut être voulu.")

        self.stdout.write("")
        self.stdout.write("  ÉCHANTILLON")
        for e, (d, f) in a_ecrire[:8]:
            self.stdout.write(f"     E-{e.pk:<5} {d:%Y-%m-%d %H:%M} → {f:%H:%M}"
                              f"   {(e.explanation or '')[:52]}")

        if options["dry_run"]:
            self.stdout.write("")
            self.stdout.write("--dry-run : rien n'a été écrit.")
            return

        with transaction.atomic():
            for e, (d, f) in a_ecrire:
                e.debut, e.fin = d, f
                e.save(update_fields=["debut", "fin"])

        total = Event.objects.exclude(debut=None).count()
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"{len(a_ecrire)} événement(s) mis à jour. "
            f"{total} / {len(evs)} portent désormais leurs bornes."))
