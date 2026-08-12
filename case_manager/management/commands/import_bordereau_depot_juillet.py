"""
Enregistre en base le bordereau du dépôt du 24 juillet 2026.

    python manage.py import_bordereau_depot_juillet --dry-run
    python manage.py import_bordereau_depot_juillet

Lit `legal/bordereau_pieces.md` en LECTURE SEULE et remplit
`case_manager.BordereauDepotJuillet` : une ligne par pièce, avec la cote qui lui
a été donnée au dépôt.

Le parsing réutilise `parse_bordereau` et `resolve_source` de `sync_pieces`, et
la résolution en objets Django reprend la logique de `sync_pieces_pdf`. Rien
n'est réécrit ici : si le bordereau change, c'est ce même moteur qui suit.

DÉVELOPPEMENT DES LIASSES — c'est l'apport de la table.
Une ligne du bordereau qui vise plusieurs pièces (« P-43 | Liasse de 19
courriels ») produit ici 19 lignes, cotées P-43.1 à P-43.19, dans l'ordre où les
identifiants figurent au bordereau. Une ligne qui ne vise qu'une pièce produit
une seule ligne, cotée P-43, sans sous-rang.
"""
import re

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction

from case_manager.models import BordereauDepotJuillet
from case_manager.management.commands.sync_pieces import (
    BORDEREAU_PATH,
    parse_bordereau,
    resolve_source,
)


# Rattrapage d'un angle mort de sync_pieces.resolve_source : une référence au
# PLURIEL portant un IDENTIFIANT UNIQUE — « emails-401 » — n'est reconnue par
# aucun de ses motifs. Le motif « liste » exige au moins un « / »
# (\d+(?:/\d+)+), et le motif simple ancre sur « email- », que le « s » de
# « emails- » fait échouer. Deux cotes du bordereau tombent dans ce trou.
#
# On ne corrige pas sync_pieces ici : ce module produit le cahier déposé, sa
# modification relève d'une décision distincte. Le rattrapage reste local.
PLURIEL_ID_UNIQUE = [
    ("pdf", r"\bpdfs-(\d+)\b"),
    ("email", r"\bemails-(\d+)\b"),
    ("event", r"\bevents-(\d+)\b"),
    ("photodoc", r"\bphotodocs-(\d+)\b"),
    ("photo", r"\bphotos-(\d+)\b"),
]


def rattraper_source(row):
    """Dernier recours quand resolve_source ne reconnaît rien."""
    from case_manager.management.commands.sync_pieces import SourceRef

    texte = f"{row.fichier_appui} | {row.source_base}"
    for kind, motif in PLURIEL_ID_UNIQUE:
        m = re.search(motif, texte, re.IGNORECASE)
        if m:
            return SourceRef(kind, (m.group(1),))
    return None


def resoudre_objets(ref):
    """
    SourceRef -> [(objet, motif_d_echec), ...], un couple par identifiant.

    Contrairement à `sync_pieces_pdf.resolve_objects`, on ne lève pas sur une
    cible absente : un constat de dépôt doit pouvoir enregistrer une cote dont
    la pièce ne se retrouve pas en base, en le disant.
    """
    from document_manager.models import Document
    from email_manager.models import Email, EmailThread
    from events.models import Event
    from googlechat_manager.models import ChatSequence
    from pdf_manager.models import PDFDocument
    from photos.models import Photo, PhotoDocument

    MODELES = {
        "pdf": PDFDocument,
        "photo": Photo,
        "photodoc": PhotoDocument,
        "event": Event,
        "email": Email,
        "document": Document,
        "chatsequence": ChatSequence,
        "thread": EmailThread,
    }

    modele = MODELES.get(ref.kind)
    if modele is None:
        return [(None, f"type non supporté : {ref.kind}")]

    resultats = []
    for brut in ref.ids:
        try:
            if ref.kind == "thread" and not str(brut).isdigit():
                obj = modele.objects.get(thread_id=brut)
            else:
                obj = modele.objects.get(pk=int(brut))

            # Une pièce photographique produite au dossier est un PhotoDocument —
            # une unité titrée et décrite — et non le fichier image brut. Le
            # bordereau et SOURCE_OVERRIDES visent parfois la Photo ; on remonte
            # alors à son document, à condition qu'il soit unique, sinon on
            # laisse la référence telle quelle en le disant. C'est cette cible
            # qui porte la date exploitable (min des prises de vue).
            if ref.kind == "photo":
                docs = list(PhotoDocument.objects.filter(photos=obj))
                if len(docs) == 1:
                    resultats.append((docs[0],
                                      f"référence redirigée : Photo {obj.pk} → "
                                      f"PhotoDocument {docs[0].pk}"))
                    continue
                if len(docs) > 1:
                    resultats.append((obj, f"Photo {obj.pk} appartient à "
                                           f"{len(docs)} PhotoDocument — non redirigée"))
                    continue

            resultats.append((obj, ""))
        except modele.DoesNotExist:
            resultats.append((None, f"{ref.kind} {brut} absent de la base"))
        except (ValueError, TypeError):
            resultats.append((None, f"identifiant illisible : {brut!r}"))
    return resultats


class Command(BaseCommand):
    help = "Enregistre le bordereau du dépôt du 24 juillet 2026 en base."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true",
                            help="rapport seul, aucune écriture")

    def handle(self, *args, **options):
        dry = options["dry_run"]

        rows = parse_bordereau(BORDEREAU_PATH)
        self.stdout.write(f"Bordereau lu : {len(rows)} lignes de cote "
                          f"({BORDEREAU_PATH.name})")

        entrees = []
        non_resolues = []

        for row in rows:
            m = re.match(r"P-(\d+)", row.cote)
            if not m:
                non_resolues.append((row.cote, "cote illisible"))
                continue
            rang = int(m.group(1))
            racine = f"P-{rang}"

            ref = resolve_source(row)
            rattrape = False
            if ref is None:
                ref = rattraper_source(row)
                rattrape = ref is not None
            if ref is None:
                entrees.append(dict(
                    cote=racine, cote_racine=racine, rang=rang, sous_rang=None,
                    ct=None, oid=None, source_type="", source_ref=row.fichier_appui,
                    date_libelle=row.date, description=row.description,
                    resolu=False,
                    note="aucune référence model+pk lisible dans la ligne",
                ))
                non_resolues.append((row.cote, "référence illisible"))
                continue

            couples = resoudre_objets(ref)
            liasse = len(couples) > 1

            for i, (obj, motif) in enumerate(couples, start=1):
                cote = f"{racine}.{i}" if liasse else racine
                ct = ContentType.objects.get_for_model(obj) if obj else None
                # le type stocké suit l'objet réellement retenu, pas le type
                # annoncé par le bordereau : une redirection photo -> photodoc
                # doit se lire dans la table
                type_reel = ct.model if ct else ref.kind
                entrees.append(dict(
                    cote=cote, cote_racine=racine, rang=rang,
                    sous_rang=i if liasse else None,
                    ct=ct, oid=(obj.pk if obj else None),
                    source_type=type_reel, source_ref=row.fichier_appui,
                    date_libelle=row.date, description=row.description,
                    resolu=obj is not None,
                    note=motif or ("résolu par rattrapage : référence au pluriel "
                                   "à identifiant unique, non reconnue par "
                                   "sync_pieces.resolve_source" if rattrape else ""),
                ))
                if obj is None:
                    non_resolues.append((cote, motif))

        liasses = {e["cote_racine"] for e in entrees if e["sous_rang"]}
        resolues = sum(1 for e in entrees if e["resolu"])

        self.stdout.write("")
        self.stdout.write(f"  pièces adressables produites : {len(entrees)}")
        self.stdout.write(f"    dont issues d'une liasse   : "
                          f"{sum(1 for e in entrees if e['sous_rang'])} "
                          f"réparties sur {len(liasses)} liasse(s)")
        self.stdout.write(f"  rattachées à un objet réel   : {resolues}")
        self.stdout.write(f"  NON résolues                 : {len(entrees) - resolues}")

        par_type = {}
        for e in entrees:
            par_type[e["source_type"] or "(aucun)"] = par_type.get(e["source_type"] or "(aucun)", 0) + 1
        self.stdout.write("  par type de source : " +
                          ", ".join(f"{k} {v}" for k, v in sorted(par_type.items())))

        if non_resolues:
            self.stdout.write("")
            self.stdout.write(self.style.WARNING("  À vérifier :"))
            for cote, motif in non_resolues:
                self.stdout.write(f"    {cote:<10} {motif}")

        if dry:
            self.stdout.write("")
            self.stdout.write("--dry-run : rien n'a été écrit.")
            return

        with transaction.atomic():
            BordereauDepotJuillet.objects.all().delete()
            BordereauDepotJuillet.objects.bulk_create([
                BordereauDepotJuillet(
                    cote=e["cote"], cote_racine=e["cote_racine"],
                    rang=e["rang"], sous_rang=e["sous_rang"],
                    content_type=e["ct"], object_id=e["oid"],
                    source_type=e["source_type"], source_ref=e["source_ref"][:500],
                    date_libelle=e["date_libelle"][:200],
                    description=e["description"],
                    resolu=e["resolu"], note=e["note"],
                )
                for e in entrees
            ])

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Écrit : {BordereauDepotJuillet.objects.count()} pièces cotées."))
