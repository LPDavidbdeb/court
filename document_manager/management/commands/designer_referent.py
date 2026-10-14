"""
Déclarer qu'un document est un acte déposé, et prendre son instantané.

Tant que cette ligne n'existe pas, les gardes de `protection.py` ne voient
qu'un document produit comme un autre : elles laissent écrire.
"""
import hashlib
import os

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from document_manager.models import Document, ReferentHistorique
from document_manager import referent as referent_service


def _sha256(chemin):
    if not chemin or not os.path.exists(chemin):
        return ""
    h = hashlib.sha256()
    with open(chemin, 'rb') as f:
        for bloc in iter(lambda: f.read(65536), b""):
            h.update(bloc)
    return h.hexdigest()


class Command(BaseCommand):
    help = "Déclare un document comme référent historique et prend son instantané."

    def add_arguments(self, parser):
        parser.add_argument("--document", type=int, required=True,
                            help="pk du document — jamais codé en dur")
        parser.add_argument("--libelle", required=True)
        parser.add_argument("--depose-le", default=None, help="AAAA-MM-JJ")
        parser.add_argument("--source", default="",
                            help="fichier archivé faisant foi du contenu")
        parser.add_argument("--concordance", default="",
                            help="table des numéros imprimés, si elle existe")
        parser.add_argument("--motif", default="désignation du référent")
        parser.add_argument("--instantane-seulement", action="store_true",
                            help="le référent existe déjà : prendre un instantané")

    @transaction.atomic
    def handle(self, *args, **o):
        w = self.stdout.write
        doc = Document.objects.filter(pk=o["document"]).first()
        if doc is None:
            raise CommandError(f"Document {o['document']} introuvable.")

        ref = ReferentHistorique.objects.filter(document=doc).first()
        if ref is None:
            if o["instantane_seulement"]:
                raise CommandError(
                    f"Document {doc.pk} n'est pas un référent : rien à instantaner."
                )
            ref = ReferentHistorique.objects.create(
                document=doc,
                libelle=o["libelle"],
                depose_le=o["depose_le"] or None,
                source_archivee=o["source"],
                source_sha256=_sha256(o["source"]),
                concordance_ref=o["concordance"],
                concordance_sha256=_sha256(o["concordance"]),
            )
            w(self.style.SUCCESS(f"  Référent créé : {ref}"))
        else:
            w(f"  Référent déjà déclaré : {ref}")

        inst = referent_service.prendre_instantane(ref, o["motif"])
        w("")
        w(f"  INSTANTANÉ  {inst.pris_le:%Y-%m-%d %H:%M:%S %Z}")
        w(f"    motif              : {inst.motif}")
        w(f"    nœuds              : {inst.nombre_noeuds}")
        w(f"    appuis de juillet  : {inst.nombre_appuis}")
        w(f"    empreinte globale  : {inst.empreinte_globale}")
        w("")
        w(f"  Source archivée      : {ref.source_archivee or '(aucune)'}")
        w(f"    sha256             : {ref.source_sha256 or '—'}")
        w(f"  Concordance          : {ref.concordance_ref or '(aucune)'}")
        w(f"    sha256             : {ref.concordance_sha256 or '—'}")
        w("")
        w(self.style.WARNING(
            "  Les gardes sont actives : le contenu de cet acte ne se modifie "
            "plus, quelle que soit la voie d'appel."))
