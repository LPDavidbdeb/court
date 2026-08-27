"""
Importe les fichiers pièce du corpus `legal/` vers la base.

    python manage.py importer_pieces                 # simulation + rapport
    python manage.py importer_pieces --appliquer

La simulation est le mode par défaut : la commande écrit dans un champ qui peut
déjà contenir un texte relu et modifié, et cela ne se rejoue pas.

Les familles traitées sont celles que `core.piece_import.REGISTRE` marque
`accueille=True` — aujourd'hui les fichiers de fil et de courriel. Étendre à une
autre famille est une entrée de registre, pas une modification de cette
commande.

LE RAPPORT DE FIDÉLITÉ

Convertir peut perdre en silence : un titre qui devient un paragraphe, un lien
qui s'évapore. Le rapport compte donc les mêmes structures avant et après —
titres, lignes de tableau, liens, citations — et signale tout écart. Un fichier
sans écart n'a pas besoin d'être relu ; un fichier avec écart dit où regarder.
"""

import os
from datetime import datetime, timezone

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from core.piece_import import (REGISTRE, compter_html, compter_markdown,
                               convertir, resoudre)


class Command(BaseCommand):
    help = "Convertit les fichiers pièce du corpus en HTML et les range sur leur objet."

    def add_arguments(self, parser):
        parser.add_argument('--appliquer', action='store_true',
                            help="écrit en base ; sans ce drapeau, la commande simule")
        parser.add_argument('--ecraser', action='store_true',
                            help="autorise l'écrasement d'une analyse déjà présente")
        parser.add_argument('--fichier', action='append', default=None,
                            help="ne traiter que ce(s) fichier(s)")
        parser.add_argument('--corpus', default=None,
                            help="dossier du corpus (défaut : legal/)")

    def handle(self, *args, **options):
        corpus = options['corpus'] or os.path.join(settings.BASE_DIR, 'legal')
        appliquer = options['appliquer']

        fichiers = options['fichier'] or sorted(
            f for f in os.listdir(corpus)
            if f.startswith('piece_') and f.endswith('.md')
        )

        retenus, ignores = [], []
        for nom in fichiers:
            adaptateur, objet = resoudre(nom)
            if adaptateur is None:
                ignores.append((nom, "aucune famille du registre ne le reconnaît"))
            elif not adaptateur.accueille:
                ignores.append((nom, f"famille « {adaptateur.nom} » non importée"))
            elif objet is None:
                ignores.append((nom, f"{adaptateur.modele} introuvable en base"))
            else:
                retenus.append((nom, adaptateur, objet))

        # Deux fichiers qui visent le même objet se recouvriraient l'un l'autre.
        vus = {}
        collisions = []
        for nom, adaptateur, objet in retenus:
            cle = (adaptateur.modele, objet.pk)
            if cle in vus:
                collisions.append((nom, vus[cle], adaptateur.modele, objet.pk))
            else:
                vus[cle] = nom

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"\nCorpus {corpus} — {len(fichiers)} fichiers pièce"
            + ("" if appliquer else "   [SIMULATION]")))
        self.stdout.write(f"  retenus : {len(retenus)} · hors périmètre : {len(ignores)}")

        if collisions:
            self.stdout.write(self.style.ERROR(
                f"\n  {len(collisions)} collision(s) — deux fichiers pour un même objet :"))
            for nom, premier, modele, pk in collisions:
                self.stdout.write(self.style.ERROR(
                    f"     {nom} et {premier} visent tous deux {modele} {pk}"))
            self.stdout.write(self.style.ERROR(
                "  Rien n'est écrit tant qu'elles ne sont pas tranchées."))
            return

        ecarts, morts_total, resolus_total, ecrits = [], [], 0, 0
        occupes = []
        lignes = []

        for nom, adaptateur, objet in retenus:
            source = open(os.path.join(corpus, nom), encoding='utf-8').read()
            html, resolus, morts = convertir(source)
            avant = compter_markdown(source)
            apres = compter_html(html, morts)
            delta = {k: apres[k] - avant[k] for k in avant}
            # Les citations consécutives fusionnent en un seul <blockquote> :
            # l'écart y est normal et n'est pas compté comme une perte.
            perte = {k: v for k, v in delta.items() if v < 0 and k != 'lignes_citation'}
            ajout = {k: v for k, v in delta.items() if v > 0 and k != 'lignes_citation'}
            if perte or ajout:
                ecarts.append((nom, avant, apres, perte, ajout))
            morts_total += morts
            resolus_total += len(resolus)
            deja = bool((objet.analyse or '').strip())
            if deja and not options['ecraser']:
                occupes.append((nom, adaptateur.modele, objet.pk))
            lignes.append((nom, adaptateur, objet, html, len(resolus), len(morts), deja))

        self.stdout.write(f"\n  liens résolus : {resolus_total} · non résolus : {len(morts_total)}")
        if morts_total:
            from collections import Counter
            self.stdout.write("  renvois non résolus les plus fréquents :")
            for cible, n in Counter(morts_total).most_common(8):
                self.stdout.write(f"     {n:>3}×  {cible}")

        pertes = [e for e in ecarts if e[3]]
        ajouts = [e for e in ecarts if e[4] and not e[3]]
        if pertes:
            self.stdout.write(self.style.ERROR(
                f"\n  {len(pertes)} fichier(s) dont la conversion PERD une structure :"))
            for nom, avant, apres, perte, _ in pertes[:15]:
                detail = ", ".join(f"{k} {avant[k]}→{apres[k]}" for k in perte)
                self.stdout.write(self.style.ERROR(f"     {nom} : {detail}"))
        if ajouts:
            self.stdout.write(self.style.WARNING(
                f"\n  {len(ajouts)} fichier(s) où la conversion AJOUTE une structure "
                f"(à examiner : convertir ne devrait rien inventer) :"))
            for nom, avant, apres, _, ajout in ajouts[:10]:
                detail = ", ".join(f"{k} {avant[k]}→{apres[k]}" for k in ajout)
                self.stdout.write(self.style.WARNING(f"     {nom} : {detail}"))
        if not ecarts:
            self.stdout.write(self.style.SUCCESS(
                "\n  fidélité : titres, tableaux et liens intacts sur tous les fichiers"))

        if occupes:
            self.stdout.write(self.style.WARNING(
                f"\n  {len(occupes)} objet(s) portent déjà une analyse — ignorés "
                f"(--ecraser pour les remplacer) :"))
            for nom, modele, pk in occupes[:10]:
                self.stdout.write(f"     {modele} {pk} ← {nom}")

        if ignores:
            self.stdout.write(f"\n  hors périmètre ({len(ignores)}) :")
            from collections import Counter
            for raison, n in Counter(r for _, r in ignores).most_common():
                self.stdout.write(f"     {n:>4}  {raison}")

        if not appliquer:
            self.stdout.write(self.style.NOTICE(
                "\n  Rien n'a été écrit. --appliquer pour exécuter.\n"))
            return

        maintenant = datetime.now(timezone.utc)
        with transaction.atomic():
            for nom, adaptateur, objet, html, _, _, deja in lignes:
                if deja and not options['ecraser']:
                    continue
                objet.analyse = html
                objet.analyse_source = nom
                objet.analyse_maj = maintenant
                objet.save(update_fields=['analyse', 'analyse_source', 'analyse_maj'])
                ecrits += 1
        self.stdout.write(self.style.SUCCESS(f"\n  {ecrits} analyse(s) écrite(s).\n"))
