from django.urls import path
from . import views

app_name = 'argument_manager'

urlpatterns = [
    path('', views.TrameNarrativeListView.as_view(), name='list'),
    path('<int:pk>/', views.TrameNarrativeDetailView.as_view(), name='detail'),
    path('create/', views.TrameNarrativeCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.TrameNarrativeUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.TrameNarrativeDeleteView.as_view(), name='delete'),

    # Email Quote Workflow
    path('ajax/search-emails/', views.ajax_search_emails, name='ajax_search_emails'),
    path('<int:narrative_pk>/ajax/add-email-quote/', views.ajax_add_email_quote, name='ajax_add_email_quote'),

    # Event Selection Workflow
    path('ajax/get-events-list/', views.ajax_get_events_list, name='ajax_get_events_list'),
    # ADDED: URL for updating events from the detail view
    path('<int:narrative_pk>/ajax_update_events/', views.ajax_update_narrative_events, name='ajax_update_narrative_events'),
]
