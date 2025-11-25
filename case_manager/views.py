from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import LegalCase, PerjuryContestation
from .forms import LegalCaseForm, PerjuryContestationForm

# --- LegalCase Views ---

class LegalCaseListView(ListView):
    model = LegalCase
    template_name = 'case_manager/legalcase_list.html'
    context_object_name = 'cases'
    ordering = ['-created_at']

class LegalCaseDetailView(DetailView):
    model = LegalCase
    template_name = 'case_manager/legalcase_detail.html'
    context_object_name = 'case'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contestations'] = self.object.contestations.all()
        return context

class LegalCaseCreateView(CreateView):
    model = LegalCase
    form_class = LegalCaseForm
    template_name = 'case_manager/legalcase_form.html'
    
    def get_success_url(self):
        return reverse_lazy('case_manager:case_detail', kwargs={'pk': self.object.pk})

# --- PerjuryContestation Views ---

class PerjuryContestationCreateView(CreateView):
    model = PerjuryContestation
    form_class = PerjuryContestationForm
    template_name = 'case_manager/perjurycontestation_form.html'

    def form_valid(self, form):
        # Assign the contestation to the current case from the URL
        form.instance.case = LegalCase.objects.get(pk=self.kwargs['case_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect back to the case detail page
        return reverse_lazy('case_manager:case_detail', kwargs={'pk': self.kwargs['case_pk']})

class PerjuryContestationDetailView(DetailView):
    model = PerjuryContestation
    template_name = 'case_manager/perjurycontestation_detail.html'
    context_object_name = 'contestation'
    # We will build this out later.
