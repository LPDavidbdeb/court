from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import CauseForm, EtatCauseForm, LienCauseForm
from .models import Cause


class AccesCausesMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class CauseListView(AccesCausesMixin, ListView):
    queryset = Cause.objects.prefetch_related('etats')
    template_name = 'cause_manager/list.html'
    context_object_name = 'causes'
    paginate_by = 30


class CauseCreateView(AccesCausesMixin, CreateView):
    model = Cause
    form_class = CauseForm
    template_name = 'cause_manager/form.html'


class CauseUpdateView(AccesCausesMixin, UpdateView):
    model = Cause
    form_class = CauseForm
    template_name = 'cause_manager/form.html'


def contexte_cause(cause, request, **forms):
    return {
        'cause': cause,
        'documents': cause.documents_origine.order_by('document_original_date', 'pk'),
        'courriels': Paginator(
            cause.courriels_origine.order_by('date_sent', 'pk'), 30,
        ).get_page(request.GET.get('page')),
        'liens_sortants': cause.liens_sortants.select_related('cause_liee'),
        'liens_entrants': cause.liens_entrants.select_related('cause'),
        'etat_form': forms.get('etat_form', EtatCauseForm()),
        'lien_form': forms.get('lien_form', LienCauseForm(cause=cause)),
    }


class CauseDetailView(AccesCausesMixin, DetailView):
    queryset = Cause.objects.prefetch_related('etats')
    template_name = 'cause_manager/detail.html'

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs), **contexte_cause(self.object, self.request)}


class ConsignerEtatView(AccesCausesMixin, View):
    def post(self, request, pk):
        cause = get_object_or_404(Cause, pk=pk)
        form = EtatCauseForm(request.POST)
        if form.is_valid():
            cause.consigner_etat(**form.cleaned_data)
            return redirect(cause)
        return render(request, 'cause_manager/detail.html',
                      contexte_cause(cause, request, etat_form=form), status=400)


class LierCauseView(AccesCausesMixin, View):
    def post(self, request, pk):
        cause = get_object_or_404(Cause, pk=pk)
        form = LienCauseForm(request.POST, cause=cause)
        if form.is_valid():
            form.save()
            return redirect(cause)
        return render(request, 'cause_manager/detail.html',
                      contexte_cause(cause, request, lien_form=form), status=400)
