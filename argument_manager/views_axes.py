"""
Création, modification et suppression des axes d'argumentation.

Jusqu'ici les axes n'existaient que par des commandes de gestion
(`axe_danse`, `axe_soccer_2013`). C'était tenable à deux axes ; ça ne l'est
plus dès qu'on trie un registre de 334 pièces et qu'il faut ouvrir une
dimension en cours de lecture.

CE QUE CES VUES NE FONT PAS. Elles ne créent ni faits ni appuis. Un axe se crée
vide : c'est un contenant nommé, qui vise éventuellement des allégations. Les
faits s'y ajoutent ensuite, et les pièces s'y rattachent depuis leur vue de
détail. Mêler les trois dans un seul formulaire redonnerait le fourre-tout que
`TrameNarrative` était devenu.
"""
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from argument_manager.forms_axes import AxeForm
from argument_manager.models import AppuiFait, Axe, Fait, RattachementAxe


def _inventaire(axe):
    """Ce que la suppression de cet axe emporterait."""
    faits = list(axe.faits.all())
    appuis = AppuiFait.objects.filter(fait__axes=axe).count()
    rattachements = RattachementAxe.objects.filter(axe=axe).count()
    # Un fait rattaché à plusieurs axes SURVIT à la suppression de celui-ci ;
    # seul un fait dont c'est le dernier axe deviendrait orphelin.
    orphelins = [f for f in faits if f.axes.count() <= 1]
    return {
        'faits': len(faits),
        'faits_orphelins': len(orphelins),
        'appuis': appuis,
        'rattachements': rattachements,
        'cibles': axe.cibles.count(),
    }


def liste_axes(request):
    axes = []
    for axe in Axe.objects.annotate(n_faits=Count('faits', distinct=True)).order_by('nom'):
        axes.append({
            'axe': axe,
            'faits': axe.n_faits,
            'appuis': AppuiFait.objects.filter(fait__axes=axe).count(),
            'rattachements': RattachementAxe.objects.filter(axe=axe).count(),
            'cibles': axe.cibles.count(),
            'plaides': axe.faits.exclude(statement=None).count(),
        })
    return render(request, 'argument_manager/axes_liste.html', {
        'axes': axes,
        'total_faits': Fait.objects.count(),
    })


def creer_axe(request):
    form = AxeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        axe = form.save()
        messages.success(
            request,
            f"Axe « {axe.nom} » créé. Il est vide : ajoutez-lui des faits, puis "
            f"rattachez-lui des pièces depuis leur vue de détail.")
        return redirect(reverse('argument_manager:axes_liste'))
    return render(request, 'argument_manager/axe_form.html', {
        'form': form, 'axe': None,
    })


def modifier_axe(request, pk):
    axe = get_object_or_404(Axe, pk=pk)
    form = AxeForm(request.POST or None, instance=axe)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f"Axe « {axe.nom} » mis à jour.")
        return redirect(reverse('argument_manager:axes_liste'))
    return render(request, 'argument_manager/axe_form.html', {
        'form': form, 'axe': axe, 'inventaire': _inventaire(axe),
    })


@require_POST
def supprimer_axe(request, pk):
    """
    Supprime un axe — après confirmation explicite du nom.

    La cascade emporte les rattachements de triage et détache les faits. Un
    fait servant un autre axe survit ; un fait dont c'était le seul axe
    deviendrait orphelin, et ses appuis avec lui. La page de modification
    affiche ce décompte avant que le bouton n'apparaisse.
    """
    axe = get_object_or_404(Axe, pk=pk)
    if (request.POST.get('confirmation') or '').strip() != axe.nom:
        messages.error(
            request,
            "Suppression annulée : le nom saisi ne correspond pas à l'axe.")
        return redirect(reverse('argument_manager:axe_modifier', kwargs={'pk': pk}))

    inv = _inventaire(axe)
    nom = axe.nom
    axe.delete()
    messages.warning(
        request,
        f"Axe « {nom} » supprimé — {inv['rattachements']} rattachement(s) de "
        f"triage emportés, {inv['faits']} fait(s) détaché(s) dont "
        f"{inv['faits_orphelins']} sans autre axe.")
    return redirect(reverse('argument_manager:axes_liste'))
