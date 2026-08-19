"""
Sortir les pièces pour relecture, puis réintégrer les transcriptions corrigées.

    python manage.py transcription_manuelle --exporter <dossier>
    python manage.py transcription_manuelle --importer <dossier>
    python manage.py transcription_manuelle --importer <dossier> --ecrire

POURQUOI CETTE COMMANDE PLUTÔT QU'UN APPEL AU SERVICE D'IA.
`ai_services.analyze_document_content` envoie la pièce à un modèle distant, avec
deux plafonds silencieux (dix pages, dix photos) et sans garantie sur ce qui
revient. Le contenu accumulé dans `ai_analysis` provient de directives qui ont
varié dans le temps : rien n'y distingue une transcription fidèle d'un résumé,
et rien ne dit laquelle on lit.

Ici la lecture est faite par un relecteur qui a le document sous les yeux, et la
commande ne fait que le service de transport :

  --exporter   dépose, pour chaque pièce du bordereau, le chemin du fichier
               d'origine et le contenu ACTUEL de `ai_analysis`. Rien n'est
               modifié.
  --importer   relit le dossier, compare chaque transcription corrigée à ce que
               la base contient, et n'écrit que là où le contenu diffère.

CONVENTION DE NOMMAGE, dans le dossier d'échange :

    pdf-14.actuel.md      ce que la base contient aujourd'hui   (écrit par --exporter)
    pdf-14.nouveau.md     la transcription corrigée             (écrit par le relecteur)
    manifeste.json        pk, titre, chemin du fichier, pages, empreinte

Une pièce sans fichier `.nouveau.md` est simplement ignorée : on peut donc
traiter le lot en plusieurs fois sans rien perdre.

PÉRIMÈTRE. Seules les pièces inscrites au bordereau. La base contient des
documents de référence volumineux qui n'y figurent pas et n'ont pas à être
transcrits.
"""
import hashlib
import json
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError

from case_manager.models import BordereauDepotJuillet
from pdf_manager.models import PDFDocument
from photos.models import PhotoDocument


def pieces_du_bordereau(modele):
    ct = ContentType.objects.get_for_model(modele)
    ids = {e.object_id for e in BordereauDepotJuillet.objects.filter(content_type=ct)
           if e.object_id}
    return modele.objects.filter(pk__in=ids).order_by('pk')


def empreinte(texte):
    return hashlib.sha256((texte or "").encode()).hexdigest()[:16]


def entete(methode, etendue, fiabilite):
    return (f"<!-- transcription | {methode} | {etendue} | "
            f"{datetime.now():%Y-%m-%d %H:%M} | fiabilité : {fiabilite} -->")


class Command(BaseCommand):
    help = "Exporte les pièces pour relecture humaine, réimporte les transcriptions."

    def add_arguments(self, parser):
        parser.add_argument("--exporter", metavar="DOSSIER", default=None)
        parser.add_argument("--importer", metavar="DOSSIER", default=None)
        parser.add_argument("--ecrire", action="store_true",
                            help="à l'import : écrire en base")
        parser.add_argument("--type", choices=['pdf', 'photodoc', 'tout'], default='tout')

    def handle(self, *args, **options):
        if bool(options["exporter"]) == bool(options["importer"]):
            raise CommandError("Choisir --exporter OU --importer.")
        if options["exporter"]:
            self.exporter(Path(options["exporter"]), options["type"])
        else:
            self.importer(Path(options["importer"]), options["ecrire"])

    # ------------------------------------------------------------------
    def exporter(self, dossier, typ):
        dossier.mkdir(parents=True, exist_ok=True)
        w = self.stdout.write
        manifeste = []

        if typ in ('pdf', 'tout'):
            import fitz
            for d in pieces_du_bordereau(PDFDocument):
                chemin = d.file.path if d.file else None
                pages = couche = None
                if chemin and Path(chemin).exists():
                    f = fitz.open(chemin)
                    pages = len(f)
                    couche = len("".join(p.get_text() for p in f)) / max(pages, 1)
                    f.close()
                actuel = d.ai_analysis or ""
                (dossier / f"pdf-{d.pk}.actuel.md").write_text(actuel)
                manifeste.append({
                    "type": "pdf", "pk": d.pk, "titre": d.title,
                    "fichier": chemin, "pages": pages,
                    "caracteres_par_page": round(couche) if couche is not None else None,
                    "voie": ("extraction" if (couche or 0) > 120 else "lecture requise"),
                    "actuel_caracteres": len(actuel),
                    "actuel_empreinte": empreinte(actuel),
                })

        if typ in ('photodoc', 'tout'):
            for d in pieces_du_bordereau(PhotoDocument):
                actuel = d.ai_analysis or ""
                (dossier / f"photodoc-{d.pk}.actuel.md").write_text(actuel)
                manifeste.append({
                    "type": "photodoc", "pk": d.pk, "titre": d.title,
                    "fichiers": [p.file.path for p in d.photos.all() if p.file],
                    "actuel_caracteres": len(actuel),
                    "actuel_empreinte": empreinte(actuel),
                })

        (dossier / "manifeste.json").write_text(
            json.dumps(manifeste, ensure_ascii=False, indent=2))

        w("=" * 76)
        w(f"EXPORT POUR RELECTURE → {dossier}")
        w("=" * 76)
        w(f"  pièces exportées : {len(manifeste)}")
        for m in manifeste:
            if m["type"] == "pdf":
                w(f"    pdf-{m['pk']:<5} {str(m['pages'] or '?'):>3} p.  "
                  f"{m['voie']:<16} actuel : {m['actuel_caracteres']:>6} car.  {m['titre'][:34]}")
            else:
                w(f"    photodoc-{m['pk']:<2} {len(m['fichiers']):>3} img. "
                  f"{'lecture requise':<16} actuel : {m['actuel_caracteres']:>6} car.  {m['titre'][:34]}")
        w("")
        w("  Déposer chaque transcription corrigée en « <type>-<pk>.nouveau.md »,")
        w("  puis relancer avec --importer.")

    # ------------------------------------------------------------------
    def importer(self, dossier, ecrire):
        w = self.stdout.write
        if not dossier.exists():
            raise CommandError(f"Dossier introuvable : {dossier}")

        modeles = {"pdf": PDFDocument, "photodoc": PhotoDocument}
        candidats = sorted(dossier.glob("*.nouveau.md"))

        w("=" * 76)
        w(f"IMPORT DES TRANSCRIPTIONS ← {dossier}")
        w("=" * 76)
        w(f"  fichiers .nouveau.md trouvés : {len(candidats)}")

        if not candidats:
            return

        sauvegarde, changements, inchanges = {}, [], 0
        for f in candidats:
            typ, reste = f.name.split("-", 1)
            pk = int(reste.split(".", 1)[0])
            modele = modeles.get(typ)
            if modele is None:
                w(self.style.ERROR(f"    {f.name} — type inconnu, ignoré"))
                continue
            obj = modele.objects.filter(pk=pk).first()
            if obj is None:
                w(self.style.ERROR(f"    {f.name} — pk absent de la base, ignoré"))
                continue

            nouveau = f.read_text().strip()
            actuel = (obj.ai_analysis or "").strip()
            if empreinte(nouveau) == empreinte(actuel):
                inchanges += 1
                continue

            sauvegarde[f"{typ}-{pk}"] = actuel
            changements.append((typ, pk, obj, actuel, nouveau))

        w(f"  identiques à la base, ignorés : {inchanges}")
        w(f"  à mettre à jour               : {len(changements)}")
        w("")
        for typ, pk, obj, actuel, nouveau in changements:
            titre = getattr(obj, 'title', '')[:34]
            w(f"    {typ}-{pk:<5} {len(actuel):>6} → {len(nouveau):>6} car.  {titre}")

        if not ecrire:
            w("")
            w(self.style.WARNING("  CONSTAT SEULEMENT — rien n'a été écrit. "
                                 "Relancer avec --ecrire."))
            return

        chemin = (Path(settings.BASE_DIR) /
                  f"backup_ai_analysis_{datetime.now():%Y-%m-%d_%H%M}.json")
        chemin.write_text(json.dumps(sauvegarde, ensure_ascii=False, indent=2))
        for typ, pk, obj, _actuel, nouveau in changements:
            obj.ai_analysis = nouveau
            obj.save(update_fields=['ai_analysis'])
        w("")
        w(f"  Sauvegarde du contenu remplacé : {chemin.name}")
        w(self.style.SUCCESS(f"  {len(changements)} transcription(s) mise(s) à jour."))
