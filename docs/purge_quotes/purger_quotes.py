#!/usr/bin/env python
"""
Suppression de citations — toutes, ou une selection — en traitant ce que Django ne
nettoie pas tout seul.

    # purge totale
    .venv/bin/python docs/purge_quotes/purger_quotes.py --dry-run
    .venv/bin/python docs/purge_quotes/purger_quotes.py --apply

    # suppression ciblee
    .venv/bin/python docs/purge_quotes/purger_quotes.py --dry-run --email 58,76 --pdf 12
    .venv/bin/python docs/purge_quotes/purger_quotes.py --apply --fichier a_supprimer.txt

SANS --email / --pdf / --fichier, la selection est TOUTE la base : c'est le mode purge
totale. Avec, le script ne vise que ces citations-la, et tout ce qu'il rapporte —
cascades, cles generiques, impact sur les pieces parentes — porte sur cette seule
selection. Une PK demandee qui n'existe pas arrete le script : c'est une faute de
frappe, pas un no-op silencieux.

CE QUE LA SELECTION CHANGE POUR LES PIECES PARENTES. refresh_case_exhibits n'inscrit
pas les citations, il inscrit leur PARENT, et il ne l'atteint qu'a travers
citations_courriel / citations_pdf. Une piece reste donc inscrite tant qu'il lui reste
UNE citation adossee a une trame, et sort du registre quand la derniere part. Ce
comptage n'est pas a ecrire : refresh recalcule l'ensemble depuis les trames et l'union
tranche seule. Le rapport le montre piece par piece avant d'ecrire.

DEUX MODELES, aucun troisieme : email_manager.Quote et pdf_manager.Quote. Le scan des
cles generiques (ci-dessous) verifie a chaque execution que rien d'autre ne pointe sur
elles ; si un modele inconnu apparait un jour, --apply refuse de s'executer plutot que
de laisser ses lignes dans le vide.

CE QUE DJANGO FAIT SEUL — les vraies cles etrangeres :
    les tables de liaison TrameNarrative.citations_courriel / .citations_pdf tombent
    en cascade avec les citations.

CE QUE DJANGO NE FAIT PAS — les cles generiques n'ont aucune contrainte en base, donc
aucune cascade. Leurs lignes survivent avec un object_id qui ne designe plus rien :

    document_manager.LibraryNode   les noeuds-citation des documents PRODUCED.
                                   C'est du CONTENU, pas de la donnee derivee.
    case_manager.ProducedExhibit   derivee EN PRINCIPE, reconstruite par
                                   rebuild_produced_exhibits() — mais pas partout,
                                   voir ci-dessous.

PRODUCEDEXHIBIT N'EST PAS UNIFORMEMENT DERIVEE. Le rebuild vide la table puis la
repeuple depuis ExhibitRegistry. Un dossier dont l'ExhibitRegistry est VIDE alors que
ses ProducedExhibit sont remplis n'a aucune source de reconstruction : le rebuild le
mettrait a zero. `cases_non_reconstructibles()` detecte ces dossiers et le script les
EPARGNE par defaut, y compris sous --refresh. --forcer-non-reconstructibles passe outre,
avec perte definitive.

CE QUE LA PURGE FAIT A LA COTATION. refresh_case_exhibits n'enregistre PAS les citations :
il enregistre leur PARENT (l'Email, le PDFDocument), et il ne l'atteint qu'a travers
citations_courriel / citations_pdf. Supprimer les citations desinscrit donc aussi les
pieces qui n'etaient au dossier que parce qu'une citation les invoquait, et le rebuild
renumerote tout ce qui reste : « P-1, P-1-1, P-2, P-3 » devient « P-1, P-2, P-3 ».
La cotation GELEE du 24 juillet 2026 n'est pas concernee : elle vit dans
BordereauDepotJuillet, qui ne se recalcule jamais et ne pointe sur aucune citation.

--noeuds decide du sort des LibraryNode :

    garder     (defaut) les noeuds restent, a pointer dans le vide. C'est ce qui rend
               `relink_quotes.py` possible : ce script repointe les object_id des
               noeuds EXISTANTS. Les supprimer ferme cette porte definitivement.
    supprimer  les noeuds partent avec les citations. Les documents PRODUCED perdent
               ces paragraphes, et le carnet de rappel ne pourra plus les retablir.

LE PIEGE SILENCIEUX : `case_manager/signals.py` ecoute m2m_changed sur les tables de
liaison. Une suppression EN CASCADE n'emet pas m2m_changed. refresh_case_exhibits ne
part donc jamais tout seul et les tables d'exhibits restent perimees sans la moindre
erreur. D'ou --refresh, ou les etapes suivantes affichees en fin d'execution.

--apply s'execute dans une transaction unique : en cas d'erreur, rien n'est ecrit.
L'operation est reversible par `backup_avant_purge.py --restore`.
"""
import argparse
import json
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
EXPORT_PATH = Path(__file__).resolve().parent / "quote_links_export.json"
BACKUP_DIR = BASE_DIR / "backup_avant_purge_quotes"
sys.path.insert(0, str(BASE_DIR))
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django  # noqa: E402
django.setup()

from django.apps import apps  # noqa: E402
from django.contrib.contenttypes.models import ContentType  # noqa: E402
from django.db import transaction  # noqa: E402
from django.db.models import Q  # noqa: E402

from argument_manager.models import TrameNarrative  # noqa: E402
from case_manager.models import ExhibitRegistry, LegalCase, ProducedExhibit  # noqa: E402
from document_manager.models import LibraryNode  # noqa: E402
from email_manager.models import Quote as EmailQuote  # noqa: E402
from pdf_manager.models import Quote as PDFQuote  # noqa: E402

# Les porteurs de cle generique que ce script sait traiter. Tout autre modele qui
# pointerait sur une citation bloque --apply : mieux vaut s'arreter que stranded.
PORTEURS_CONNUS = {"document_manager.LibraryNode", "case_manager.ProducedExhibit"}

ap = argparse.ArgumentParser(description=__doc__,
                             formatter_class=argparse.RawDescriptionHelpFormatter)
g = ap.add_mutually_exclusive_group(required=True)
g.add_argument("--dry-run", action="store_true", help="rapport seul, aucune ecriture")
g.add_argument("--apply", action="store_true", help="ecrit en base (transaction unique)")
ap.add_argument("--email", metavar="PK[,PK...]", default=None,
                help="ne vise que ces email_manager.Quote (defaut : toutes)")
ap.add_argument("--pdf", metavar="PK[,PK...]", default=None,
                help="ne vise que ces pdf_manager.Quote (defaut : toutes)")
ap.add_argument("--fichier", metavar="CHEMIN", default=None,
                help="lit la selection dans un fichier, une entree « email:12 » ou "
                     "« pdf:7 » par ligne (# = commentaire)")
ap.add_argument("--noeuds", choices=["garder", "supprimer"], default="garder",
                help="sort des LibraryNode qui pointent sur une citation (defaut: garder)")
ap.add_argument("--exhibits", choices=["supprimer", "garder"], default="supprimer",
                help="sort des ProducedExhibit devenus caducs (defaut: supprimer)")
ap.add_argument("--refresh", action="store_true",
                help="enchaine refresh_case_exhibits + rebuild_produced_exhibits apres le commit")
ap.add_argument("--ignorer-carnet", action="store_true",
                help="passe outre un quote_links_export.json absent ou perime")
ap.add_argument("--ignorer-inconnus", action="store_true",
                help="passe outre un porteur de cle generique non reconnu")
ap.add_argument("--forcer-non-reconstructibles", action="store_true",
                help="touche aussi les ProducedExhibit des dossiers qu'aucun rebuild ne "
                     "regenere (perte definitive)")
ap.add_argument("--oui", action="store_true", help="pas de confirmation")
args = ap.parse_args()

EQ_CT = ContentType.objects.get_for_model(EmailQuote)
PQ_CT = ContentType.objects.get_for_model(PDFQuote)
CT_IDS = [EQ_CT.id, PQ_CT.id]


def lire_pks(brut, quoi):
    if not brut:
        return set()
    try:
        return {int(x) for x in brut.replace(",", " ").split()}
    except ValueError:
        sys.exit(f"--{quoi} : liste de PK entiers attendue, recu {brut!r}")


def lire_fichier(chemin):
    """« email:12 » / « pdf:7 » par ligne. Le prefixe est obligatoire : les PK des
    deux modeles se recouvrent, une liste nue serait ambigue."""
    sel = {"email": set(), "pdf": set()}
    p = Path(chemin)
    if not p.exists():
        sys.exit(f"--fichier : introuvable — {chemin}")
    for num, ligne in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        ligne = ligne.split("#", 1)[0].strip()
        if not ligne:
            continue
        if ":" not in ligne:
            sys.exit(f"--fichier ligne {num} : prefixe « email: » ou « pdf: » attendu — {ligne!r}")
        kind, _, pk = ligne.partition(":")
        kind = kind.strip().lower()
        if kind not in sel:
            sys.exit(f"--fichier ligne {num} : prefixe inconnu {kind!r}")
        try:
            sel[kind].add(int(pk.strip()))
        except ValueError:
            sys.exit(f"--fichier ligne {num} : PK entier attendu — {pk!r}")
    return sel


SEL_E = lire_pks(args.email, "email")
SEL_P = lire_pks(args.pdf, "pdf")
if args.fichier:
    du_fichier = lire_fichier(args.fichier)
    SEL_E |= du_fichier["email"]
    SEL_P |= du_fichier["pdf"]

# Purge TOTALE si aucune selection : c'est le mode historique du script.
TOTAL = not (SEL_E or SEL_P)

qs_e = EmailQuote.objects.all() if TOTAL else EmailQuote.objects.filter(pk__in=SEL_E)
qs_p = PDFQuote.objects.all() if TOTAL else PDFQuote.objects.filter(pk__in=SEL_P)

if not TOTAL:
    # Une PK demandee qui n'existe pas est une erreur de saisie, pas un no-op.
    absentes_e = SEL_E - set(qs_e.values_list("pk", flat=True))
    absentes_p = SEL_P - set(qs_p.values_list("pk", flat=True))
    if absentes_e or absentes_p:
        sys.exit(f"Citations introuvables — email {sorted(absentes_e)} pdf {sorted(absentes_p)}\n"
                 f"Aucune ecriture. Verifie la selection.")

n_quotes_e = qs_e.count()
n_quotes_p = qs_p.count()
PK_E = set(qs_e.values_list("pk", flat=True))
PK_P = set(qs_p.values_list("pk", flat=True))


def q_visees():
    """Q() visant les lignes generiques qui pointent sur les citations SELECTIONNEES.

    Le content_type doit accompagner chaque liste de PK : les PK de email_manager.Quote
    et de pdf_manager.Quote se recouvrent, filtrer sur object_id seul emporterait des
    lignes etrangeres a la selection.
    """
    q = Q(pk__in=[])
    if PK_E:
        q |= Q(content_type_id=EQ_CT.id, object_id__in=PK_E)
    if PK_P:
        q |= Q(content_type_id=PQ_CT.id, object_id__in=PK_P)
    return q


def scan_cles_generiques():
    """Tout modele portant (content_type, object_id) et pointant sur une citation.

    Balayage dynamique plutot que liste en dur : c'est la seule facon de remarquer
    qu'un modele ajoute depuis la derniere purge pointe lui aussi sur les citations.
    """
    trouves = []
    for model in apps.get_models():
        noms = {f.name for f in model._meta.get_fields()}
        if not {"content_type", "object_id"} <= noms:
            continue
        try:
            n_e = model.objects.filter(content_type=EQ_CT, object_id__in=PK_E).count()
            n_p = model.objects.filter(content_type=PQ_CT, object_id__in=PK_P).count()
        except Exception as exc:                       # champ homonyme, pas une cle generique
            print(f"  [scan] {model._meta.label} ignore : {exc}")
            continue
        if n_e or n_p:
            trouves.append((model._meta.label, n_e, n_p))
    return sorted(trouves)


def cases_non_reconstructibles():
    """Dossiers dont la table ProducedExhibit n'est PAS regenerable.

    rebuild_produced_exhibits() vide la table puis la repeuple depuis
    ExhibitRegistry, lequel se remplit depuis les trames de contestation. Un
    dossier qui porte des ProducedExhibit avec un ExhibitRegistry VIDE n'a donc
    aucune source de reconstruction : ces lignes n'existent que la, et le
    prochain rebuild les met a zero. Les toucher est une perte definitive, ce
    qui les separe des lignes reellement derivees.

    Retourne [(case_id, lignes_totales, lignes_pointant_sur_une_citation)].
    """
    out = []
    for case_id in LegalCase.objects.values_list("pk", flat=True):
        n_prod = ProducedExhibit.objects.filter(case_id=case_id).count()
        if n_prod and not ExhibitRegistry.objects.filter(case_id=case_id).exists():
            n_cit = ProducedExhibit.objects.filter(q_visees(), case_id=case_id).count()
            out.append((case_id, n_prod, n_cit))
    return out


def impact_sur_les_parents():
    """Pour chaque piece parente touchee : combien de citations partent, combien restent.

    C'est la question qui decide de l'inscription au registre. refresh_case_exhibits
    n'inscrit pas les citations, il inscrit leur PARENT, et il ne l'atteint qu'a travers
    citations_courriel / citations_pdf. Une piece reste donc inscrite tant qu'il lui
    reste UNE citation adossee a une trame ; elle sort du registre quand la derniere
    part. Aucun comptage a ecrire : refresh recalcule l'ensemble et l'union le dit.

    Retourne [(libelle, partantes, restantes, restantes_en_trame)].
    """
    lignes = []
    for kind, qs, champ, modele in (("email", qs_e, "email_id", EmailQuote),
                                    ("pdf", qs_p, "pdf_document_id", PDFQuote)):
        parents = sorted({v for v in qs.values_list(champ, flat=True) if v})
        for parent_id in parents:
            partantes = qs.filter(**{champ: parent_id}).count()
            reste = modele.objects.filter(**{champ: parent_id}).exclude(
                pk__in=(PK_E if kind == "email" else PK_P))
            # Seule une citation reliee a une trame maintient l'inscription.
            en_trame = reste.filter(trames_narratives__isnull=False).distinct().count()
            lignes.append((f"{kind}:{parent_id}", partantes, reste.count(), en_trame))
    return lignes


# --- Etat des lieux -------------------------------------------------------------------

porteurs = scan_cles_generiques()
inconnus = [p for p in porteurs if p[0] not in PORTEURS_CONNUS]
fragiles = cases_non_reconstructibles()
CASES_FRAGILES = [c for c, _, _ in fragiles]

noeuds = list(LibraryNode.objects.filter(q_visees()).select_related("document"))
noeuds_avec_enfants = [n for n in noeuds if n.get_children_count()]

n_exhibits = ProducedExhibit.objects.filter(q_visees()).count()

n_m2m_e = TrameNarrative.citations_courriel.through.objects.filter(quote_id__in=PK_E).count()
n_m2m_p = TrameNarrative.citations_pdf.through.objects.filter(quote_id__in=PK_P).count()
n_trames = (TrameNarrative.objects
            .filter(Q(citations_courriel__in=PK_E) | Q(citations_pdf__in=PK_P))
            .distinct().count())

titre = ("PURGE TOTALE DES CITATIONS" if TOTAL
         else f"SUPPRESSION CIBLEE — {n_quotes_e + n_quotes_p} CITATION(S)")
print("=" * 78)
print(titre + ("  [DRY-RUN]" if args.dry_run else "  [APPLY]"))
print("=" * 78)
print()
print("A SUPPRIMER — les citations elles-memes")
print(f"  email_manager.Quote                       {n_quotes_e:>6}")
print(f"  pdf_manager.Quote                         {n_quotes_p:>6}")
print(f"  {'TOTAL':<40} {n_quotes_e + n_quotes_p:>6}")
print()
print("EN CASCADE — vraies cles etrangeres, Django s'en charge")
print(f"  liaison TrameNarrative.citations_courriel {n_m2m_e:>6}")
print(f"  liaison TrameNarrative.citations_pdf      {n_m2m_p:>6}")
print(f"  trames narratives touchees                {n_trames:>6}  (les trames survivent, leurs citations non)")
if not TOTAL:
    impacts = impact_sur_les_parents()
    perdent = [x for x in impacts if x[3] == 0]
    gardent = [x for x in impacts if x[3] > 0]
    print()
    print("PIECES PARENTES — qui reste inscrite au registre, qui en sort")
    print(f"  {len(impacts)} piece(s) touchee(s) : {len(gardent)} conserve(nt) leur inscription, "
          f"{len(perdent)} la perde(nt)")
    for libelle, partantes, restantes, en_trame in impacts:
        if en_trame:
            verdict = f"RESTE inscrite ({en_trame} citation(s) en trame subsistent)"
        elif restantes:
            verdict = f"SORT du registre ({restantes} citation(s) restent, aucune en trame)"
        else:
            verdict = "SORT du registre (derniere citation)"
        print(f"    {libelle:<14} -{partantes:<3} {verdict}")
    print("  Rien a coder : refresh_case_exhibits recalcule l'ensemble et l'union tranche.")

print()
print("CLES GENERIQUES — aucune cascade, a traiter a la main")
if not porteurs:
    print("  aucun porteur ne pointe sur une citation")
for label, n_e, n_p in porteurs:
    marque = "" if label in PORTEURS_CONNUS else "   <-- INCONNU"
    print(f"  {label:<40} {n_e + n_p:>6}  (email {n_e} / pdf {n_p}){marque}")

if noeuds:
    print()
    print(f"  LibraryNode — sort choisi : --noeuds {args.noeuds}")
    par_doc = {}
    for n in noeuds:
        cle = (n.document_id, n.document.title, n.document.source_type)
        par_doc[cle] = par_doc.get(cle, 0) + 1
    for (doc_id, titre, source), n in sorted(par_doc.items()):
        total = LibraryNode.objects.filter(document_id=doc_id).count()
        print(f"    doc {doc_id:<3} {source:<10} {n:>4}/{total} noeuds   {titre[:44]}")
    if noeuds_avec_enfants:
        print(f"    ATTENTION : {len(noeuds_avec_enfants)} noeud(s) ont des descendants ;")
        print( "    une suppression treebeard emporte le sous-arbre entier :")
        for n in noeuds_avec_enfants[:10]:
            print(f"      node {n.pk} (depth {n.depth}) — {n.get_children_count()} enfant(s) — {n.item[:40]!r}")
    else:
        print("    tous ces noeuds sont des feuilles : aucun sous-arbre emporte.")
    if args.noeuds == "garder":
        print("    -> conserves, a pointer dans le vide ; `relink_quotes.py` pourra les repointer.")
    else:
        print("    -> SUPPRIMES : ces paragraphes quittent les documents, sans retour par le carnet.")

if n_exhibits:
    print()
    print(f"  ProducedExhibit — sort choisi : --exhibits {args.exhibits}")
    n_frag_cit = sum(n_cit for _, _, n_cit in fragiles)
    print(f"    {n_exhibits - n_frag_cit} ligne(s) reellement derivee(s) ; "
          f"rebuild_produced_exhibits() les recalcule de toute facon.")
    if fragiles:
        print()
        print("    DOSSIERS NON RECONSTRUCTIBLES — ProducedExhibit rempli, ExhibitRegistry VIDE :")
        for case_id, n_prod, n_cit in fragiles:
            print(f"      case {case_id} : {n_prod} ligne(s), dont {n_cit} sur une citation")
        print("      Aucune trame ne les adosse : rebuild_produced_exhibits() les mettrait a ZERO.")
        print("      Ces lignes n'existent que la — les supprimer est definitif.")
        if args.forcer_non_reconstructibles:
            print("      -> --forcer-non-reconstructibles : elles seront traitees comme les autres.")
        else:
            print("      -> EPARGNEES par defaut ; --refresh saute aussi ces dossiers.")

# --- Verifications avant ecriture -----------------------------------------------------

blocages = []
avertissements = []

if inconnus and not args.ignorer_inconnus:
    blocages.append(
        "porteur(s) de cle generique non reconnu(s) : "
        + ", ".join(f"{label} ({n_e + n_p})" for label, n_e, n_p in inconnus)
        + "\n    Ces lignes pointeraient dans le vide sans que rien ne les traite."
        "\n    Traite-les, ajoute-les a PORTEURS_CONNUS, ou passe --ignorer-inconnus.")

# Le carnet est la voie de retour d'une purge TOTALE : on recree tout, puis relink_quotes
# recable. Une suppression ciblee ne repasse pas par la — sa voie de retour est la
# sauvegarde. On n'exige donc la fraicheur du carnet que sur une purge totale.
BASE_E = EmailQuote.objects.count()
BASE_P = PDFQuote.objects.count()

if not TOTAL:
    pass
elif not EXPORT_PATH.exists():
    if not args.ignorer_carnet:
        blocages.append(
            f"carnet de rappel absent : {EXPORT_PATH.relative_to(BASE_DIR)}"
            "\n    Lance export_quote_links.py AVANT la purge, ou passe --ignorer-carnet.")
else:
    meta = json.loads(EXPORT_PATH.read_text(encoding="utf-8"))["_meta"]
    carnet_e = meta.get("email_quote_count")
    carnet_p = meta.get("pdf_quote_count")
    if (carnet_e, carnet_p) != (BASE_E, BASE_P):
        msg = (f"carnet de rappel PERIME : il decrit {carnet_e} + {carnet_p} citations, "
               f"la base en compte {BASE_E} + {BASE_P}."
               "\n    Relance export_quote_links.py, ou passe --ignorer-carnet.")
        (avertissements if args.ignorer_carnet else blocages).append(msg)
    else:
        print()
        print(f"  carnet de rappel a jour : {EXPORT_PATH.relative_to(BASE_DIR)} "
              f"({carnet_e} + {carnet_p} citations)")

sauvegardes = sorted((d for d in BACKUP_DIR.glob("*") if d.is_dir()), key=lambda d: d.name)
if not sauvegardes:
    avertissements.append(
        f"aucune sauvegarde sous {BACKUP_DIR.relative_to(BASE_DIR)}/ — "
        "lance backup_avant_purge.py avant --apply.")
else:
    print(f"  derniere sauvegarde     : {sauvegardes[-1].relative_to(BASE_DIR)}")

if avertissements:
    print()
    print("AVERTISSEMENTS")
    for a in avertissements:
        print(f"  ! {a}")

if blocages:
    print()
    print("=" * 78)
    print("BLOCAGE — rien n'a ete ecrit")
    print("=" * 78)
    for b in blocages:
        print(f"  x {b}")
    sys.exit(1)

# --- Ecriture -------------------------------------------------------------------------

if args.dry_run:
    print()
    print("=" * 78)
    print("DRY-RUN : aucune ecriture. Relancer avec --apply pour executer.")
    print("=" * 78)
    sys.exit(0)

if not args.oui:
    print()
    attendu = f"{n_quotes_e + n_quotes_p}"
    print(f"Tape le nombre total de citations a supprimer ({attendu}) pour confirmer, "
          f"ou n'importe quoi d'autre pour annuler.")
    try:
        reponse = input("> ").strip()
    except EOFError:
        sys.exit("Pas de terminal interactif : relance avec --oui.")
    if reponse != attendu:
        sys.exit("Annule.")

print()
print("=" * 78)
print("ECRITURE")
print("=" * 78)

with transaction.atomic():
    if noeuds:
        if args.noeuds == "supprimer":
            # Les feuilles d'abord, pour qu'une suppression treebeard n'emporte pas
            # un noeud deja traite par son ancetre.
            for n in sorted(noeuds, key=lambda n: -n.depth):
                LibraryNode.objects.filter(pk=n.pk).delete()
            print(f"  LibraryNode supprimes                     {len(noeuds):>6}")
        else:
            print(f"  LibraryNode conserves (pointent dans le vide) {len(noeuds):>2}"
                  f" -> relink_quotes.py")

    if n_exhibits and args.exhibits == "supprimer":
        qs = ProducedExhibit.objects.filter(q_visees())
        if CASES_FRAGILES and not args.forcer_non_reconstructibles:
            qs = qs.exclude(case_id__in=CASES_FRAGILES)
        n, _ = qs.delete()
        print(f"  ProducedExhibit supprimes                 {n:>6}")
        epargnees = ProducedExhibit.objects.filter(q_visees()).count()
        if epargnees:
            print(f"  ProducedExhibit epargnes (non reconstructibles) {epargnees:>2}"
                  f"  cases {CASES_FRAGILES}")

    total_e, detail_e = qs_e.delete()
    total_p, detail_p = qs_p.delete()
    print(f"  email_manager.Quote supprimees            {detail_e.get('email_manager.Quote', 0):>6}")
    print(f"  pdf_manager.Quote supprimees              {detail_p.get('pdf_manager.Quote', 0):>6}")
    for label, n in sorted({**detail_e, **detail_p}.items()):
        if label not in ("email_manager.Quote", "pdf_manager.Quote"):
            print(f"    en cascade : {label:<38} {n:>6}")

print()
print(f"  restant en base : {EmailQuote.objects.count()} citation(s) courriel, "
      f"{PDFQuote.objects.count()} citation(s) pdf")

# --- Reconstruction des tables derivees -----------------------------------------------
# Hors transaction : refresh_case_exhibits / rebuild_produced_exhibits ouvrent la leur.

if args.refresh:
    from case_manager.exhibit_service import refresh_case_exhibits, rebuild_produced_exhibits
    print()
    print("RECONSTRUCTION")
    for case_id in LegalCase.objects.values_list("pk", flat=True):
        if case_id in CASES_FRAGILES and not args.forcer_non_reconstructibles:
            print(f"  case {case_id} : SAUTE — un rebuild y remettrait la table a zero")
            continue
        refresh_case_exhibits(case_id)
        rebuild_produced_exhibits(case_id)
        print(f"  case {case_id} : exhibits recalcules")

print()
print("Etapes suivantes :")
if not args.refresh:
    print("  refresh_case_exhibits + rebuild_produced_exhibits pour chaque LegalCase")
    print("    (la cascade n'emet PAS m2m_changed : le signal ne l'a pas fait pour toi)")
print("  .venv/bin/python docs/purge_quotes/audit_quotes.py           # temoin apres purge")
if args.noeuds == "garder" and TOTAL:
    print("  .venv/bin/python docs/purge_quotes/relink_quotes.py --dry-run")
    print("    une fois les citations recreees, pour repointer trames et noeuds")
elif args.noeuds == "garder" and noeuds:
    print(f"  {len(noeuds)} LibraryNode pointent desormais dans le vide : les repointer a la")
    print("    main, ou relancer avec --noeuds supprimer sur cette meme selection.")
print(f"  restauration : .venv/bin/python docs/purge_quotes/backup_avant_purge.py --restore "
      f"--dir {sauvegardes[-1].relative_to(BASE_DIR) if sauvegardes else '<repertoire>'}")
