"""
Ce qui ne se supprime pas, et ce qui se supprime à condition de laisser une trace.

LA RÈGLE. Un acte REPRODUIT est la copie d'une pièce qui existe hors de la base :
une requête adverse, une déclaration assermentée, un courriel. Le dossier s'en
sert pour dire « voici ce qui a été écrit ». Supprimer un de ses nœuds, ou
l'énoncé qu'un de ses nœuds porte, ferait disparaître la citation en laissant
l'argument qui s'y appuie — et rien ne signalerait le trou. C'est donc refusé,
quelle que soit la voie d'appel.

Les documents PRODUITS, eux, se rédigent : leurs occurrences se suppriment. Mais
une occurrence engagée dans une concordance emporte avec elle ce que la
comparaison a besoin de lire ; elle est donc ARCHIVÉE avant de disparaître.

POURQUOI DES SIGNAUX, ET NON UNE SURCHARGE DE `delete()`. Une surcharge de
`Model.delete()` ne voit pas `QuerySet.delete()`, qui ne l'appelle jamais, ni les
cascades, qui passent par le collecteur. `pre_delete` voit les trois — et,
effet secondaire décisif, le seul fait d'enregistrer un receveur désactive le
« fast delete » de Django, cette optimisation qui supprime en masse sans
instancier les objets. Sans cela, `LibraryNode.objects.filter(...).delete()`
passerait sous les gardes.

L'exception levée dans `pre_delete` remonte à travers la transaction que le
collecteur ouvre : l'opération entière est annulée. C'est ce qui garantit qu'un
lot visant un seul nœud protégé ne supprime aucun des autres.
"""
import hashlib

from django.core.exceptions import PermissionDenied
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from document_manager.models import (
    Document, DocumentSource, LibraryNode, NoeudArchive, ReferentHistorique,
    Statement,
)


class SuppressionRefusee(PermissionDenied):
    """Une suppression interdite par la politique du dossier."""


class ModificationRefusee(PermissionDenied):
    """Une écriture interdite sur le contenu d'un acte déposé."""


# Mis à True le temps d'une opération délibérée qui doit traverser les gardes —
# par exemple la reprise des numéros imprimés, qui ÉCRIT sur le référent, mais
# seulement un champ de métadonnée. Voir `metadonnees_autorisees`.
class _Contexte:
    autorise_metadonnees = False
    suppression_autorisee_pk = None


_ctx = _Contexte()


class metadonnees_autorisees:
    """
    Autorise, le temps du bloc, les écritures de métadonnées de numérotation
    sur un référent protégé.

    Ce que cela n'autorise pas : toucher au texte, à l'arborescence ou aux
    appuis. La garde continue de refuser ces champs-là.
    """

    def __enter__(self):
        self._prec = _ctx.autorise_metadonnees
        _ctx.autorise_metadonnees = True
        return self

    def __exit__(self, *a):
        _ctx.autorise_metadonnees = self._prec
        return False


class suppression_autorisee:
    """
    Autorise la suppression d'un nœud PRODUCED précis et de ses descendants.

    Ne lève aucune protection REPRODUCED : un nœud reproduit reste refusé même
    à l'intérieur de ce bloc. Le drapeau sert à distinguer une suppression
    décidée et archivée d'une suppression accidentelle.
    """

    def __init__(self, noeud_pk):
        self.noeud_pk = noeud_pk

    def __enter__(self):
        self._prec = _ctx.suppression_autorisee_pk
        _ctx.suppression_autorisee_pk = self.noeud_pk
        return self

    def __exit__(self, *a):
        _ctx.suppression_autorisee_pk = self._prec
        return False


# ---------------------------------------------------------------------------
# Lectures de base
# ---------------------------------------------------------------------------

def est_reproduit(document):
    return document.source_type == DocumentSource.REPRODUCED


def documents_du_statement(statement_pk):
    """Les documents où cet énoncé apparaît, par ses occurrences réelles.

    Par les OCCURRENCES, et non par `is_user_created` : ce drapeau dit qui a
    saisi l'énoncé, pas où il sert. Un énoncé importé puis réutilisé dans un
    document produit reste marqué « importé », et un énoncé saisi à la main
    peut très bien être cité dans un acte reproduit.
    """
    ct = ContentType.objects.get_for_model(Statement)
    return set(
        LibraryNode.objects.filter(content_type=ct, object_id=statement_pk)
        .values_list('document__source_type', flat=True)
    )


def statement_protege(statement_pk):
    """Cet énoncé est-il utilisé par au moins un document REPRODUIT ?"""
    return DocumentSource.REPRODUCED in documents_du_statement(statement_pk)


def est_referent(document_pk):
    return ReferentHistorique.objects.filter(document_id=document_pk).exists()


def archiver_noeud(noeud, motif="", statement_supprime=False):
    """Conserve ce qu'une occurrence portait, avant sa disparition physique."""
    texte = ""
    obj = noeud.content_object
    if obj is not None:
        texte = getattr(obj, 'text', None) or ""
    return NoeudArchive.objects.create(
        document=noeud.document,
        noeud_pk=noeud.pk,
        path=noeud.path,
        depth=noeud.depth,
        item=noeud.item or "",
        paragraph_number=noeud.paragraph_number or "",
        statement_pk=noeud.object_id,
        statement_supprime=statement_supprime,
        texte=texte,
        texte_sha256=hashlib.sha256(texte.encode('utf-8')).hexdigest() if texte else "",
        motif=motif,
    )


# ---------------------------------------------------------------------------
# Les gardes
# ---------------------------------------------------------------------------

@receiver(pre_delete, sender=LibraryNode, dispatch_uid="e01_garde_noeud")
def garde_suppression_noeud(sender, instance, **kwargs):
    """Refuse la suppression d'un nœud reproduit ou appartenant au référent."""
    if est_reproduit(instance.document):
        raise SuppressionRefusee(
            f"Nœud {instance.pk} : il appartient au document REPRODUIT "
            f"« {instance.document.title[:60]} ». Un acte reproduit ne se "
            f"modifie pas — c'est la copie d'une pièce."
        )
    if est_referent(instance.document_id):
        raise SuppressionRefusee(
            f"Nœud {instance.pk} : il appartient au référent historique "
            f"« {instance.document.title[:60]} », acte déposé. Sa structure "
            f"est figée."
        )


@receiver(pre_delete, sender=Statement, dispatch_uid="e01_garde_statement")
def garde_suppression_statement(sender, instance, **kwargs):
    """
    Refuse la suppression d'un énoncé utilisé par un acte reproduit.

    Refuse aussi celle d'un énoncé encore porté par une occurrence vivante :
    la clé générique n'a pas de contrainte d'intégrité, donc rien n'empêcherait
    un nœud actif de pointer dans le vide.
    """
    ct = ContentType.objects.get_for_model(Statement)
    occurrences = list(
        LibraryNode.objects.filter(content_type=ct, object_id=instance.pk)
        .select_related('document')
    )
    for n in occurrences:
        if est_reproduit(n.document):
            raise SuppressionRefusee(
                f"Statement {instance.pk} : utilisé par le document REPRODUIT "
                f"« {n.document.title[:60]} » (nœud {n.pk}). Protégé."
            )
        if est_referent(n.document_id):
            raise SuppressionRefusee(
                f"Statement {instance.pk} : utilisé par le référent historique "
                f"« {n.document.title[:60]} » (nœud {n.pk}). Protégé."
            )
    if occurrences:
        raise SuppressionRefusee(
            f"Statement {instance.pk} : encore porté par "
            f"{len(occurrences)} occurrence(s) ({[n.pk for n in occurrences]}). "
            f"Supprimer d'abord les occurrences, sinon elles désigneraient un "
            f"objet disparu."
        )


@receiver(pre_delete, sender=Document, dispatch_uid="e01_garde_document")
def garde_suppression_document(sender, instance, **kwargs):
    """
    Refuse la suppression d'un acte reproduit ou d'un référent.

    Sans cela, `Document.delete()` emporterait ses nœuds en cascade : la garde
    sur LibraryNode les refuserait un par un, mais autant le dire ici, où le
    diagnostic est lisible.
    """
    if est_reproduit(instance):
        raise SuppressionRefusee(
            f"Document {instance.pk} : REPRODUIT. Sa suppression emporterait "
            f"ses nœuds et les citations qui s'y appuient."
        )
    if est_referent(instance.pk):
        raise SuppressionRefusee(
            f"Document {instance.pk} : référent historique. Acte déposé."
        )


@receiver(pre_save, sender=Statement, dispatch_uid="e01_garde_texte_statement")
def garde_modification_statement(sender, instance, **kwargs):
    """
    Refuse la réécriture en place d'un énoncé d'un acte reproduit ou du référent.

    C'est le chemin par lequel une modification de la version CIBLE atteindrait
    la SOURCE : les deux versions partagent des Statements tant que le
    paragraphe n'a pas été réécrit, et `ajax_edit_node` écrivait sur l'objet
    partagé. Le texte de l'acte déposé changeait alors sans que personne ne
    l'ait demandé. La version cible doit recevoir son propre Statement —
    voir `concordance.detacher_pour_edition`.
    """
    if instance.pk is None:
        return
    ancien = Statement.objects.filter(pk=instance.pk).values_list('text', flat=True).first()
    if ancien is None or ancien == instance.text:
        return  # création, ou sauvegarde sans changement de contenu
    ct = ContentType.objects.get_for_model(Statement)
    for n in (LibraryNode.objects.filter(content_type=ct, object_id=instance.pk)
              .select_related('document')):
        if est_reproduit(n.document):
            raise ModificationRefusee(
                f"Statement {instance.pk} : son texte est cité par le document "
                f"REPRODUIT « {n.document.title[:60]} ». Pour réécrire la "
                f"version cible, lui donner son propre Statement."
            )
        if est_referent(n.document_id):
            raise ModificationRefusee(
                f"Statement {instance.pk} : son texte appartient au référent "
                f"historique « {n.document.title[:60]} », acte déposé. Pour "
                f"réécrire la version cible, lui donner son propre Statement."
            )


@receiver(pre_save, sender=LibraryNode, dispatch_uid="e01_garde_noeud_maj")
def garde_modification_noeud(sender, instance, **kwargs):
    """
    Sur un référent, n'autorise que les métadonnées de numérotation.

    `paragraph_number` est précisément la métadonnée que l'Epic ajoute à l'acte
    déposé : elle consigne ce que le papier porte, elle ne le change pas. Tout
    le reste — `item`, le rattachement du contenu, la place dans l'arbre — est
    refusé hors d'un bloc `metadonnees_autorisees`.
    """
    if instance.pk is None:
        return
    if not est_referent(instance.document_id):
        return
    ancien = LibraryNode.objects.filter(pk=instance.pk).first()
    if ancien is None:
        return
    surveilles = ('item', 'path', 'depth', 'content_type_id', 'object_id',
                  'document_id', 'is_evidence')
    changes = [c for c in surveilles
               if getattr(ancien, c) != getattr(instance, c)]
    if changes:
        raise ModificationRefusee(
            f"Nœud {instance.pk} du référent historique : champs {changes} "
            f"modifiés. Seules les métadonnées de numérotation sont admises."
        )
    if ancien.paragraph_number != instance.paragraph_number \
            and not _ctx.autorise_metadonnees:
        raise ModificationRefusee(
            f"Nœud {instance.pk} du référent : `paragraph_number` ne s'écrit "
            f"que dans un bloc `metadonnees_autorisees` — c'est-à-dire par la "
            f"reprise contrôlée, après son test de rattachement."
        )
