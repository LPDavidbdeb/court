from django.urls import path
from . import views

app_name = 'pdf_manager'

urlpatterns = [
    path('', views.pdf_document_list, name='pdf_list'),
    path('upload/', views.upload_pdf_document, name='pdf_upload'),
    path('pdf/<int:pk>/', views.PDFDocumentDetailView.as_view(), name='pdf_detail'),
    path('pdf/<int:pk>/update/', views.PDFDocumentUpdateView.as_view(), name='pdf_update'),
    path('pdf/<int:pk>/delete/', views.PDFDocumentDeleteView.as_view(), name='pdf_delete'),

    # AJAX URLs
    path('author-search/', views.author_search_view, name='author_search'),
    path('add-protagonist/', views.add_protagonist_view, name='add_protagonist'),
]
