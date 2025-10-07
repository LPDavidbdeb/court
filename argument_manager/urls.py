from django.urls import path
from . import views

app_name = 'argument_manager'

urlpatterns = [
    path('', views.TrameNarrativeListView.as_view(), name='list'),
    path('<int:pk>/', views.TrameNarrativeDetailView.as_view(), name='detail'),
    path('create/', views.TrameNarrativeCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.TrameNarrativeUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.TrameNarrativeDeleteView.as_view(), name='delete'),
    path('<int:narrative_pk>/ajax_update_summary/', views.ajax_update_summary, name='ajax_update_summary'),

    # Email Quote Workflow
    path('<int:narrative_pk>/ajax/add-email-quote/', views.ajax_add_email_quote, name='ajax_add_email_quote'),
    path('ajax/get-email-quotes-list/', views.ajax_get_email_quotes_list, name='ajax_get_email_quotes_list'),
    path('<int:narrative_pk>/ajax_update_email_quotes/', views.ajax_update_narrative_email_quotes, name='ajax_update_narrative_email_quotes'),
    path('ajax/get-email-threads/', views.ajax_get_email_threads, name='ajax_get_email_threads'),
    path('ajax/get-thread-emails/<int:thread_pk>/', views.ajax_get_thread_emails, name='ajax_get_thread_emails'),

    # Event Selection Workflow
    path('ajax/get-events-list/', views.ajax_get_events_list, name='ajax_get_events_list'),
    path('<int:narrative_pk>/ajax_update_events/', views.ajax_update_narrative_events, name='ajax_update_narrative_events'),
]
