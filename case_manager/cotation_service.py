"""
La cotation chronologique — une FONCTION, jamais une donnée.

Le bordereau du dépôt est immuable : ce qui est figé, c'est l'association
(modèle + pk) → cote de juillet. La cotation chronologique, elle, se recalcule
à chaque lecture : la pièce donne sa date, la date donne le rang, le rang donne
la cote. Rien n'est stocké, donc rien ne peut vieillir.

CE MODULE EXISTE POUR QU'IL N'Y AIT QU'UNE SEULE IMPLÉMENTATION. La commande
`traduire_cotes` et la vue du tableau des cotes l'appellent toutes deux. Deux
implémentations parallèles finiraient par diverger, et le dossier aurait alors
deux ordres différents pour la même preuve — celui du cahier et celui de
l'écran.

Le tri réutilise lui-même `exhibit_service.get_datetime_for_sorting`, moteur
déjà employé par `rebuild_produced_exhibits`.
"""
import datetime

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from case_manager.models import BordereauDepotJuillet
from core.mixins import ExhibitableMixin

# Un horodatage antérieur à ce plancher n'est pas une date, c'est une valeur
# sentinelle laissée par une saisie incomplète — P-83 porte 1900-01-01, ce qui
# la placerait en tête du dossier sans que rien ne le signale. Ces pièces
# rejoignent celles qui n'ont pas de date du tout : rangées en fin de tableau,
# en attente d'une date. Le jour où elle est saisie, la pièce reprend d'elle-même
# sa place — rien n'étant stocké, il suffit de relire.
PLANCHER = datetime.date(2000, 1, 1)


def horodatage(obj, nom_modele=""):
    """
    Reprise fidèle de exhibit_service.get_datetime_for_sorting, adaptée à un
    objet déjà résolu. Toute divergence ici produirait deux ordres différents
    pour la même preuve.
    """
    if obj is None:
        return None

    if isinstance(obj, ExhibitableMixin):
        dt = obj.get_exhibit_date()
        if dt and timezone.is_naive(dt):
            return timezone.make_aware(dt, timezone.get_current_timezone())
        if dt:
            return dt

    dt = None
    if nom_modele == "chatsequence":
        dt = getattr(obj, "start_date", None)
        if not dt and hasattr(obj, "messages") and obj.messages.exists():
            dt = obj.messages.order_by("timestamp").first().timestamp

    if not dt:
        dt = getattr(obj, "created_at", None)

    if dt and timezone.is_naive(dt):
        return timezone.make_aware(dt, timezone.get_current_timezone())
    return dt


def cotation_chronologique(plancher_annee=None):
    """
    Retourne la liste ordonnée `[(rang, entree, horodatage, groupe)]`.

    `groupe` vaut 'datee', 'a_dater' ou 'atemporelle'. Les trois blocs se
    suivent dans cet ordre : les pièces datées, puis celles dont la date
    manque et s'ajoutera, puis celles qui n'en auront jamais par nature.

    La distinction entre les deux derniers groupes n'est pas cosmétique : une
    pièce « à dater » appelle une correction, une pièce atemporelle n'en
    appelle aucune. Les confondre ferait porter au tableau une dette qui
    n'existe pas.
    """
    annee = plancher_annee if plancher_annee is not None else PLANCHER.year
    cts = {ct.id: ct for ct in ContentType.objects.all()}

    # `prefetch_related('content_object')` sait résoudre une clé générique en
    # une requête par modèle. Sans lui, chaque ligne du registre en coûte une :
    # 356 requêtes pour 334 pièces, et la facture croît avec le dossier.
    datees, sans_date, atemporelles = [], [], []
    for e in BordereauDepotJuillet.objects.prefetch_related('content_object'):
        if e.atemporel:
            atemporelles.append(e)
            continue
        ct = cts.get(e.content_type_id)
        dt = horodatage(e.content_object, ct.model if ct else "")
        if dt is None or dt.year < annee:
            sans_date.append(e)
        else:
            datees.append((dt, e))

    # Départage — type puis PK — seulement à horodatage strictement égal. Il est
    # déterministe : deux lectures donnent la même cotation.
    datees.sort(key=lambda t: (t[0], t[1].source_type, t[1].object_id or 0))

    def _cle(e):
        # `rang` est NULL pour une pièce versée après le dépôt : elle se range
        # après les autres plutôt que de faire échouer la comparaison.
        return (e.rang is None, e.rang or 0, e.sous_rang or 0)

    sans_date.sort(key=_cle)
    atemporelles.sort(key=_cle)

    ordre = ([(dt, e, 'datee') for dt, e in datees]
             + [(None, e, 'a_dater') for e in sans_date]
             + [(None, e, 'atemporelle') for e in atemporelles])

    return [(i, e, dt, g) for i, (dt, e, g) in enumerate(ordre, start=1)]


def axes_par_piece():
    """
    `{(content_type_id, object_id): [{axe, role, fait}, …]}`

    Une pièce n'appartient pas à un axe : elle y joue un RÔLE, au soutien d'un
    FAIT précis. Le tableau doit porter cette information, faute de quoi il
    présenterait côte à côte une ATTESTATION datée et une ILLUSTRATION sans
    valeur probante propre — en aplatissant justement la distinction que
    `RoleAppui` existe pour préserver.
    """
    from argument_manager.models import AppuiFait

    index = {}
    appuis = (AppuiFait.objects
              .select_related('fait', 'content_type')
              .prefetch_related('fait__axes'))
    for ap in appuis:
        cle = (ap.content_type_id, ap.object_id)
        for axe in ap.fait.axes.all():
            index.setdefault(cle, []).append({
                'axe': axe,
                'role': ap.role,
                'role_libelle': ap.get_role_display(),
                'fait': ap.fait,
                'note': ap.note,
            })
    return index
