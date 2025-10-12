import os
from django.db.models import Min
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView, FormView, DeleteView, View
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from ..models import EmailThread
from ..forms import EmailAjaxSearchForm, QuoteForm
from ..utils import search_gmail, save_gmail_thread


class EmailThreadListView(ListView):
    model = EmailThread
    template_name = 'email_manager/thread/list.html'
    context_object_name = 'threads'

    def get_queryset(self):
        return EmailThread.objects.annotate(
            start_date=Min('emails__date_sent')
        ).order_by('-start_date')


class EmailThreadDetailView(DetailView):
    model = EmailThread
    template_name = 'email_manager/thread/detail.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thread = self.get_object()
        context['emails_in_thread'] = thread.emails.all().order_by('date_sent')
        context['form'] = QuoteForm()
        return context


class EmailSearchView(FormView):
    template_name = 'email_manager/thread/search.html'
    form_class = EmailAjaxSearchForm
    success_url = reverse_lazy('email_manager:thread_list')

    def form_valid(self, form):
        try:
            search_results = search_gmail(form.cleaned_data)
        except Exception as e:
            messages.error(self.request, f"An error occurred during the search: {e}")
            search_results = {'status': 'error', 'message': str(e)}

        context = self.get_context_data(form=form, search_results=search_results)
        
        if search_results.get('status') == 'success':
            context['selected_protagonist'] = search_results.get('selected_protagonist')

        return self.render_to_response(context)


class EmailThreadDeleteView(DeleteView):
    model = EmailThread
    success_url = reverse_lazy('email_manager:thread_list')

    def form_valid(self, form):
        thread = self.get_object()
        thread_subject = thread.subject
        for email_record in thread.emails.all():
            if email_record.eml_file_path and os.path.exists(email_record.eml_file_path):
                try:
                    os.remove(email_record.eml_file_path)
                except OSError as e:
                    messages.warning(self.request, f"Failed to delete EML file {email_record.eml_file_path}: {e}")

        response = super().form_valid(form)
        messages.success(self.request, f"Thread '{thread_subject}' and all its messages deleted successfully.")
        return response

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class EmailThreadSaveView(View):
    def post(self, request, *args, **kwargs):
        thread_id = request.POST.get('thread_id')
        protagonist_id = request.POST.get('protagonist_id')

        try:
            new_thread = save_gmail_thread(thread_id, protagonist_id)
            messages.success(request, f"Successfully saved thread '{new_thread.subject}'.")
            return redirect('email_manager:thread_detail', pk=new_thread.pk)
        except Exception as e:
            messages.error(request, f"An error occurred while saving the thread: {e}")
            return HttpResponseRedirect(reverse('email_manager:thread_search'))
