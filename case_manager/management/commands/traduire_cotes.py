"""
Traduit la cotation déposée en une cotation chronologique.

    python manage.py traduire_cotes
    python manage.py traduire_cotes --limite 40

Le bordereau du dépôt est IMMUABLE : il a été déposé. Ce qui est figé, c'est la
correspondance entre une pièce (modèle + PK) et la cote qu'elle a reçue. Cette
table sert donc de traducteur : elle donne la pièce, la pièce donne sa date, la
date donne le rang, et le rang donne la nouvelle cote. Rien n'est stocké — la
nouvelle cotation est une FONCTION du contenu, recalculable à volonté.

Le tri réutilise `case_manager.exhibit_service.get_datetime_for_sorting`, le
moteur déjà employé par `rebuild_produced_exhibits` (la vue
« generate-production »), plutôt qu'une logique parallèle qui divergerait :
`ExhibitableMixin.get_exhibit_date()` en premier, normalisation du fuseau,
repli sur `created_at`, cas particulier des séquences de clavardage.

Le tri porte sur l'horodatage complet. Un courriel de 9 h 14 se range donc après
un document daté du même jour sans heure, celui-ci valant minuit.
"""
import datetime

from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from case_manager.models import BordereauDepotJuillet
from core.mixins import ExhibitableMixin

# Un horodatage antérieur à ce plancher n'est pas une date, c'est une valeur
# sentinelle laissée par une saisie incomplète — P-83 porte 1900-01-01, ce qui
# la placerait en tête du dossier sans que rien ne le signale. Ces pièces
# rejoignent donc celles qui n'ont pas de date du tout : rangées en fin de
# tableau, en attente d'une date. Le jour où elle est saisie, la pièce reprend
# d'elle-même sa place — rien n'étant stocké, il suffit de relancer.
#
# Le plancher est fixé bien au-dessous du corpus : la pièce datée la plus
# ancienne est de janvier 2010, et aucune ne se situe entre 1900 et 2010.
PLANCHER = datetime.date(2000, 1, 1)


def horodatage(obj, nom_modele):
    """
    Reprise fidèle de exhibit_service.get_datetime_for_sorting, adaptée à un
    objet déjà résolu. Toute divergence ici produirait deux ordres différents
    pour la même preuve — celui du cahier et celui de la traduction.
    """
    if obj is None:
        return None

    if isinstance(obj, ExhibitableMixin):
        dt = obj.get_exhibit_date()
        if dt and timezone.is_naive(dt):
            return timezone.make_aware(dt, timezone.get_current_timezone())
        if dt:
            return dt

    dt = None
    if nom_modele == "chatsequence":
        dt = getattr(obj, "start_date", None)
        if not dt and hasattr(obj, "messages") and obj.messages.exists():
            dt = obj.messages.order_by("timestamp").first().timestamp

    if not dt:
        dt = getattr(obj, "created_at", None)

    if dt and timezone.is_naive(dt):
        return timezone.make_aware(dt, timezone.get_current_timezone())
    return dt


class Command(BaseCommand):
    help = "Traduit les cotes déposées en cotes chronologiques."

    def add_arguments(self, parser):
        parser.add_argument("--limite", type=int, default=20,
                            help="nombre de lignes montrées dans l'extrait")
        parser.add_argument("--liasse", default=None,
                            help="détailler la dispersion d'une cote racine, ex. P-43")
        parser.add_argument("--plancher", type=int, default=PLANCHER.year,
                            help="année sous laquelle un horodatage est tenu pour absent")

    def handle(self, *args, **options):
        entrees = []
        sans_date = []          # (motif, entree)
        plancher = options["plancher"]

        cts = {ct.id: ct for ct in ContentType.objects.all()}
        for e in BordereauDepotJuillet.objects.all():
            ct = cts.get(e.content_type_id)
            dt = horodatage(e.content_object, ct.model if ct else "")
            if dt is None:
                sans_date.append(("aucun horodatage", e))
            elif dt.year < plancher:
                sans_date.append((f"horodatage sentinelle ({dt:%Y-%m-%d})", e))
            else:
                entrees.append((dt, e))

        # Tri sur l'horodatage complet. Le départage — type puis PK — n'intervient
        # qu'à horodatage strictement égal ; il est déterministe, donc deux
        # exécutions donnent la même cotation.
        entrees.sort(key=lambda t: (t[0], t[1].source_type, t[1].object_id or 0))
        sans_date.sort(key=lambda t: (t[1].rang, t[1].sous_rang or 0))

        ordre = entrees + [(None, e) for _, e in sans_date]
        traduction = [(i, e, d) for i, (d, e) in enumerate(ordre, start=1)]

        inchangees = sum(1 for i, e, _ in traduction if e.cote == f"P-{i}")
        self.stdout.write("=" * 76)
        self.stdout.write("TRADUCTION — cote déposée → cote chronologique")
        self.stdout.write("=" * 76)
        self.stdout.write(f"  pièces traduites : {len(traduction)}")
        self.stdout.write(f"    cote inchangée : {inchangees}")
        self.stdout.write(f"    cote modifiée  : {len(traduction) - inchangees}")
        if sans_date:
            self.stdout.write("")
            self.stdout.write(self.style.WARNING(
                f"  À DATER — {len(sans_date)} pièce(s) rangée(s) en fin de tableau"))
            self.stdout.write("    Elles reprendront leur place d'elles-mêmes une fois "
                              "la date saisie : rien n'est stocké, il suffit de relancer.")
            rang_debut = len(entrees) + 1
            for n, (motif, e) in enumerate(sans_date):
                self.stdout.write(f"      {e.cote:<10} → P-{rang_debut + n:<6} "
                                  f"{motif:<32} {e.description[:40]}")

        self.stdout.write("")
        self.stdout.write(f"  EXTRAIT — les {options['limite']} premières, "
                          f"par ordre chronologique")
        self.stdout.write(f"    {'nouvelle':<10}{'déposée':<11}{'horodatage':<18}"
                          f"{'type':<13}description")
        for i, e, d in traduction[:options["limite"]]:
            ds = f"{d:%Y-%m-%d %H:%M}" if d else "—"
            self.stdout.write(f"    P-{i:<8}{e.cote:<11}{ds:<18}"
                              f"{e.source_type:<13}{e.description[:40]}")

        if options["liasse"]:
            racine = options["liasse"]
            self.stdout.write("")
            self.stdout.write(f"  DISPERSION DE {racine}")
            for i, e, d in traduction:
                if e.cote_racine == racine:
                    self.stdout.write(f"    {e.cote:<11} → P-{i:<7} {d:%Y-%m-%d %H:%M}")

        self.stdout.write("")
        self.stdout.write("Rien n'a été écrit : la nouvelle cotation est une fonction, "
                          "pas une donnée.")
