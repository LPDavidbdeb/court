"""
Enregistre en base le bordereau du dépôt du 24 juillet 2026.

    python manage.py import_bordereau_depot_juillet --dry-run
    python manage.py import_bordereau_depot_juillet

DEUX FICHIERS, DEUX RÔLES — c'est le point qu'il ne faut pas confondre.

  `legal/bordereau_pieces.md`  le registre VIVANT. Il dit quelles pièces
                               existent. Il continue de grossir : des pièces
                               sont versées après le dépôt.
  la copie GELÉE du dépôt      `legal/depots/2026-07-24_initial/candidats/
                               bordereau_pieces.md`. Elle seule dit quelle cote
                               une pièce a reçue AU DÉPÔT.

La colonne `cote` est celle de juillet. Elle ne peut donc venir que du fichier
gelé. La lire dans le fichier vivant — ce que faisait cette commande — donne une
cote de juillet à des pièces versées en août : la table censée figer un constat
se met alors à suivre une source qui bouge. Une pièce du registre vivant absente
du gelé reçoit `cote = NULL`, avec `cote_racine`, `rang` et `sous_rang` vides
eux aussi : ces trois colonnes ne sont que la cote de juillet découpée, elles
n'ont aucun contenu possible sans elle.

L'APPARIEMENT SE FAIT PAR LA PIÈCE, PAS PAR LA COTE. Une pièce est un modèle et
un pk ; c'est la seule chose que les deux fichiers désignent de façon stable. Un
appariement par chaîne de cote avalerait en silence toute divergence de notation
entre les deux fichiers.

DÉVELOPPEMENT DES LIASSES — c'est l'apport de la table.
Une ligne du bordereau qui vise plusieurs pièces (« P-43 | Liasse de 19
courriels ») produit ici 19 lignes, cotées P-43.1 à P-43.19, dans l'ordre où les
identifiants figurent au bordereau. Une ligne qui ne vise qu'une pièce produit
une seule ligne, cotée P-43, sans sous-rang.

LA COMMANDE N'EFFACE PLUS RIEN. Elle remplaçait la table entière à chaque
passage, ce qui emportait les pièces versées par `verser_piece` — absentes du
registre vivant, donc invisibles à l'import — et se heurte désormais à la clé
`PROTECT` d'`AppuiDepotJuillet`. Chaque pièce est mise à jour sur sa clé
naturelle (modèle + pk) ; les lignes que le registre ne mentionne plus sont
signalées, jamais supprimées.
"""
import re
from pathlib import Path

from django.conf import settings
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


# La copie gelée du bordereau, telle qu'elle était au dépôt. Le répertoire
# `legal/depots/2026-07-24_initial/` porte son propre avertissement : « Répertoire
# gelé. Aucun fichier de ce répertoire ne doit être modifié. » On n'y lit jamais
# que la cotation.
BORDEREAU_DEPOT_PATH = (Path(settings.BASE_DIR) / "legal" / "depots" /
                        "2026-07-24_initial" / "candidats" / "bordereau_pieces.md")


def cotation_du_depot(chemin=BORDEREAU_DEPOT_PATH):
    """
    `{(content_type_id, object_id): (cote, cote_racine, rang, sous_rang)}`.

    La cotation de juillet, lue dans le fichier gelé et indexée PAR PIÈCE. Le
    développement des liasses suit exactement la logique de l'import principal —
    même parseur, même résolution, même ordre — pour que la cote attribuée ici
    soit celle que le bordereau déposé porte réellement.
    """
    index = {}
    for row in parse_bordereau(chemin):
        m = re.match(r"P-(\d+)", row.cote)
        if not m:
            continue
        rang = int(m.group(1))
        racine = f"P-{rang}"

        ref = resolve_source(row) or rattraper_source(row)
        if ref is None:
            continue

        couples = resoudre_objets(ref)
        liasse = len(couples) > 1
        for i, (obj, _motif) in enumerate(couples, start=1):
            if obj is None:
                continue
            ct = ContentType.objects.get_for_model(obj)
            cote = f"{racine}.{i}" if liasse else racine
            index[(ct.id, obj.pk)] = (cote, racine, rang, i if liasse else None)
    return index


class Command(BaseCommand):
    help = "Enregistre le bordereau du dépôt du 24 juillet 2026 en base."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true",
                            help="rapport seul, aucune écriture")

    def handle(self, *args, **options):
        dry = options["dry_run"]

        rows = parse_bordereau(BORDEREAU_PATH)
        self.stdout.write(f"Registre vivant lu : {len(rows)} lignes de cote "
                          f"({BORDEREAU_PATH.name})")

        depot = cotation_du_depot()
        self.stdout.write(f"Cotation du dépôt lue : {len(depot)} pièces cotées "
                          f"en juillet ({BORDEREAU_DEPOT_PATH.parent.parent.name})")

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
                # Sans référence model+pk, la ligne ne peut être appariée au
                # fichier gelé : on ne peut pas AFFIRMER qu'elle a été déposée,
                # donc on ne lui attribue pas de cote de juillet.
                entrees.append(dict(
                    cote=None, cote_racine=None, rang=None, sous_rang=None,
                    ct=None, oid=None, source_type="", source_ref=row.fichier_appui,
                    date_libelle=row.date, description=row.description,
                    resolu=False,
                    note=f"aucune référence model+pk lisible dans la ligne "
                         f"(cote {row.cote} au registre vivant, non appariable "
                         f"au bordereau gelé)",
                ))
                non_resolues.append((row.cote, "référence illisible"))
                continue

            couples = resoudre_objets(ref)
            liasse = len(couples) > 1

            for i, (obj, motif) in enumerate(couples, start=1):
                ct = ContentType.objects.get_for_model(obj) if obj else None

                # La cote de juillet vient du fichier GELÉ, jamais du registre
                # vivant. Une pièce que le dépôt ne contenait pas n'a pas de
                # cote de juillet, donc pas de racine, de rang ni de sous-rang.
                cote, cote_racine, rang_juillet, sous_rang = (None, None, None, None)
                if ct and obj:
                    trouve = depot.get((ct.id, obj.pk))
                    if trouve:
                        cote, cote_racine, rang_juillet, sous_rang = trouve
                # le type stocké suit l'objet réellement retenu, pas le type
                # annoncé par le bordereau : une redirection photo -> photodoc
                # doit se lire dans la table
                type_reel = ct.model if ct else ref.kind
                entrees.append(dict(
                    cote=cote, cote_racine=cote_racine, rang=rang_juillet,
                    sous_rang=sous_rang,
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

        avec_cote = sum(1 for e in entrees if e["cote"])
        self.stdout.write("")
        self.stdout.write(f"  COTE DE JUILLET (fichier gelé) : {avec_cote}")
        self.stdout.write(f"  SANS cote de juillet — versées après le dépôt : "
                          f"{len(entrees) - avec_cote}")

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

        # UPSERT SUR LA CLÉ NATURELLE (modèle + pk). Une pièce est un objet de la
        # base ; c'est par lui qu'on la retrouve d'un passage à l'autre. La
        # remise à zéro d'autrefois emportait les pièces versées hors registre
        # et se heurte à la clé PROTECT d'AppuiDepotJuillet.
        crees = majs = 0
        vues = set()
        with transaction.atomic():
            # Les cotes sont uniques : on les libère avant de les réattribuer,
            # sinon une pièce qui perd sa cote de juillet la laisse occupée.
            BordereauDepotJuillet.objects.exclude(cote=None).update(
                cote=None, cote_racine=None, rang=None, sous_rang=None)

            for e in entrees:
                champs = dict(
                    cote=e["cote"], cote_racine=e["cote_racine"],
                    rang=e["rang"], sous_rang=e["sous_rang"],
                    source_type=e["source_type"],
                    source_ref=e["source_ref"][:500],
                    date_libelle=e["date_libelle"][:200],
                    description=e["description"],
                    resolu=e["resolu"], note=e["note"],
                )
                if e["ct"] is None or e["oid"] is None:
                    BordereauDepotJuillet.objects.create(
                        content_type=None, object_id=None, **champs)
                    crees += 1
                    continue
                _obj, neuf = BordereauDepotJuillet.objects.update_or_create(
                    content_type=e["ct"], object_id=e["oid"], defaults=champs)
                vues.add((e["ct"].id, e["oid"]))
                crees += 1 if neuf else 0
                majs += 0 if neuf else 1

            # Ce que le registre ne mentionne plus. Jamais supprimé : une pièce
            # peut avoir été versée par `verser_piece`, ou être invoquée par un
            # paragraphe déjà persisté.
            absentes = [e for e in BordereauDepotJuillet.objects.exclude(content_type=None)
                        if (e.content_type_id, e.object_id) not in vues]

        self.stdout.write("")
        self.stdout.write(f"  créées : {crees}   mises à jour : {majs}")
        if absentes:
            self.stdout.write("")
            self.stdout.write(self.style.WARNING(
                f"  HORS REGISTRE — {len(absentes)} ligne(s) que "
                f"{BORDEREAU_PATH.name} ne mentionne pas. Conservées."))
            for e in absentes[:20]:
                self.stdout.write(f"    {e.source_type:<14} {e.description[:52]}")

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Écrit : {BordereauDepotJuillet.objects.count()} pièces cotées."))
