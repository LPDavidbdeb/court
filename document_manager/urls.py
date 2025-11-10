from django.urls import path
from . import views

app_name = 'document_manager'

urlpatterns = [
    path('list/', views.document_list_view, name='document_list'),
    path('document/<int:pk>/', views.document_detail_view, name='document_detail'),
    path('clean/<int:pk>/', views.clean_detail_view, name='clean_detail'),
    path('interactive/<int:pk>/', views.interactive_detail_view, name='interactive_detail'),
    path('perjury-elements/', views.PerjuryElementListView.as_view(), name='perjury_element_list'),
]
