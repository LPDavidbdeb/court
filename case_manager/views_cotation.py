"""
Le tableau des cotes — registre complet, ordonné chronologiquement, filtrable
par axe d'argumentation.

La page réunit deux systèmes de cotation qui coexistent volontairement :

  COTE DE JUILLET      immuable. Elle a été déposée. Une pièce versée depuis
                       n'en a pas, et n'en aura jamais.
  COTE CHRONOLOGIQUE   recalculée à chaque affichage par `cotation_service`.
                       Elle bouge quand une pièce est ajoutée ou datée — c'est
                       voulu : elle est une fonction du contenu.

Le tableau est donc aussi le TRADUCTEUR entre les deux, et c'est sa raison
d'être principale : un paragraphe déposé cite « P-74.5 », le travail courant
manipule la cote chronologique, et il faut pouvoir passer de l'un à l'autre
sans reconstruire quoi que ce soit.
"""


from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from argument_manager.models import AppuiFait, Axe, Fait, RoleAppui
from argument_manager.axes_service import axes_par_piece_union
from case_manager.cotation_service import cotation_chronologique
from case_manager.models import BordereauDepotJuillet


def _url_piece(obj):
    """
    L'adresse de TRAVAIL de la pièce, si le modèle en expose une.

    ⚠️ `get_absolute_url` d'abord, `get_public_url` seulement à défaut — et
    l'ordre est porteur. Trois modèles distinguent les deux : `PDFDocument`,
    `Email` et `Document` renvoient par `get_public_url` vers une vue publique
    de PARTAGE, exemptée du contrôle superutilisateur et dépourvue de tout
    outil d'édition. Le tableau des cotes est un outil de travail : il doit
    mener là où l'on peut rattacher la pièce à un axe, pas là où on la montre
    à un tiers.
    """
    if obj is None:
        return None
    for methode in ('get_absolute_url', 'get_public_url'):
        f = getattr(obj, methode, None)
        if callable(f):
            try:
                return f()
            except Exception:
                continue
    return None


def _description(entree, obj):
    """
    Ce que le bordereau dit de la pièce, à défaut ce que la pièce dit d'elle.

    La colonne du bordereau est privilégiée : c'est le libellé DÉPOSÉ. Une
    pièce versée depuis n'en a pas, et se décrit alors par son propre modèle.
    """
    if (entree.description or '').strip():
        return entree.description.strip()
    if obj is not None:
        for methode in ('get_exhibit_description', 'get_exhibit_title'):
            f = getattr(obj, methode, None)
            if callable(f):
                try:
                    v = (f() or '').strip()
                    if v:
                        return v
                except Exception:
                    continue
        return str(obj)[:200]
    return '—'


def tableau_cotes(request):
    axe_id = request.GET.get('axe') or ''
    role = request.GET.get('role') or ''

    # L'union du triage (cases cochées) et des appuis précis. Filtrer sur le
    # seul AppuiFait masquerait tout le travail de triage; ne montrer que le
    # triage effacerait le rôle probatoire. Le tableau doit porter les deux et
    # les distinguer.
    index = axes_par_piece_union()
    cts = {ct.id: ct for ct in ContentType.objects.all()}

    lignes = []
    for rang, entree, dt, groupe in cotation_chronologique():
        cle = (entree.content_type_id, entree.object_id)
        rattachements = index.get(cle, [])
        obj = entree.content_object
        ct = cts.get(entree.content_type_id)
        lignes.append({
            'registre_pk': entree.pk,
            'rang': rang,
            'cote_chrono': f"P-{rang}",
            'cote_juillet': entree.cote,
            'groupe': groupe,
            'date': dt,
            'date_libelle': entree.date_libelle,
            'type': entree.source_type or (ct.model if ct else ''),
            'reference': f"{ct.model}-{entree.object_id}" if ct else '',
            'description': _description(entree, obj),
            'url': _url_piece(obj),
            'resolu': entree.resolu,
            'atemporel': entree.atemporel,
            'rattachements': rattachements,
            'axes_ids': {r['axe'].pk for r in rattachements},
            'roles': {r['role'] for r in rattachements},
        })

    # --- filtrage ------------------------------------------------------
    # Le filtre RESTREINT l'affichage; il ne renumérote rien. La cote
    # chronologique d'une pièce ne dépend pas du filtre appliqué, sans quoi
    # deux vues de la même page donneraient deux cotes à la même pièce.
    total = len(lignes)
    if axe_id.isdigit():
        lignes = [l for l in lignes if int(axe_id) in l['axes_ids']]
    if role:
        lignes = [l for l in lignes if role in l['roles']]

    axes = []
    for axe in Axe.objects.all().order_by('nom'):
        n = sum(1 for c, r in index.items() if any(x['axe'].pk == axe.pk for x in r))
        axes.append({'axe': axe, 'nombre': n})

    roles = []
    for valeur, libelle in RoleAppui.choices:
        n = sum(1 for l_ in lignes if valeur in l_['roles'])
        roles.append({'valeur': valeur, 'libelle': libelle, 'nombre': n})

    # Catalogue des faits, servi au navigateur pour que le choix du fait se
    # restreigne à l'axe retenu sans aller-retour au serveur. Une douzaine
    # d'entrées : le coût est nul et l'interface reste immédiate.
    catalogue = [{
        'pk': f.pk,
        'ordre': f.ordre,
        'enonce': f.enonce,
        'nature': f.nature,
        'axes': [a.pk for a in f.axes.all()],
    } for f in Fait.objects.prefetch_related('axes').order_by('ordre')]

    contexte = {
        'lignes': lignes,
        'total': total,
        'affichees': len(lignes),
        'axes': axes,
        'roles': roles,
        'axe_actif': axe_id,
        'role_actif': role,
        'rattachees': sum(1 for l_ in lignes if l_['rattachements']),
        'sans_cote_juillet': sum(1 for l_ in lignes if not l_['cote_juillet']),
        'a_dater': sum(1 for l_ in lignes if l_['groupe'] == 'a_dater'),
        'atemporelles': sum(1 for l_ in lignes if l_['groupe'] == 'atemporelle'),
        # Passé brut : le gabarit l'embarque avec `json_script`, qui échappe
        # correctement. Un `json.dumps` rendu avec `|safe` casserait dès qu'un
        # énoncé de fait contiendrait « </script> » — texte saisi à la main,
        # donc l'hypothèse n'est pas théorique.
        'catalogue_faits': catalogue,
        'roles_choix': RoleAppui.choices,
    }
    return render(request, 'case_manager/tableau_cotes.html', contexte)


# ---------------------------------------------------------------------------
# Rattachement d'une pièce à un axe
#
# UNE PIÈCE NE S'ASSOCIE PAS À UN AXE — elle joue un RÔLE au soutien d'un FAIT
# précis, et le fait appartient à un ou plusieurs axes. Trois raisons de ne pas
# raccourcir :
#
#   1. Une même pièce peut servir deux faits pour des motifs différents. La
#      rattacher « à l'axe » perdrait lequel.
#   2. Le rôle détermine ce qu'on peut lui faire dire. Un horaire de 2026 versé
#      pour éclairer la forme d'une saison ne prouve pas le calendrier de 2013 :
#      le déclarer ILLUSTRATION empêche l'assemblage de lui faire porter un fait
#      qu'il ne porte pas.
#   3. C'est exactement ce que `TrameNarrative` faisait — collecter des preuves
#      autour d'un argument sans les qualifier — et la raison pour laquelle elle
#      a été remplacée.
# ---------------------------------------------------------------------------

def _piece_du_registre(registre_pk):
    """La ligne de registre visée, ou None."""
    return BordereauDepotJuillet.objects.filter(pk=registre_pk).first()


@require_POST
def rattacher_piece(request):
    """Crée un AppuiFait reliant une pièce du registre à un fait."""
    registre_pk = request.POST.get('registre_pk')
    fait_pk = request.POST.get('fait_pk')
    role = request.POST.get('role') or RoleAppui.ATTESTATION
    note = (request.POST.get('note') or '').strip()

    entree = _piece_du_registre(registre_pk)
    fait = Fait.objects.filter(pk=fait_pk).first()
    if entree is None or fait is None:
        return JsonResponse({'ok': False,
                             'erreur': "Pièce ou fait introuvable."}, status=404)
    if role not in dict(RoleAppui.choices):
        return JsonResponse({'ok': False,
                             'erreur': f"Rôle inconnu : {role}"}, status=400)

    try:
        with transaction.atomic():
            appui = AppuiFait.objects.create(
                fait=fait,
                ordre=(fait.appuis.count() + 1),
                content_type_id=entree.content_type_id,
                object_id=entree.object_id,
                role=role,
                note=note,
            )
    except IntegrityError:
        # `appui_unique_par_fait` : la même pièce ne peut soutenir deux fois le
        # même fait. Ce n'est pas une erreur de l'utilisateur, c'est un doublon.
        return JsonResponse(
            {'ok': False,
             'erreur': "Cette pièce soutient déjà ce fait."}, status=409)

    return JsonResponse({
        'ok': True,
        'appui_pk': appui.pk,
        'role': appui.role,
        'fait_ordre': fait.ordre,
        'axes': [{'pk': a.pk, 'nom': a.nom} for a in fait.axes.all()],
    })


@require_POST
def detacher_piece(request):
    """Supprime un AppuiFait. Ne touche ni à la pièce ni au registre."""
    appui = AppuiFait.objects.filter(pk=request.POST.get('appui_pk')).first()
    if appui is None:
        return JsonResponse({'ok': False,
                             'erreur': "Rattachement introuvable."}, status=404)
    appui.delete()
    return JsonResponse({'ok': True})


def rattachements_piece(request, registre_pk):
    """Les rattachements actuels d'une pièce — sert à peupler le panneau."""
    entree = _piece_du_registre(registre_pk)
    if entree is None:
        return JsonResponse({'ok': False, 'erreur': "Pièce introuvable."},
                            status=404)
    appuis = (AppuiFait.objects
              .filter(content_type_id=entree.content_type_id,
                      object_id=entree.object_id)
              .select_related('fait')
              .prefetch_related('fait__axes'))
    return JsonResponse({
        'ok': True,
        'cote': entree.cote,
        'description': entree.description,
        'rattachements': [{
            'appui_pk': ap.pk,
            'role': ap.role,
            'role_libelle': ap.get_role_display(),
            'note': ap.note,
            'fait_pk': ap.fait_id,
            'fait_ordre': ap.fait.ordre,
            'fait_enonce': ap.fait.enonce,
            'axes': [a.nom for a in ap.fait.axes.all()],
        } for ap in appuis],
    })
