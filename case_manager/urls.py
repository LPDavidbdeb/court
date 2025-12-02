from django.urls import path
from . import views

app_name = 'case_manager'

urlpatterns = [
    # LegalCase URLs
    path('', views.LegalCaseListView.as_view(), name='case_list'),
    path('create/', views.LegalCaseCreateView.as_view(), name='case_create'),
    path('<int:pk>/', views.LegalCaseDetailView.as_view(), name='case_detail'),
    path('cases/<int:pk>/export/', views.LegalCaseExportView.as_view(), name='case_export'),
    path('cases/<int:pk>/export-police/', views.PoliceComplaintExportView.as_view(), name='case_export_police'),

    # PerjuryContestation URLs
    path('<int:case_pk>/contestations/create/', views.PerjuryContestationCreateView.as_view(), name='contestation_create'),
    path('contestations/<int:pk>/', views.PerjuryContestationDetailView.as_view(), name='contestation_detail'),
    path('contestations/<int:pk>/update-title/', views.update_contestation_title_ajax, name='update_contestation_title'),
    path('contestations/<int:pk>/manage-narratives/', views.ManageContestationNarrativesView.as_view(), name='manage_narratives'),
    path('contestations/<int:pk>/manage-statements/', views.ManageContestationStatementsView.as_view(), name='manage_statements'),
    
    # AI Suggestion and Debugging URLs
    path('contestations/<int:contestation_pk>/generate-suggestion/', views.generate_ai_suggestion, name='generate_suggestion'),
    path('contestation/<int:contestation_pk>/gen-police/', views.generate_police_report, name='gen_police_report'),
    path('contestations/<int:contestation_pk>/preview/', views.preview_ai_context, name='preview_context'),
    path('suggestions/<int:suggestion_pk>/retry-parse/', views.retry_parse_suggestion, name='retry_parse_suggestion'),
]
