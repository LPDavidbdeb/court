"""
Ce qu'un paragraphe de l'acte déposé est devenu dans la version modifiée.

CE QUE LA CONCORDANCE N'EST PAS. Ce n'est pas une comparaison de numéros. Les
deux versions numérotent indépendamment — la source affiche ce que son papier
porte, la cible ce que sa structure calcule — et deux paragraphes portant le
même numéro n'ont aucune raison de se correspondre. Les liens portent sur les
OCCURRENCES, dont les identifiants ne bougent pas quand la rédaction déplace un
paragraphe.

CE QU'ELLE NE DÉCIDE PAS NON PLUS. L'absence de lien signifie « à établir », et
rien d'autre. Ni « ajout », ni « retrait », ni « fait nouveau » : ce sont des
décisions, qui s'écrivent. Une ressemblance de texte peut SUGGÉRER un
rapprochement ; elle ne le confirme pas, parce que deux paragraphes voisins d'un
même acte se ressemblent souvent plus que l'original et sa réécriture.

TROIS CONFIRMATIONS DISTINCTES, qu'il ne faut pas laisser se tenir lieu l'une de
l'autre :

    le TRAITEMENT ÉDITORIAL   « ce texte-ci est bien la reformulation de
                              celui-là » — porté par `Correspondance.etat` ;
    les APPUIS                « cette pièce appuie ce texte, pour cette
                              portée » — porté par `ConfirmationAppui` ;
    les CITATIONS             « ce "P-12" désigne cette pièce » — porté par
                              `AncrageCitation`.

Reconfirmer les pièces d'un paragraphe réécrit ne dit rien de la première
question. C'est la confusion que `etat_courant()` existe pour empêcher.
"""
from django.db import transaction

from document_manager.models import (
    Correspondance, EtatConfirmation, ExtremiteCorrespondance, LibraryNode,
    RoleExtremite, Statement, TraitementEditorial, VersionTexte,
)
from document_manager.protection import (
    SuppressionRefusee, archiver_noeud, est_reproduit, statement_protege,
)


# ---------------------------------------------------------------------------
# Créer et confirmer des liens
# ---------------------------------------------------------------------------

@transaction.atomic
def relier(document_source, document_cible, sources=(), cibles=(),
           traitement=TraitementEditorial.A_ETABLIR, deplace=False,
           motif="", note=""):
    """
    Enregistre une correspondance entre n occurrences source et m occurrences cible.

    `sources=()` décrit un AJOUT, `cibles=()` un RETRAIT — à condition que le
    traitement le dise. Un groupe vide des deux côtés n'a pas de sens et est
    refusé.
    """
    sources, cibles = list(sources), list(cibles)
    if not sources and not cibles:
        raise ValueError("Une correspondance sans aucune extrémité ne dit rien.")
    for n in sources:
        if n.document_id != document_source.pk:
            raise ValueError(
                f"Nœud {n.pk} n'appartient pas au document source "
                f"{document_source.pk} mais au {n.document_id}.")
    for n in cibles:
        if n.document_id != document_cible.pk:
            raise ValueError(
                f"Nœud {n.pk} n'appartient pas au document cible "
                f"{document_cible.pk} mais au {n.document_id}.")

    corr = Correspondance.objects.create(
        document_source=document_source, document_cible=document_cible,
        traitement=traitement, deplace=deplace, motif=motif, note=note,
    )
    for i, n in enumerate(sources):
        ExtremiteCorrespondance.objects.create(
            correspondance=corr, role=RoleExtremite.SOURCE, noeud=n, ordre=i)
    for i, n in enumerate(cibles):
        ExtremiteCorrespondance.objects.create(
            correspondance=corr, role=RoleExtremite.CIBLE, noeud=n, ordre=i)
    return corr


@transaction.atomic
def confirmer_traitement(correspondance, traitement, motif="", deplace=None):
    """
    Décide du traitement éditorial, en retenant les textes examinés.

    Les versions sont captées MAINTENANT : c'est ce qui permettra de dire, après
    une réécriture, que la décision portait sur un autre texte.
    """
    correspondance.traitement = traitement
    if deplace is not None:
        correspondance.deplace = deplace
    correspondance.motif = motif or correspondance.motif
    correspondance.etat = EtatConfirmation.CONFIRME
    from django.utils import timezone
    correspondance.decide_le = timezone.now()
    correspondance.save()

    correspondance.versions_source_examinees.clear()
    correspondance.versions_cible_examinees.clear()
    for role, champ in ((RoleExtremite.SOURCE, correspondance.versions_source_examinees),
                        (RoleExtremite.CIBLE, correspondance.versions_cible_examinees)):
        for e in correspondance.extremites.filter(role=role).select_related('noeud'):
            if e.noeud is None:
                continue
            obj = e.noeud.content_object
            if isinstance(obj, Statement):
                champ.add(VersionTexte.capter(
                    obj, motif=f"traitement {traitement} confirmé"))
    return correspondance


def correspondances_de(noeud, role=None):
    """Les correspondances où cette occurrence figure."""
    qs = ExtremiteCorrespondance.objects.filter(noeud=noeud)
    if role is not None:
        qs = qs.filter(role=role)
    return (Correspondance.objects
            .filter(pk__in=qs.values_list('correspondance_id', flat=True))
            .prefetch_related('extremites__noeud'))


def antecedents_de(noeud_cible):
    """Les occurrences source dont cette cible procède."""
    out = []
    for corr in correspondances_de(noeud_cible, RoleExtremite.CIBLE):
        out.extend(corr.noeuds_source())
    return out


def appuis_dorigine(noeud_cible):
    """
    Les appuis de JUILLET des antécédents de cette cible.

    Identifiés comme tels : ce sont les références de la version source, pas les
    appuis du nouvel énoncé. Les confondre ferait passer pour déposé en juillet
    un paragraphe qui ne l'a pas été.
    """
    from case_manager.models import AppuiDepotJuillet
    out = []
    for ant in antecedents_de(noeud_cible):
        if ant.object_id is None:
            continue
        for a in (AppuiDepotJuillet.objects
                  .filter(statement_id=ant.object_id)
                  .select_related('entree')):
            out.append({
                'antecedent': ant,
                'appui_depot': a,
                'entree': a.entree,
                'cote_de_juillet': a.entree.cote,
                'cote_citee': a.cote_citee,
                'via_liasse': a.via_liasse,
                'origine': 'VERSION SOURCE — appui du dépôt de juillet',
            })
    return out


# ---------------------------------------------------------------------------
# Réécrire sans abîmer la source
# ---------------------------------------------------------------------------

@transaction.atomic
def detacher_pour_edition(noeud_cible, nouveau_texte, motif="réécriture"):
    """
    Donne à l'occurrence cible son propre Statement avant de la réécrire.

    TANT QUE LE PARAGRAPHE EST CONSERVÉ TEL QUEL, les deux versions partagent le
    même Statement — c'est ce qui rend la conservation lisible. Réécrire en place
    changerait donc le texte de l'acte déposé. On duplique au moment de la
    divergence, pas avant : un Statement par version dès le départ aurait fait
    perdre l'information « ce texte n'a pas bougé ».
    """
    obj = noeud_cible.content_object
    if not isinstance(obj, Statement):
        raise ValueError(
            f"Nœud {noeud_cible.pk} ne porte pas un Statement : rien à détacher.")
    if est_reproduit(noeud_cible.document):
        raise SuppressionRefusee(
            f"Nœud {noeud_cible.pk} appartient à un document REPRODUIT : son "
            f"texte ne se réécrit pas.")

    from document_manager.protection import est_referent
    partage = (LibraryNode.objects
               .filter(content_type=noeud_cible.content_type,
                       object_id=obj.pk)
               .exclude(pk=noeud_cible.pk).exists())
    doit_detacher = partage or statement_protege(obj.pk) or \
        est_referent(noeud_cible.document_id)

    if doit_detacher:
        VersionTexte.capter(obj, motif="texte source, avant détachement")
        nouveau = Statement.objects.create(
            text=nouveau_texte, is_true=obj.is_true,
            is_falsifiable=obj.is_falsifiable, is_user_created=True)
        noeud_cible.object_id = nouveau.pk
        noeud_cible.save(update_fields=['object_id'])
    else:
        obj.text = nouveau_texte
        obj.save(update_fields=['text'])
        nouveau = obj

    VersionTexte.capter(nouveau, motif=motif)
    return nouveau


# ---------------------------------------------------------------------------
# Supprimer — ce qui est permis, et à quelle condition
# ---------------------------------------------------------------------------

@transaction.atomic
def supprimer_occurrence(noeud, motif="retrait décidé"):
    """
    Supprime une occurrence PRODUCED et ses descendants, après les avoir archivés.

    VÉRIFIE LE BLOC ENTIER D'ABORD. Un bloc dont un seul descendant est protégé
    est refusé en totalité : aucune suppression partielle, pas même des nœuds
    qui auraient pu partir.

    Ce qui est conservé au passage : le document, les anciens identifiants, le
    texte, et le lien avec les correspondances — ce dont la comparaison a besoin
    pour rester lisible une fois le nœud parti.
    """
    bloc = [noeud] + list(noeud.get_descendants())

    # --- contrôle préalable du bloc entier ---
    for n in bloc:
        if est_reproduit(n.document):
            raise SuppressionRefusee(
                f"Bloc refusé : le nœud {n.pk} appartient au document REPRODUIT "
                f"« {n.document.title[:50]} ». Aucune suppression effectuée.")
        from document_manager.protection import est_referent
        if est_referent(n.document_id):
            raise SuppressionRefusee(
                f"Bloc refusé : le nœud {n.pk} appartient au référent "
                f"historique. Aucune suppression effectuée.")

    # --- archivage, puis dénouage des correspondances ---
    archives = {}
    for n in bloc:
        archives[n.pk] = archiver_noeud(n, motif=motif)
    for n in bloc:
        for e in ExtremiteCorrespondance.objects.filter(noeud=n):
            e.archive = archives[n.pk]
            e.noeud = None
            e.save(update_fields=['archive', 'noeud'])

    # --- les Statements devenus inutilisés ---
    # Un Statement encore porté par une autre occurrence reste intact ; un
    # Statement utilisé par un document REPRODUIT l'est quoi qu'il arrive.
    candidats = {n.object_id for n in bloc if n.object_id is not None
                 and n.content_type_id is not None}
    ct_statement = next((n.content_type for n in bloc
                         if n.content_type and n.content_type.model == 'statement'),
                        None)

    for n in sorted(bloc, key=lambda x: -len(x.path)):
        LibraryNode.objects.filter(pk=n.pk).delete()

    supprimes = []
    if ct_statement is not None:
        for sid in candidats:
            if statement_protege(sid):
                continue
            if LibraryNode.objects.filter(content_type=ct_statement,
                                          object_id=sid).exists():
                continue
            stmt = Statement.objects.filter(pk=sid).first()
            if stmt is None:
                continue
            if stmt.appuis_depot.exists():
                # L'énoncé est cité par le constat du dépôt : il reste.
                continue
            stmt.delete()
            supprimes.append(sid)
            for a in archives.values():
                if a.statement_pk == sid:
                    a.statement_supprime = True
                    a.save(update_fields=['statement_supprime'])

    return {'noeuds_supprimes': [n.pk for n in bloc],
            'archives': [a.pk for a in archives.values()],
            'statements_supprimes': supprimes}


def historique_de(document):
    """Les occurrences supprimées de ce document, et ce qu'elles portaient."""
    from document_manager.models import NoeudArchive
    return NoeudArchive.objects.filter(document=document).prefetch_related('extremites')
