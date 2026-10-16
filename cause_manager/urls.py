from django.urls import path

from . import views

app_name = 'cause_manager'
urlpatterns = [
    path('', views.CauseListView.as_view(), name='list'),
    path('nouvelle/', views.CauseCreateView.as_view(), name='create'),
    path('<int:pk>/', views.CauseDetailView.as_view(), name='detail'),
    path('<int:pk>/modifier/', views.CauseUpdateView.as_view(), name='update'),
    path('<int:pk>/etat/', views.ConsignerEtatView.as_view(), name='etat'),
    path('<int:pk>/lier/', views.LierCauseView.as_view(), name='lier'),
]
