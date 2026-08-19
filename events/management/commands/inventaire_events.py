"""
Inventaire des descriptions d'événements, regroupées par similitude.

    python manage.py inventaire_events
    python manage.py inventaire_events --membres        # lister chaque membre
    python manage.py inventaire_events --min-groupe 3

Les descriptions d'`Event` ont été produites en série : beaucoup partagent un
même moule dont seuls la date, l'heure et les prénoms changent. Les inventorier
sans les regrouper donnerait 319 lignes illisibles ; les regrouper par leur
SQUELETTE — la phrase une fois ôtés date, heure et chiffres — fait apparaître
les moules, donc les catégories réelles de la preuve événementielle.

Trois lectures sont produites :

  1. LE MOULE      — squelette de phrase, ce qui révèle les patrons de rédaction
  2. LE LIEU       — « at his house », « in Cape Cod », extrait de la phrase
  3. LES PERSONNES — qui est nommé comme présent

Un défaut de qualité y devient visible : descriptions identiques répétées,
horodatage recopié dans le texte, mélange français / anglais.
"""
import re
import unicodedata
from collections import Counter, defaultdict

from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

from case_manager.models import BordereauDepotJuillet
from events.models import Event

# Ce qui varie d'un événement à l'autre et doit disparaître du squelette.
RE_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
RE_HEURE = re.compile(r"\b\d{1,2}[:h]\d{2}\b")
RE_NOMBRE = re.compile(r"\b\d+\b")
RE_ESPACES = re.compile(r"\s+")

PRENOMS = ["alexia", "nicolas", "nicholas", "elise", "élise", "lp",
           "sandrine", "annie-claude", "josée", "johanne"]

# « at his house », « in Cape Cod », « at the Montreal Jazz Festival »…
RE_LIEU = re.compile(r"\b(?:at|in)\s+(?:the\s+|his\s+|her\s+|a\s+)?"
                     r"([a-zà-ÿ'\-]+(?:\s+[a-zà-ÿ'\-]+){0,3})", re.I)

MOTS_LIEU_IGNORES = {"his", "her", "the", "a", "and", "with", "between", "is",
                     "picture", "pictures", "of", "he", "she", "it", "them"}


def squelette(texte):
    """La phrase une fois ôtés date, heure, chiffres et prénoms."""
    t = unicodedata.normalize("NFKC", texte or "").lower()
    t = RE_DATE.sub("«date»", t)
    t = RE_HEURE.sub("«heure»", t)
    t = RE_NOMBRE.sub("«n»", t)
    for p in PRENOMS:
        t = re.sub(rf"\b{re.escape(p)}\b", "«qui»", t)
    t = re.sub(r"[^a-zà-ÿ«»\s]", " ", t)
    return RE_ESPACES.sub(" ", t).strip()


def lieux(texte):
    out = []
    for m in RE_LIEU.finditer(texte or ""):
        mots = [w for w in m.group(1).split()
                if w.lower() not in MOTS_LIEU_IGNORES]
        if mots:
            out.append(" ".join(mots[:3]).lower())
    return out


class Command(BaseCommand):
    help = "Inventaire groupé des descriptions d'événements."

    def add_arguments(self, parser):
        parser.add_argument("--membres", action="store_true",
                            help="lister les événements de chaque groupe")
        parser.add_argument("--min-groupe", type=int, default=2,
                            help="taille minimale d'un groupe affiché")

    def handle(self, *args, **options):
        ct = ContentType.objects.get_for_model(Event).id
        cotes = {e.object_id: e.cote for e in
                 BordereauDepotJuillet.objects.filter(content_type_id=ct)}

        evs = list(Event.objects.all().order_by("date", "pk"))
        sans_texte = [e for e in evs if not (e.explanation or "").strip()]
        avec = [e for e in evs if (e.explanation or "").strip()]

        self.stdout.write("=" * 82)
        self.stdout.write("INVENTAIRE DES DESCRIPTIONS D'ÉVÉNEMENTS")
        self.stdout.write("=" * 82)
        self.stdout.write(f"  événements            : {len(evs)}")
        self.stdout.write(f"    avec description    : {len(avec)}")
        self.stdout.write(f"    SANS description    : {len(sans_texte)}")
        cotes_n = sum(1 for e in evs if e.pk in cotes)
        self.stdout.write(f"    cotés au registre   : {cotes_n}")

        # --- langue -----------------------------------------------------
        anglais = [e for e in avec
                   if re.search(r"\b(is|at|with|his|her|the)\b",
                                (e.explanation or "").lower())]
        francais = [e for e in avec if e not in anglais]
        self.stdout.write("")
        self.stdout.write(f"  rédigées en anglais   : {len(anglais)}")
        self.stdout.write(f"  rédigées en français  : {len(francais)}")

        # --- doublons stricts -------------------------------------------
        exact = defaultdict(list)
        for e in avec:
            exact[RE_ESPACES.sub(" ", (e.explanation or "").strip())].append(e)
        doublons = {k: v for k, v in exact.items() if len(v) > 1}
        self.stdout.write("")
        self.stdout.write(f"  descriptions STRICTEMENT identiques : {len(doublons)} "
                          f"groupe(s), {sum(len(v) for v in doublons.values())} événements")
        for texte, membres in sorted(doublons.items(), key=lambda kv: -len(kv[1]))[:6]:
            dates = ", ".join(f"{e.date}" for e in membres[:5])
            self.stdout.write(f"      ×{len(membres):<3} « {texte[:62]} »")
            self.stdout.write(f"           {dates}")

        # --- horodatage recopié dans le texte ---------------------------
        recopie = [e for e in avec if RE_DATE.search(e.explanation or "")]
        double_heure = [e for e in avec
                        if len(RE_HEURE.findall(e.explanation or "")) > 2]
        self.stdout.write("")
        self.stdout.write(f"  texte recopiant la date de l'événement : {len(recopie)}")
        self.stdout.write(f"  texte portant plus de deux heures      : {len(double_heure)}"
                          f"   (horodatage dupliqué à la génération)")

        # --- groupes par moule ------------------------------------------
        moules = defaultdict(list)
        for e in avec:
            moules[squelette(e.explanation)].append(e)
        groupes = sorted(moules.items(), key=lambda kv: -len(kv[1]))
        retenus = [(k, v) for k, v in groupes if len(v) >= options["min_groupe"]]
        isoles = [v[0] for k, v in groupes if len(v) < options["min_groupe"]]

        self.stdout.write("")
        self.stdout.write("=" * 82)
        self.stdout.write(f"  GROUPES PAR MOULE — {len(retenus)} groupe(s) d'au moins "
                          f"{options['min_groupe']} événements, {len(isoles)} isolé(s)")
        self.stdout.write("=" * 82)
        for sq, membres in retenus:
            periode = f"{min(e.date for e in membres)} → {max(e.date for e in membres)}"
            n_cotes = sum(1 for e in membres if e.pk in cotes)
            self.stdout.write("")
            self.stdout.write(f"  ×{len(membres):<4} {periode}   cotés {n_cotes}/{len(membres)}")
            self.stdout.write(f"        moule : {sq[:74]}")
            self.stdout.write(f"        ex.   : {(membres[0].explanation or '')[:74]}")
            if options["membres"]:
                for e in membres:
                    self.stdout.write(f"           E-{e.pk:<5} {e.date} "
                                      f"[{cotes.get(e.pk,'—'):<9}] "
                                      f"{e.linked_photos.count():>2}ph")

        # --- lieux ------------------------------------------------------
        compteur_lieux = Counter()
        for e in avec:
            for l in set(lieux(e.explanation)):
                compteur_lieux[l] += 1
        self.stdout.write("")
        self.stdout.write("=" * 82)
        self.stdout.write("  LIEUX LES PLUS FRÉQUENTS")
        self.stdout.write("=" * 82)
        for lieu, n in compteur_lieux.most_common(18):
            if n >= 2:
                self.stdout.write(f"    ×{n:<4} {lieu}")

        # --- personnes --------------------------------------------------
        self.stdout.write("")
        self.stdout.write("=" * 82)
        self.stdout.write("  PERSONNES NOMMÉES")
        self.stdout.write("=" * 82)
        cpt = Counter()
        for e in avec:
            t = (e.explanation or "").lower()
            for p in ("alexia", "nicolas", "elise", "lp"):
                motif = "nicolas|nicholas" if p == "nicolas" else \
                        ("elise|élise" if p == "elise" else p)
                if re.search(rf"\b(?:{motif})\b", t):
                    cpt[p] += 1
        for p, n in cpt.most_common():
            self.stdout.write(f"    ×{n:<4} {p}")

        seul_pere_enfant = [
            e for e in avec
            if re.search(r"\blp\b", (e.explanation or "").lower())
            and not re.search(r"\b(?:elise|élise)\b", (e.explanation or "").lower())
            and re.search(r"\b(?:alexia|nicolas|nicholas)\b", (e.explanation or "").lower())
        ]
        self.stdout.write("")
        self.stdout.write(f"    dont LP avec un enfant SANS mention d'Élise : "
                          f"{len(seul_pere_enfant)}")
