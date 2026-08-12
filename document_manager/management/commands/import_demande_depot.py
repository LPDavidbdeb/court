"""
Construit, dans document_manager, l'arbre de la demande déposée le 24 juillet 2026.

    python manage.py import_demande_depot                 # rapport seul
    python manage.py import_demande_depot --apply

Lit `legal/demande_DEPOT_2026-07-21.md` en LECTURE SEULE. N'écrit jamais dans
les fichiers .md.

PRINCIPE — la profondeur porte le rôle, donc rien d'autre ne le porte.

    profondeur 1   racine du document
    profondeur 2   § I, § II, …            (titres de section)
    profondeur 3   A., B., C.              (sous-sections)
    profondeur 4   thèmes
    profondeur 5   sous-thèmes
    profondeur 6   PARAGRAPHES             (toujours, sans exception)

Le document réel n'est pas régulier : un paragraphe peut être rattaché à une
section, à une sous-section ou à un thème. Plutôt que d'assouplir la règle, on
régularise l'arbre par des NŒUDS TRANSPARENTS — des LibraryNode sans
content_object, qui n'existent que pour porter des enfants et occuper un niveau.

    convention : content_type IS NULL  <=>  nœud transparent
    invariant  : un nœud transparent n'est jamais une feuille

Le rendu les saute ; la profondeur les compte. Chaque paragraphe se retrouve
ainsi à la profondeur 6, et son rôle se déduit de sa position sans qu'aucun
champ n'ait à le déclarer.

RENUMÉROTATION — le document déposé porte 198 paragraphes numérotés de 1 à 241,
avec 61 numéros inutilisés et 19 paragraphes suffixés (8-A … 22-A) insérés lors
d'amendements. La numérotation continue est reconstruite par simple parcours de
l'arbre. Le numéro d'origine est conservé dans `LibraryNode.item` : sans lui, les
renvois du corpus (« §§ 14-17 », « les paragraphes 30 et 31 ») deviendraient
intraçables. La table de correspondance ancien -> nouveau est écrite sur disque.
"""
import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from document_manager.models import Document, DocumentSource, LibraryNode, Statement

SOURCE = Path(settings.BASE_DIR) / "legal" / "demande_DEPOT_2026-07-21.md"
# La correspondance ancien -> nouveau numero vit en base (LibraryNode.item),
# pas dans un fichier : rien ne sort de l application.

PROFONDEUR_PARAGRAPHE = 6

RE_TITRE = re.compile(r"^(#{1,5})\s+(.*\S)\s*$")
RE_PARAGRAPHE = re.compile(r"^(\d{1,3}(?:-[A-Z])?)\.\s+(.*)$")
RE_PUCE = re.compile(r"^[-*]\s+(.*\S)\s*$")

# La clôture de l'acte n'a pas la forme du corps : ses sections ne contiennent
# aucun paragraphe numéroté, mais des conclusions en liste et des blocs libres.
# On n'y capte du texte brut QUE dans ces sections-là : ailleurs, une ligne non
# numérotée est le plus souvent la suite d'un paragraphe replié par le markdown,
# et la capturer produirait des doublons.
SECTIONS_DE_CLOTURE = {
    "POUR CES MOTIFS, PLAISE AU TRIBUNAL :",
    "BORDEREAU DES PIÈCES",
    "SIGNATURE",
}

IGNORER = re.compile(r"^\s*(?:-{3,}|_{3,}|\*{3,})\s*$")


def lire(chemin):
    """
    -> [(genre, niveau, libelle, texte)]
       genre = 'titre' | 'paragraphe' | 'conclusion' | 'mention'
       niveau : profondeur visée (titres) ; None sinon
    """
    if not chemin.exists():
        raise CommandError(f"Source introuvable : {chemin}")

    elements = []
    dans_bloc = False
    dans_cloture = False
    rang_conclusion = 0

    for ligne in chemin.read_text(encoding="utf-8").splitlines():
        if ligne.startswith("```"):
            dans_bloc = not dans_bloc
            continue
        if dans_bloc or IGNORER.match(ligne):
            continue

        m = RE_TITRE.match(ligne)
        if m:
            titre = m.group(2)
            dans_cloture = titre.strip() in SECTIONS_DE_CLOTURE
            elements.append(("titre", len(m.group(1)), titre, titre))
            continue

        m = RE_PARAGRAPHE.match(ligne)
        if m:
            elements.append(("paragraphe", None, m.group(1), m.group(2).strip()))
            continue

        if not dans_cloture:
            continue

        m = RE_PUCE.match(ligne)
        if m:
            rang_conclusion += 1
            elements.append(("conclusion", None, f"C-{rang_conclusion}",
                             m.group(1).strip()))
            continue

        if ligne.strip():
            elements.append(("mention", None, "", ligne.strip()))

    return elements


class Command(BaseCommand):
    help = "Construit l'arbre de la demande déposée dans document_manager."

    def add_arguments(self, parser):
        parser.add_argument("--apply", action="store_true",
                            help="écrit en base (transaction unique)")
        parser.add_argument("--titre", default="DEMANDE INTRODUCTIVE D'INSTANCE "
                                               "— dépôt du 24 juillet 2026")
        parser.add_argument("--remplacer", type=int, default=None,
                            help="pk d'un Document à remplacer intégralement")

    def handle(self, *args, **options):
        elements = lire(SOURCE)
        titres = [e for e in elements if e[0] == "titre"]
        paragraphes = [e for e in elements if e[0] == "paragraphe"]

        # ------------------------------------------------------------------
        # Plan de l'arbre : chaque paragraphe reçoit sa chaîne d'ancêtres,
        # complétée par des nœuds transparents jusqu'à la profondeur cible.
        # ------------------------------------------------------------------
        pile = {}          # niveau -> libellé du titre courant
        plan = []          # (profondeur, genre, libelle, texte)
        transparents = 0
        replaces = 0
        par_profondeur_origine = {}

        for genre, niveau, libelle, texte in elements:
            if genre == "titre":
                if niveau == 1:
                    continue                      # le titre du document = la racine
                pile[niveau] = libelle
                for k in list(pile):
                    if k > niveau:
                        del pile[k]
                plan.append((niveau, "titre", libelle, texte))
                continue

            # paragraphe, conclusion ou mention : meme traitement structurel —
            # tous descendent a la profondeur terminale, comblee au besoin. Seul
            # le genre differe, et c'est lui qui decide de la numerotation.
            origine = max(pile) if pile else 1
            if genre == "paragraphe":
                par_profondeur_origine[origine] = par_profondeur_origine.get(origine, 0) + 1
            manquants = PROFONDEUR_PARAGRAPHE - 1 - origine
            if manquants > 0:
                if genre == "paragraphe":
                    replaces += 1
                for d in range(origine + 1, PROFONDEUR_PARAGRAPHE):
                    plan.append((d, "transparent", "", ""))
                    transparents += 1
            plan.append((PROFONDEUR_PARAGRAPHE, genre, libelle, texte))

        # Les nœuds transparents consécutifs d'un même niveau, entre deux
        # paragraphes frères, doivent être MUTUALISÉS : sans ça chaque
        # paragraphe traîne sa propre chaîne et l'arbre explose.
        plan_compact = []
        for entree in plan:
            if (entree[1] == "transparent" and plan_compact
                    and plan_compact[-1][1] == "transparent"
                    and plan_compact[-1][0] == entree[0]):
                continue
            if entree[1] == "transparent" and plan_compact:
                # un transparent de niveau d n'est utile que si le précédent
                # élément n'est pas déjà à une profondeur >= d
                precedents = [e for e in plan_compact if e[0] < entree[0]]
                derniers = [e for e in plan_compact[::-1] if e[0] <= entree[0]]
                if derniers and derniers[0][0] == entree[0] and derniers[0][1] == "transparent":
                    continue
            plan_compact.append(entree)

        transparents_reels = sum(1 for e in plan_compact if e[1] == "transparent")

        # ------------------------------------------------------------------
        # Rapport
        # ------------------------------------------------------------------
        self.stdout.write("=" * 74)
        self.stdout.write("SOURCE")
        self.stdout.write("=" * 74)
        self.stdout.write(f"  {SOURCE.relative_to(settings.BASE_DIR)}")
        self.stdout.write(f"  titres      : {len(titres)}")
        for n in range(1, 6):
            c = sum(1 for t in titres if t[1] == n)
            if c:
                self.stdout.write(f"      niveau {n} : {c}")
        self.stdout.write(f"  paragraphes : {len(paragraphes)}")
        suffixes = [p[2] for p in paragraphes if "-" in p[2]]
        self.stdout.write(f"      dont suffixés : {len(suffixes)} — {', '.join(suffixes)}")
        conclusions = [e for e in elements if e[0] == "conclusion"]
        mentions = [e for e in elements if e[0] == "mention"]
        self.stdout.write(f"  conclusions : {len(conclusions)}   (liste sous « POUR CES MOTIFS »)")
        self.stdout.write(f"  mentions    : {len(mentions)}   (bordereau, signature)")

        self.stdout.write("")
        self.stdout.write("=" * 74)
        self.stdout.write("RÉGULARISATION")
        self.stdout.write("=" * 74)
        self.stdout.write(f"  profondeur cible des paragraphes : {PROFONDEUR_PARAGRAPHE}")
        self.stdout.write("  répartition d'origine :")
        for d in sorted(par_profondeur_origine):
            self.stdout.write(f"      rattachés à un titre de niveau {d} : "
                              f"{par_profondeur_origine[d]}")
        self.stdout.write(f"  paragraphes à replacer   : {replaces}")
        self.stdout.write(f"  nœuds transparents créés : {transparents_reels}")
        self.stdout.write(f"  nœuds au total           : {len(plan_compact) + 1} "
                          f"(racine comprise)")

        self.stdout.write("")
        self.stdout.write("=" * 74)
        self.stdout.write("RENUMÉROTATION")
        self.stdout.write("=" * 74)
        corr = [(p[2], i) for i, p in enumerate(
            [e for e in plan_compact if e[1] == "paragraphe"], start=1)]
        deplaces = [(a, n) for a, n in corr if a != str(n)]
        self.stdout.write(f"  paragraphes numérotés 1 à {len(corr)}")
        self.stdout.write(f"  numéros modifiés : {len(deplaces)} / {len(corr)}")
        self.stdout.write("  extrait :")
        for ancien, nouveau in corr[:6]:
            marque = "" if ancien == str(nouveau) else "   <-- change"
            self.stdout.write(f"      {ancien:>6}  ->  {nouveau}{marque}")
        self.stdout.write("      ...")
        for ancien, nouveau in corr[-4:]:
            self.stdout.write(f"      {ancien:>6}  ->  {nouveau}")

        if not options["apply"]:
            self.stdout.write("")
            self.stdout.write("Rapport seul — rien n'a été écrit. Ajouter --apply pour construire.")
            return

        # ------------------------------------------------------------------
        # Écriture
        # ------------------------------------------------------------------
        with transaction.atomic():
            if options["remplacer"]:
                ancien = Document.objects.get(pk=options["remplacer"])
                LibraryNode.objects.filter(document=ancien).delete()
                doc = ancien
                doc.title = options["titre"]
                doc.source_type = DocumentSource.PRODUCED
                doc.save()
            else:
                doc = Document.objects.create(
                    title=options["titre"],
                    source_type=DocumentSource.PRODUCED,
                )

            racine = LibraryNode.add_root(document=doc, item="Racine")
            racine = LibraryNode.objects.get(pk=racine.pk)
            derniers = {1: racine}
            numero = 0
            correspondance = []

            for profondeur, genre, libelle, texte in plan_compact:
                parent = derniers[max(k for k in derniers if k < profondeur)]

                if genre == "transparent":
                    noeud = parent.add_child(document=doc, item="")
                else:
                    if genre == "paragraphe":
                        numero += 1
                        correspondance.append((libelle, numero))
                    st = Statement.objects.create(text=texte, is_user_created=True)
                    noeud = parent.add_child(
                        document=doc,
                        # numero d'origine pour un paragraphe, « C-n » pour une
                        # conclusion, le titre pour un titre, vide pour une mention
                        item=libelle,
                        content_object=st,
                    )

                noeud = LibraryNode.objects.get(pk=noeud.pk)
                derniers[profondeur] = noeud
                for k in list(derniers):
                    if k > profondeur:
                        del derniers[k]

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Document {doc.pk} — {LibraryNode.objects.filter(document=doc).count()} nœuds, "
            f"{numero} paragraphes."))
        self.stdout.write("")
        self.stdout.write("  La correspondance ancien -> nouveau numéro reste EN BASE :")
        self.stdout.write("  LibraryNode.item porte le numéro du document déposé, la position")
        self.stdout.write("  dans l'arbre donne le numéro continu. Aucun fichier n'est écrit.")
        self.stdout.write("")
        self.stdout.write("      LibraryNode.objects.filter(document_id=%d, depth=%d)"
                          % (doc.pk, PROFONDEUR_PARAGRAPHE))
        self.stdout.write("          .order_by('path').values_list('item', flat=True)")
