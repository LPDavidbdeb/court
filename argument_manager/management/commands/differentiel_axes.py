"""
Différentiel : ce que les axes veulent plaider  vs  ce qui est plaidé.

    python manage.py differentiel_axes
    python manage.py differentiel_axes --axe danse
    python manage.py differentiel_axes --rattacher      # écrit Fait.statement
    python manage.py differentiel_axes --seuil 0.45

Un `Fait` est un paragraphe de l'exposé. `Fait.statement` le rattache au
paragraphe réellement plaidé dans un document PRODUCED. Le différentiel lit
l'écart dans les deux sens :

  MANQUANT   — un fait de l'axe qu'aucun paragraphe ne plaide.
  ORPHELIN   — un paragraphe plaidé qu'aucun axe ne réclame.

L'appariement est LEXICAL, pas sémantique : recouvrement de termes distinctifs
pondérés par leur rareté dans le document. Ce choix est délibéré. Un
rapprochement par plongement vectoriel donnerait un meilleur rappel mais ne
s'expliquerait pas ; ici chaque appariement se justifie par les mots qu'il
partage, et se conteste sur la même base. C'est un audit, pas une recherche.

Rien n'est écrit sans `--rattacher`, et le rattachement ne touche que les faits
dont le meilleur candidat dépasse le seuil ET distance nettement le suivant :
un appariement ambigu doit être tranché à la main.
"""
import math
import textwrap
import re
import unicodedata
from collections import Counter, defaultdict

from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from argument_manager.models import Axe, Fait, AppuiFait
from document_manager.models import Document, DocumentSource, LibraryNode, Statement

# Mots trop fréquents en français juridique pour distinguer deux paragraphes.
VIDES = {
    'le', 'la', 'les', 'un', 'une', 'des', 'du', 'de', 'et', 'ou', 'a', 'à',
    'au', 'aux', 'en', 'dans', 'par', 'pour', 'sur', 'que', 'qui', 'quoi',
    'dont', 'ce', 'cet', 'cette', 'ces', 'il', 'elle', 'ils', 'elles', 'on',
    'se', 'sa', 'son', 'ses', 'leur', 'leurs', 'est', 'sont', 'etait',
    'etaient', 'ete', 'avoir', 'etre', 'plus', 'moins', 'tout', 'toute',
    'tous', 'toutes', 'pas', 'ne', 'ni', 'non', 'aussi', 'comme', 'meme',
    'entre', 'avec', 'sans', 'sous', 'lors', 'apres', 'avant', 'depuis',
    'pendant', 'selon', 'ainsi', 'donc', 'car', 'mais', 'y', 'd', 'l', 's',
    'n', 'c', 'j', 'm', 't', 'qu', 'demandeur', 'defenderesse', 'demanderesse',
    'defendeur', 'piece', 'pieces', 'appert', 'tel', 'telle',
}


# « 27 », « 22-A » — la numérotation du dépôt, suffixes compris.
RE_NUMERO = re.compile(r"^\d+(-[A-Z])?$")
RE_PHRASE = re.compile(r"(?<=[.;])\s+")


def mots(texte):
    t = unicodedata.normalize('NFKD', texte or '').encode('ascii', 'ignore').decode().lower()
    return [m for m in re.findall(r"[a-z0-9]+", t) if len(m) > 2 and m not in VIDES]


def phrases(texte):
    """Le paragraphe, plus chacune de ses phrases prises isolément."""
    p = [s.strip() for s in RE_PHRASE.split(texte or "") if len(s.strip()) > 30]
    return [texte] + p if len(p) > 1 else [texte]


class Command(BaseCommand):
    help = "Compare les faits des axes aux paragraphes réellement plaidés."

    def add_arguments(self, parser):
        parser.add_argument("--axe", default=None,
                            help="filtrer sur un axe (fragment du nom)")
        parser.add_argument("--doc", type=int, default=None,
                            help="document PRODUCED de référence (défaut : le plus fourni)")
        parser.add_argument("--seuil", type=float, default=0.30,
                            help="score minimal pour proposer un appariement")
        parser.add_argument("--rattacher", action="store_true",
                            help="écrit Fait.statement pour les appariements nets")

    # ------------------------------------------------------------------
    def handle(self, *args, **o):
        ct_stmt = ContentType.objects.get_for_model(Statement)

        doc = (Document.objects.filter(pk=o["doc"]).first() if o["doc"] else
               max(Document.objects.filter(source_type=DocumentSource.PRODUCED),
                   key=lambda d: LibraryNode.objects.filter(
                       document=d, content_type=ct_stmt).count()))
        noeuds = list(LibraryNode.objects.filter(document=doc, content_type=ct_stmt)
                      .order_by('path'))
        stmts = {s.pk: s for s in Statement.objects.filter(
            pk__in=[n.object_id for n in noeuds])}
        # Seuls les paragraphes NUMÉROTÉS sont des candidats. Les titres de
        # section sont eux aussi des Statement dans l'arbre ; les laisser
        # concourir faisait gagner « Les routines du soir pendant les cours de
        # danse » contre les paragraphes de fond, sur la seule présence du mot
        # « danse ». Un fait s'apparie à un paragraphe, jamais à un intertitre.
        paras = [(n, stmts[n.object_id]) for n in noeuds
                 if n.object_id in stmts
                 and n.item and RE_NUMERO.match(str(n.item).strip())]

        # idf sur le document : un mot présent partout ne distingue rien.
        df = Counter()
        for _, s in paras:
            df.update(set(mots(s.text)))
        N = max(1, len(paras))
        idf = {m: math.log(N / (1 + c)) + 1 for m, c in df.items()}

        def brut(a, b):
            ma, mb = set(mots(a)), set(mots(b))
            if not ma or not mb:
                return 0.0
            num = sum(idf.get(m, 1.0) for m in ma & mb)
            den = math.sqrt(sum(idf.get(m, 1.0) for m in ma) *
                            sum(idf.get(m, 1.0) for m in mb))
            return num / den if den else 0.0

        def score(fait, para):
            """
            Le meilleur des rapprochements : le paragraphe entier, ou l'une de
            ses phrases. Les paragraphes du dépôt agrègent plusieurs
            propositions — §28 porte la structure de l'école ET la réserve sur
            les dates. Comparer au paragraphe entier dilue la réserve au point
            de la déclarer absente alors qu'elle y est, mot pour mot.
            """
            return max(brut(fait, p) for p in phrases(para))

        axes = Axe.objects.all()
        if o["axe"]:
            axes = axes.filter(nom__icontains=o["axe"])

        self.stdout.write("=" * 88)
        self.stdout.write("DIFFÉRENTIEL — faits des axes  vs  paragraphes plaidés")
        self.stdout.write("=" * 88)
        self.stdout.write(f"  document de référence : doc {doc.pk} — {doc.title[:56]}")
        self.stdout.write(f"  paragraphes examinés  : {len(paras)}")
        self.stdout.write(f"  axes                  : {axes.count()}")

        reclames = set()          # pk de Statement réclamés par un fait
        a_ecrire = []

        for axe in axes:
            faits = axe.faits.all().order_by('ordre')
            self.stdout.write("")
            self.stdout.write("─" * 88)
            self.stdout.write(f"AXE — {axe.nom}")
            self.stdout.write(f"  cible {axe.cibles.count()} allégation(s) ; "
                              f"{faits.count()} faits ; "
                              f"{AppuiFait.objects.filter(fait__axes=axe).count()} appuis")
            self.stdout.write("─" * 88)

            for f in faits:
                if f.statement_id:
                    # Fait déjà rattaché : on n'apparie plus, on RESTITUE le
                    # verdict enregistré. Le rapprochement lexical n'a plus rien
                    # à dire ici — il a été remplacé par une lecture, et c'est
                    # elle qui fait foi.
                    reclames.add(f.statement_id)
                    n = f.numero_plaide()
                    raison = f.raison or ""
                    statut = "RATTACHÉ"
                    if raison.startswith("["):
                        statut = raison[1:raison.find("]")]
                        raison = raison[raison.find("]") + 1:].strip()
                    style = (self.style.WARNING if statut in
                             ("ENFOUI", "ABSENT") else lambda x: x)
                    self.stdout.write(style(
                        f"\n  [{f.ordre}] {statut}  →  §{n}   [{f.nature}]"))
                    self.stdout.write(f"      {f.enonce[:150]}")
                    if raison:
                        for ligne in textwrap.wrap(raison, 84)[:6]:
                            self.stdout.write(f"        {ligne}")
                    for ap in f.appuis.all():
                        self.stdout.write(f"        · {ap.role:<12} "
                                          f"{ap.content_type.model}-{ap.object_id}")
                    continue

                classe = sorted(((score(f.enonce, s.text), n, s) for n, s in paras),
                                key=lambda t: -t[0])
                meilleur = classe[0] if classe else (0.0, None, None)
                second = classe[1][0] if len(classe) > 1 else 0.0

                if meilleur[0] < o["seuil"]:
                    self.stdout.write(self.style.WARNING(
                        f"\n  [{f.ordre}] ABSENT DU DOSSIER   (meilleur score {meilleur[0]:.2f})"))
                    self.stdout.write(f"      {f.enonce[:150]}")
                    if meilleur[1] is not None:
                        self.stdout.write(f"      le moins loin : §{meilleur[1].item} — "
                                          f"{meilleur[2].text[:96]}")
                    continue

                net = meilleur[0] >= o["seuil"] and (meilleur[0] - second) >= 0.05
                marque = "APPARIÉ  " if net else "AMBIGU   "
                self.stdout.write(f"\n  [{f.ordre}] {marque} §{meilleur[1].item}  "
                                  f"score {meilleur[0]:.2f}"
                                  + ("" if net else f"  (2e à {second:.2f} — à trancher)"))
                self.stdout.write(f"      fait   : {f.enonce[:140]}")
                self.stdout.write(f"      plaidé : {meilleur[2].text[:140]}")
                reclames.add(meilleur[2].pk)
                if net:
                    a_ecrire.append((f, meilleur[2], meilleur[1].item))

        # --- les orphelins, section par section ---------------------------
        self.stdout.write("")
        self.stdout.write("=" * 88)
        self.stdout.write("ORPHELINS — paragraphes plaidés qu'aucun axe ne réclame")
        self.stdout.write("=" * 88)
        par_section = defaultdict(list)
        for n, s in paras:
            if s.pk in reclames:
                continue
            parent = n.get_parent()
            titre = "—"
            while parent is not None:
                if parent.item and not str(parent.item).strip().isdigit():
                    titre = str(parent.item)
                    break
                parent = parent.get_parent()
            par_section[titre].append((n, s))
        self.stdout.write(f"  {sum(len(v) for v in par_section.values())} paragraphe(s) "
                          f"sur {len(paras)}, répartis en {len(par_section)} section(s).")
        self.stdout.write("  Un orphelin n'est pas une faute : tout le dossier n'est pas "
                          "couvert par les deux axes construits.")
        for titre, items in sorted(par_section.items(), key=lambda kv: -len(kv[1]))[:8]:
            self.stdout.write(f"\n    {len(items):>3} × {titre[:74]}")

        # --- écriture ------------------------------------------------------
        self.stdout.write("")
        self.stdout.write("=" * 88)
        if not a_ecrire:
            self.stdout.write("  aucun appariement net à écrire.")
            return
        self.stdout.write(f"  {len(a_ecrire)} appariement(s) net(s) :")
        for f, s, num in a_ecrire:
            self.stdout.write(f"     fait {f.pk} → §{num} (statement {s.pk})")
        if not o["rattacher"]:
            self.stdout.write("\n  Rien n'a été écrit. Relancer avec --rattacher.")
            return
        with transaction.atomic():
            for f, s, _ in a_ecrire:
                f.statement = s
                f.save(update_fields=["statement"])
        self.stdout.write(self.style.SUCCESS(
            f"\n  {len(a_ecrire)} fait(s) rattaché(s). "
            f"{Fait.objects.exclude(statement=None).count()} / {Fait.objects.count()} "
            f"faits sont désormais reliés à un paragraphe plaidé."))
