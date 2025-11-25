from django.urls import path
from . import views

app_name = 'case_manager'

urlpatterns = [
    # LegalCase URLs
    path('', views.LegalCaseListView.as_view(), name='case_list'),
    path('create/', views.LegalCaseCreateView.as_view(), name='case_create'),
    path('<int:pk>/', views.LegalCaseDetailView.as_view(), name='case_detail'),

    # PerjuryContestation URLs
    path('<int:case_pk>/contestations/create/', views.PerjuryContestationCreateView.as_view(), name='contestation_create'),
    path('contestations/<int:pk>/', views.PerjuryContestationDetailView.as_view(), name='contestation_detail'),
    
    # AI Suggestion URL
    path('contestations/<int:contestation_pk>/generate-suggestion/', views.generate_ai_suggestion, name='generate_suggestion'),
]
