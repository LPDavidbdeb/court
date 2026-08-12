"""
Confronte chaque document à son schéma de niveaux, et rapporte les écarts.

    python manage.py verifier_schemas
    python manage.py verifier_schemas --document 1

NE CORRIGE RIEN. Un schéma est une affirmation sur un document, pas une
contrainte de base : rien n'empêche un arbre de s'en écarter, et c'est
délibéré — un acte de forme imprévue doit pouvoir entrer tel quel. Le prix de
cette souplesse est qu'il faut un contrôle explicite, sinon le schéma devient
une documentation qui ment.

CE QUI EST CONTRÔLÉ

  1. profondeur hors schéma   un nœud occupe une profondeur que le schéma n'a pas prévue
  2. niveau déclaré vide      le schéma prévoit une profondeur qu'aucun nœud n'occupe
  3. transparent feuille      un nœud sans contenu qui ne porte aucun enfant — il
                              n'aurait aucune raison d'exister
  4. niveau hétérogène        une profondeur mélange des contenus de natures
                              différentes (sous-items marqués « a) » et paragraphes
                              de continuation, par exemple) : le rôle unique que le
                              schéma lui attribue est alors une approximation
  5. porteur stérile          un nœud dont le rôle est structurant (section, thème…)
                              mais qui n'a pas d'enfant
  6. paragraphe vide          un nœud PARAGRAPHE sans texte

Un écart n'est pas nécessairement une faute : il signale un endroit où le
document et la règle divergent, et c'est à la lecture de décider lequel des deux
a raison.
"""
import re

from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

from document_manager.models import (
    Document, LibraryNode, RoleNiveau, Statement,
)

MARQUEUR_ITEM = re.compile(r"^\s*(?:[a-z]\)|[a-z]\.|\d+\)|[ivx]+\)|[-•*])\s", re.I)

STRUCTURANTS = {
    RoleNiveau.RACINE, RoleNiveau.SECTION, RoleNiveau.SOUS_SECTION,
    RoleNiveau.THEME, RoleNiveau.SOUS_THEME, RoleNiveau.CHAPEAU,
}


def texte_de(noeud):
    obj = noeud.content_object
    if obj is None:
        return None
    return (getattr(obj, "text", None) or getattr(obj, "quote_text", None)
            or getattr(obj, "titre", None) or str(obj))


class Command(BaseCommand):
    help = "Rapporte les écarts entre les documents et leur schéma de niveaux."

    def add_arguments(self, parser):
        parser.add_argument("--document", type=int, default=None,
                            help="ne vérifier qu'un document")

    def handle(self, *args, **options):
        docs = Document.objects.select_related("schema").order_by("pk")
        if options["document"]:
            docs = docs.filter(pk=options["document"])

        total = 0
        for doc in docs:
            ecarts = self.verifier(doc)
            total += len(ecarts)
            self.stdout.write("")
            entete = f"doc {doc.pk} [{doc.source_type}] « {doc.title[:52]} »"
            self.stdout.write(self.style.MIGRATE_HEADING(entete))
            if doc.schema is None:
                self.stdout.write("    aucun schéma — non vérifiable, et c'est licite")
                continue
            self.stdout.write(f"    schéma : {doc.schema.nom}")
            if not ecarts:
                self.stdout.write(self.style.SUCCESS("    conforme"))
                continue
            for genre, detail in ecarts:
                self.stdout.write(f"    {genre:<22} {detail}")

        self.stdout.write("")
        self.stdout.write(f"{total} écart(s) au total. Aucun n'a été corrigé.")

    def verifier(self, doc):
        if doc.schema is None:
            return []

        ecarts = []
        noeuds = list(LibraryNode.objects.filter(document=doc).order_by("path"))
        enfants = {}
        for n in noeuds:
            enfants[n.pk] = n.get_children_count()

        prevues = {n.profondeur: n for n in doc.schema.niveaux.all()}
        occupees = {}
        for n in noeuds:
            occupees.setdefault(n.depth, []).append(n)

        # 1. profondeur hors schéma
        for prof in sorted(set(occupees) - set(prevues)):
            ecarts.append(("profondeur hors schéma",
                           f"profondeur {prof} : {len(occupees[prof])} nœud(s), "
                           f"aucun niveau déclaré"))

        # 2. niveau déclaré vide
        for prof in sorted(set(prevues) - set(occupees)):
            ecarts.append(("niveau déclaré vide",
                           f"profondeur {prof} ({prevues[prof].role}) : aucun nœud"))

        for prof, groupe in sorted(occupees.items()):
            niveau = prevues.get(prof)

            # 3. transparent feuille
            orphelins = [n for n in groupe
                         if n.content_type_id is None and enfants[n.pk] == 0]
            if orphelins:
                ecarts.append(("transparent feuille",
                               f"profondeur {prof} : {len(orphelins)} nœud(s) sans "
                               f"contenu ni enfant — pk {[n.pk for n in orphelins][:6]}"))

            if niveau is None:
                continue

            # 4. niveau hétérogène
            avec_marqueur, sans_marqueur = [], []
            for n in groupe:
                t = texte_de(n)
                if t is None:
                    continue
                (avec_marqueur if MARQUEUR_ITEM.match(t) else sans_marqueur).append(n)
            if avec_marqueur and sans_marqueur:
                ecarts.append(("niveau hétérogène",
                               f"profondeur {prof} déclarée « {niveau.role} » : "
                               f"{len(avec_marqueur)} nœud(s) marqués « a) / 1) / - » "
                               f"et {len(sans_marqueur)} non marqués"))

            # 5. porteur stérile
            if niveau.role in STRUCTURANTS:
                steriles = [n for n in groupe if enfants[n.pk] == 0]
                if steriles:
                    ecarts.append(("porteur stérile",
                                   f"profondeur {prof} ({niveau.role}) : "
                                   f"{len(steriles)} nœud(s) sans enfant — "
                                   f"pk {[n.pk for n in steriles][:6]}"))

            # 6. paragraphe vide
            if niveau.role == RoleNiveau.PARAGRAPHE:
                vides = [n for n in groupe if not (texte_de(n) or "").strip()]
                if vides:
                    ecarts.append(("paragraphe vide",
                                   f"profondeur {prof} : {len(vides)} nœud(s) "
                                   f"sans texte — pk {[n.pk for n in vides][:6]}"))

        return ecarts
