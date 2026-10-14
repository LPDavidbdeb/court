"""
T01 puis T03 — contrôler le rattachement, puis écrire les numéros du papier.

Sans `--appliquer`, la commande ne fait que constater : c'est le mode rapport
exigé par le cahier. Avec, elle refait le contrôle dans sa propre transaction
avant d'écrire une seule valeur.

Aucune option de forçage. Une anomalie bloque l'application — c'est tout l'objet
du contrôle, et un drapeau qui le contournerait le rendrait décoratif.
"""
import json

from django.core.management.base import BaseCommand, CommandError

from document_manager.models import Document, NumberingMode
from document_manager import referent as referent_service
from document_manager import reprise_numeros as rn


class Command(BaseCommand):
    help = ("Contrôle le rattachement des numéros imprimés, puis les applique "
            "sur demande.")

    def add_arguments(self, parser):
        parser.add_argument("--document", type=int, required=True)
        parser.add_argument("--concordance", required=True,
                            help="JSON de la table .md → imprimé")
        parser.add_argument("--markdown", required=True,
                            help="Markdown archivé, pour le contrôle du contenu")
        parser.add_argument("--appliquer", action="store_true",
                            help="écrire ; sans ce drapeau, simple constat")
        parser.add_argument("--passer-en-stored", action="store_true",
                            help="après application, lire les numéros conservés")
        parser.add_argument("--manifeste", default=None,
                            help="chemin où écrire le manifeste d'appariement")
        parser.add_argument("--limite", type=int, default=12)

    def handle(self, *args, **o):
        w = self.stdout.write
        doc = Document.objects.filter(pk=o["document"]).first()
        if doc is None:
            raise CommandError(f"Document {o['document']} introuvable.")

        w("=" * 78)
        w(f"RATTACHEMENT — {doc.title[:58]}")
        w("=" * 78)
        w(f"  document        : {doc.pk}  ({doc.source_type}, mode {doc.numbering_mode})")
        w(f"  concordance     : {o['concordance']}")
        w(f"  markdown        : {o['markdown']}")
        w("")

        rapport = rn.verifier(doc, o["concordance"], o["markdown"])
        self._afficher(rapport, o["limite"])

        if o["manifeste"]:
            with open(o["manifeste"], "w", encoding="utf-8") as f:
                json.dump({
                    'document': doc.pk,
                    'concordance': o['concordance'],
                    'markdown': o['markdown'],
                    'regles_normalisation': rn.REGLES_NORMALISATION,
                    'resume': rapport.resume(),
                    'associations': rapport.manifeste,
                    'anomalies': {
                        'manquantes': rapport.manquantes,
                        'ambigues': rapport.ambigues,
                        'doublons': rapport.doublons,
                        'oublies': rapport.oublies,
                        'contenus_incompatibles': rapport.contenus_incompatibles,
                        'etrangers': rapport.etrangers,
                        'conflits': rapport.conflits,
                    },
                }, f, ensure_ascii=False, indent=2)
            w(f"  Manifeste écrit : {o['manifeste']}")
            w("")

        if not rapport.conforme:
            w(self.style.ERROR(
                "  CONTRÔLE NON CONFORME — l'application est bloquée."))
            raise SystemExit(1)

        w(self.style.SUCCESS("  CONTRÔLE CONFORME."))
        if not o["appliquer"]:
            w("")
            w("  Mode rapport : aucune écriture. Ajouter --appliquer pour écrire.")
            return

        ref = referent_service.referent_de(doc)
        if ref is None:
            raise CommandError(
                f"Document {doc.pk} n'est pas déclaré référent historique. "
                f"Lancer d'abord `designer_referent`, qui pose les gardes et "
                f"prend l'instantané."
            )
        inst = referent_service.prendre_instantane(ref, "avant reprise des numéros")
        w("")
        w(f"  Instantané pris   : {inst.empreinte_globale[:16]}… "
          f"({inst.nombre_noeuds} nœuds)")

        applique = rn.appliquer(doc, o["concordance"], o["markdown"],
                                rapport_prealable=rapport)
        w(f"  Numéros écrits    : {applique.ecritures}")

        controle = rn.controler_apres_reprise(doc, o["concordance"], o["markdown"])
        w("")
        w("  CONTRÔLE APRÈS REPRISE")
        w(f"    valeurs contrôlées        : {controle['controles']}")
        w(f"    conformes                 : {controle['verifies']}")
        w(f"    écarts                    : {len(controle['ecarts'])}")
        w(f"    suffixes conservés        : {controle['suffixes']}")
        w(f"    divergents du Markdown    : {controle['divergents_du_markdown']}")
        for e in controle['ecarts'][:o["limite"]]:
            w(self.style.ERROR(f"      nœud {e['noeud']} : "
                               f"attendu {e['attendu']}, obtenu {e['obtenu']!r}"))

        ecarts_ref = referent_service.comparer(inst)
        intact = referent_service.contenu_intact(ecarts_ref)
        w("")
        w(f"  CONTENU DU RÉFÉRENT : "
          f"{'intact' if intact else 'MODIFIÉ'} "
          f"(textes {len(ecarts_ref['textes'])}, arbre "
          f"{len(ecarts_ref['arborescence'])}, items {len(ecarts_ref['items'])}, "
          f"appuis {len(ecarts_ref['appuis'])})")
        w(f"  métadonnées de numérotation modifiées : {len(ecarts_ref['numeros'])}")

        if o["passer_en_stored"]:
            rn.passer_en_stored(doc)
            w("")
            w(self.style.SUCCESS(
                f"  Document {doc.pk} en mode {NumberingMode.STORED} : "
                f"il affiche désormais les numéros du papier."))

        if controle['ecarts'] or not intact:
            raise SystemExit(1)

    def _afficher(self, r, limite):
        w = self.stdout.write
        res = r.resume()
        w("  ASSERTIONS")
        w(f"    lignes de référence              : {res['lignes_reference']}")
        w(f"    lignes appariées                 : {res['lignes_appariees']}")
        w(f"    occurrences distinctes appariées : {res['noeuds_distincts']}")
        for cle, libelle in (
            ('manquantes', "ligne sans occurrence"),
            ('ambigues', "ligne à plusieurs occurrences"),
            ('doublons', "occurrence visée plusieurs fois"),
            ('oublies', "paragraphe admissible non apparié"),
            ('contenus_incompatibles', "contenu incompatible"),
            ('etrangers', "occurrence d'un autre document"),
            ('conflits', "numéro présent et divergent"),
        ):
            n = res[cle]
            style = self.style.ERROR if n else (lambda x: x)
            w(style(f"    {libelle:<33}: {n}"))
            if n:
                for item in getattr(r, cle)[:limite]:
                    w(self.style.ERROR(f"        {item}"))
        w("")
