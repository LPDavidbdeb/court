"""
Transcrit les pièces du bordereau — et seulement elles.

    python manage.py transcrire_pieces_bordereau                  # constat
    python manage.py transcrire_pieces_bordereau --ecrire
    python manage.py transcrire_pieces_bordereau --ecrire --phase extraction

PÉRIMÈTRE STRICT. Seuls les `PDFDocument` et `PhotoDocument` inscrits au
registre des pièces sont traités. La base en contient bien davantage — des
documents de référence, parfois très volumineux, qui n'entrent pas au bordereau
et n'ont aucune raison d'être transcrits. Le périmètre se lit dans la table, il
ne se saisit pas.

DEUX VOIES, ET LA PREMIÈRE EST DE LOIN LA MEILLEURE.

  EXTRACTION   35 des 44 PDF portent une couche texte. C'est le texte que le
               producteur du document a écrit. Le copier est exact, gratuit et
               instantané. Le faire relire par un modèle de vision n'ajouterait
               qu'un risque d'erreur là où il n'y en a aucun.
  OCR          9 PDF sont des images (jugements numérisés, permis, certificat).
               Là seulement, un modèle de vision est nécessaire — et c'est là
               que la directive de fiabilité travaille.

Les `PhotoDocument` n'ont par nature aucune couche texte : ils passent tous par
la seconde voie.

CE QUI EST ÉCRIT LE DIT. Chaque transcription commence par un en-tête qui nomme
sa méthode, son étendue et sa date. Une extraction exacte et une lecture par
OCR n'ont pas la même valeur probante, et rien ne doit obliger un lecteur à
deviner laquelle il a sous les yeux.

RIEN N'EST PERDU. Le contenu existant de `ai_analysis` est sauvegardé dans un
fichier JSON horodaté avant toute écriture.
"""
import json
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from ai_services.services import extraire_texte_pdf, transcrire_document
from case_manager.models import BordereauDepotJuillet
from pdf_manager.models import PDFDocument
from photos.models import PhotoDocument

# En deçà de ce nombre de caractères par page, la couche texte n'est pas
# exploitable : le PDF est un scan. Le seuil est bas — une page de facture
# n'en porte que 400 — mais un scan en porte zéro, l'écart n'est jamais serré.
SEUIL_COUCHE_TEXTE = 120


def pieces_du_bordereau(modele):
    ct = ContentType.objects.get_for_model(modele)
    ids = {e.object_id for e in BordereauDepotJuillet.objects.filter(content_type=ct)
           if e.object_id}
    return modele.objects.filter(pk__in=ids).order_by('pk')


def diagnostiquer_pdf(doc):
    """`(pages, caracteres_par_page, voie)` — 'extraction' ou 'ocr'."""
    import fitz
    f = fitz.open(doc.file.path)
    pages = len(f)
    texte = "".join(p.get_text() for p in f)
    f.close()
    cpp = len(texte) / max(pages, 1)
    return pages, cpp, ('extraction' if cpp > SEUIL_COUCHE_TEXTE else 'ocr')


def entete(methode, etendue, fiabilite):
    return (f"<!-- transcription | {methode} | {etendue} | "
            f"{datetime.now():%Y-%m-%d %H:%M} | fiabilité : {fiabilite} -->")


class Command(BaseCommand):
    help = "Transcrit les PDF et PhotoDocuments inscrits au bordereau des pièces."

    def add_arguments(self, parser):
        parser.add_argument("--ecrire", action="store_true",
                            help="écrire en base ; sans ce drapeau, simple constat")
        parser.add_argument("--phase", choices=['extraction', 'ocr', 'photos', 'tout'],
                            default='tout')
        parser.add_argument("--pk", type=int, default=None,
                            help="ne traiter qu'une pièce, par son pk (PDF)")
        parser.add_argument("--dpi", type=int, default=200,
                            help="résolution de rendu des pages pour l'OCR")

    def handle(self, *args, **options):
        ecrire = options["ecrire"]
        phase = options["phase"]
        w = self.stdout.write

        pdfs = list(pieces_du_bordereau(PDFDocument))
        photos = list(pieces_du_bordereau(PhotoDocument))
        if options["pk"]:
            pdfs = [d for d in pdfs if d.pk == options["pk"]]
            photos = []

        # --- tri des PDF par voie ---
        plan = []
        for d in pdfs:
            pages, cpp, voie = diagnostiquer_pdf(d)
            plan.append((d, pages, cpp, voie))

        extraction = [x for x in plan if x[3] == 'extraction']
        ocr = [x for x in plan if x[3] == 'ocr']

        w("=" * 76)
        w("TRANSCRIPTION DES PIÈCES DU BORDEREAU")
        w("=" * 76)
        w(f"  PDF au bordereau        : {len(plan)}  ({sum(p for _d, p, _c, _v in plan)} pages)")
        w(f"    par extraction exacte : {len(extraction)}  "
          f"({sum(p for _d, p, _c, _v in extraction)} pages) — aucune IA")
        w(f"    par OCR (image seule) : {len(ocr)}  "
          f"({sum(p for _d, p, _c, _v in ocr)} pages)")
        w(f"  PhotoDocuments          : {len(photos)}  "
          f"({sum(d.photos.count() for d in photos)} photos)")
        w(f"  appels au modèle        : {len(ocr) + len(photos)}")

        if not ecrire:
            w("")
            w("  PAR OCR :")
            for d, pages, _c, _v in ocr:
                w(f"    pdf {d.pk:<4} {pages:>3} p.  {d.title[:52]}")
            w("")
            w("  PHOTOS :")
            for d in photos:
                w(f"    doc {d.pk:<4} {d.photos.count():>3} img. {d.title[:52]}")
            w("")
            w(self.style.WARNING("  CONSTAT SEULEMENT — rien n'a été écrit. "
                                 "Relancer avec --ecrire."))
            return

        # --- sauvegarde ---
        sauvegarde = {"genere_le": datetime.now().isoformat(), "pdf": {}, "photodoc": {}}
        for d, _p, _c, _v in plan:
            sauvegarde["pdf"][str(d.pk)] = d.ai_analysis or ""
        for d in photos:
            sauvegarde["photodoc"][str(d.pk)] = d.ai_analysis or ""
        chemin = (Path(settings.BASE_DIR) /
                  f"backup_ai_analysis_{datetime.now():%Y-%m-%d_%H%M}.json")
        chemin.write_text(json.dumps(sauvegarde, ensure_ascii=False, indent=2))
        w("")
        w(f"  Sauvegarde des transcriptions existantes : {chemin.name}")

        faits = erreurs = 0

        # --- voie 1 : extraction ---
        if phase in ('extraction', 'tout'):
            w("")
            w("  EXTRACTION")
            for d, pages, _cpp, _v in extraction:
                texte = extraire_texte_pdf(d.file.path)
                d.ai_analysis = (entete("extraction directe de la couche texte",
                                        f"{pages} page(s), intégral", "exacte")
                                 + "\n\n" + texte)
                d.save(update_fields=['ai_analysis'])
                faits += 1
                w(f"    pdf {d.pk:<4} {pages:>3} p.  {len(texte):>7} car.  {d.title[:40]}")

        # --- voie 2 : OCR ---
        if phase in ('ocr', 'tout'):
            w("")
            w("  OCR — modèle de vision, directive de fiabilité")
            for d, pages, _cpp, _v in ocr:
                texte, unites, err = transcrire_document(d, dpi=options["dpi"])
                if err:
                    erreurs += 1
                    w(self.style.ERROR(f"    pdf {d.pk:<4} ÉCHEC — {err[:60]}"))
                    continue
                d.ai_analysis = (entete("OCR par modèle de vision (gemini-2.5-flash)",
                                        f"{unites} page(s), intégral",
                                        "à vérifier — voir les réserves en fin de texte")
                                 + "\n\n" + texte)
                d.save(update_fields=['ai_analysis'])
                faits += 1
                reserve = "Aucune." not in texte[-400:]
                w(f"    pdf {d.pk:<4} {unites:>3} p.  {len(texte):>7} car.  "
                  f"{'⚠ réserves' if reserve else 'sans réserve'}  {d.title[:32]}")

        # --- voie 3 : photos ---
        if phase in ('photos', 'tout'):
            w("")
            w("  PHOTOS — constat visuel, directive de fiabilité")
            for d in photos:
                texte, unites, err = transcrire_document(d)
                if err:
                    erreurs += 1
                    w(self.style.ERROR(f"    doc {d.pk:<4} ÉCHEC — {err[:60]}"))
                    continue
                d.ai_analysis = (entete("constat visuel par modèle de vision (gemini-2.5-flash)",
                                        f"{unites} image(s), intégral",
                                        "à vérifier — voir les réserves en fin de texte")
                                 + "\n\n" + texte)
                d.save(update_fields=['ai_analysis'])
                faits += 1
                reserve = "Aucune." not in texte[-400:]
                w(f"    doc {d.pk:<4} {unites:>3} img. {len(texte):>7} car.  "
                  f"{'⚠ réserves' if reserve else 'sans réserve'}  {d.title[:32]}")

        w("")
        w(self.style.SUCCESS(f"  {faits} pièce(s) transcrite(s)")
          if not erreurs else
          self.style.WARNING(f"  {faits} transcrite(s), {erreurs} en échec"))
