"""
Union des pièces d'une fenêtre temporelle — l'extension qui réfute une allégation
d'extension.

    python manage.py union_temporelle --fenetre ete_2013
    python manage.py union_temporelle --debut 2013-06-27 --fin 2013-08-31
    python manage.py union_temporelle --fenetre ete_2013 --detail

POURQUOI UNE UNION PLUTÔT QU'UNE LISTE

Le § 9 de la Requête du 19 novembre 2015 allègue : « En 2013, le défendeur est
parti tout l'été et a laissé la demanderesse seule avec les deux (2) enfants. »
C'est une affirmation d'EXTENSION — « tout l'été », « seule ». Elle ne se réfute
pas par un contre-exemple mais par le remplissage de la période. L'appui du
paragraphe qui la conteste n'est donc pas une liste choisie à la main : c'est
tout ce que la base contient entre deux dates.

LES PHOTOS NE SONT JAMAIS ATTEINTES DIRECTEMENT

Une photographie isolée n'est pas une pièce : elle le devient par l'unité qui la
porte — un `Event` daté, ou un `PhotoDocument` titré. Interroger `Photo`
directement produirait des centaines d'items sans contexte ni cote. L'union porte
donc sur les UNITÉS CITABLES, et les photos y entrent par leur contenant.

Un `EmailThread` est volontairement exclu : ses courriels sont déjà comptés
individuellement, et l'inclure les compterait deux fois.

LES BORNES SONT UN CHOIX D'ARGUMENTATION

« Tout l'été » n'a pas de définition dans la base. L'été astronomique, le
« 27 juin à la fin d'août » du paragraphe 47, ou les vacances scolaires donnent
trois unions différentes. Les fenêtres sont donc nommées et déclarées ici, pour
que l'union soit reproductible et que la borne retenue soit discutable comme
telle.
"""
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from case_manager.models import BordereauDepotJuillet
from email_manager.models import Email
from events.models import Event
from googlechat_manager.models import ChatSequence
from pdf_manager.models import PDFDocument
from photos.models import Photo, PhotoDocument


FENETRES = {
    # nom          début         fin           ce que la borne prétend couvrir
    "ete_2013": (datetime.date(2013, 6, 21), datetime.date(2013, 9, 21),
                 "été astronomique — la lecture la plus large de « tout l'été »"),
    "ete_2013_par47": (datetime.date(2013, 6, 27), datetime.date(2013, 8, 31),
                       "« du 27 juin à la fin d'août », borne du paragraphe 47"),
    "ete_2013_scolaire": (datetime.date(2013, 6, 24), datetime.date(2013, 8, 26),
                          "vacances scolaires québécoises 2013"),
}


# ---------------------------------------------------------------------------
# EXCLUSIONS — à remplir au fur et à mesure.
#
# L'union temporelle donne les CANDIDATS, pas la preuve. Un objet situé dans la
# fenêtre peut n'avoir aucun rapport avec la présence du père — voire la
# desservir. Chaque exclusion se déclare ici, par modèle, sous forme de Q()
# combinés par ET avec la fenêtre. Écrire l'exclusion plutôt que d'élaguer la
# liste à la main garde l'union reproductible : deux exécutions donnent le même
# ensemble, et le motif du retrait reste lisible.
# ---------------------------------------------------------------------------
EXCLUSIONS = {
    "Email": [
        # ex. ~Q(sender_protagonist__isnull=True),
    ],
    "Event": [
        # ex. ~Q(explanation__icontains="…"),
    ],
    "PhotoDocument": [],
    "PDFDocument": [],
    "ChatSequence": [],
}


def appliquer(qs, nom):
    for condition in EXCLUSIONS.get(nom, []):
        qs = qs.filter(condition)
    return qs


class Command(BaseCommand):
    help = "Union des pièces citables d'une fenêtre temporelle."

    def add_arguments(self, parser):
        parser.add_argument("--fenetre", choices=sorted(FENETRES),
                            help="fenêtre nommée, déclarée dans FENETRES")
        parser.add_argument("--debut", help="AAAA-MM-JJ, si fenêtre libre")
        parser.add_argument("--fin", help="AAAA-MM-JJ, si fenêtre libre")
        parser.add_argument("--detail", action="store_true",
                            help="lister chaque objet de l'union")

    def handle(self, *args, **options):
        if options["fenetre"]:
            debut, fin, motif = FENETRES[options["fenetre"]]
            titre = options["fenetre"]
        elif options["debut"] and options["fin"]:
            debut = datetime.date.fromisoformat(options["debut"])
            fin = datetime.date.fromisoformat(options["fin"])
            titre, motif = "fenêtre libre", "bornes passées en argument"
        else:
            raise CommandError("Préciser --fenetre, ou --debut et --fin.")

        self.stdout.write("=" * 76)
        self.stdout.write(f"UNION TEMPORELLE — {titre}")
        self.stdout.write("=" * 76)
        self.stdout.write(f"  du {debut} au {fin}")
        self.stdout.write(f"  borne : {motif}")

        # Unités citables. Photo n'y figure pas : elle entre par son contenant.
        groupes = [
            ("Email", appliquer(Email.objects.filter(
                date_sent__date__gte=debut, date_sent__date__lte=fin), "Email")),
            ("Event", appliquer(Event.objects.filter(
                date__gte=debut, date__lte=fin), "Event")),
            ("PhotoDocument", appliquer(PhotoDocument.objects.filter(
                photos__datetime_original__date__gte=debut,
                photos__datetime_original__date__lte=fin).distinct(), "PhotoDocument")),
            ("PDFDocument", appliquer(PDFDocument.objects.filter(
                document_date__gte=debut, document_date__lte=fin), "PDFDocument")),
            ("ChatSequence", appliquer(ChatSequence.objects.filter(
                start_date__date__gte=debut, start_date__date__lte=fin), "ChatSequence")),
        ]

        cotees = {(e.content_type_id, e.object_id): e.cote
                  for e in BordereauDepotJuillet.objects.all()}

        self.stdout.write("")
        self.stdout.write(f"  {'modèle':<16}{'objets':>7}{'cotés':>8}{'à coter':>9}"
                          f"   {'exclusions':>10}")
        total = deja = 0
        for nom, qs in groupes:
            ct = ContentType.objects.get_for_model(qs.model).id
            pks = list(qs.values_list("pk", flat=True))
            n_cot = sum(1 for pk in pks if (ct, pk) in cotees)
            total += len(pks); deja += n_cot
            self.stdout.write(f"  {nom:<16}{len(pks):>7}{n_cot:>8}{len(pks)-n_cot:>9}"
                              f"   {len(EXCLUSIONS.get(nom, [])):>10}")
        self.stdout.write(f"  {'—':<16}{'—':>7}{'—':>8}{'—':>9}")
        self.stdout.write(f"  {'UNION':<16}{total:>7}{deja:>8}{total-deja:>9}")

        # Les photos de la fenêtre qu'aucune unité citable ne porte seraient
        # invisibles à l'union : elles existent, mais rien ne permet de les citer.
        photos = Photo.objects.filter(datetime_original__date__gte=debut,
                                      datetime_original__date__lte=fin)
        orphelines = photos.filter(events__isnull=True,
                                   photo_documents__isnull=True).distinct()
        self.stdout.write("")
        self.stdout.write(f"  photos de la fenêtre : {photos.count()}, "
                          f"portées par un Event ou un PhotoDocument : "
                          f"{photos.count() - orphelines.count()}")
        if orphelines.exists():
            self.stdout.write(self.style.WARNING(
                f"    {orphelines.count()} photo(s) ORPHELINE(S) — inatteignables, "
                f"donc absentes de l'union :"))
            for p in orphelines[:10]:
                self.stdout.write(f"      photo {p.pk} — {p} — "
                                  f"{p.datetime_original:%Y-%m-%d}")

        if not options["detail"]:
            self.stdout.write("")
            self.stdout.write("  --detail pour lister chaque objet de l'union.")
            return

        for nom, qs in groupes:
            if not qs.exists():
                continue
            ct = ContentType.objects.get_for_model(qs.model).id
            self.stdout.write("")
            self.stdout.write(f"  --- {nom} ({qs.count()})")
            for o in qs:
                cote = cotees.get((ct, o.pk), "—")
                d = o.get_exhibit_date() if hasattr(o, "get_exhibit_date") else None
                ds = f"{d:%Y-%m-%d}" if d else "?"
                extra = ""
                if nom == "Event":
                    extra = f" [{o.linked_photos.count()} photo(s)]"
                self.stdout.write(f"      {cote:<9} {ds}  pk={o.pk:<6} "
                                  f"{str(o)[:60]}{extra}")
