from django.urls import path
from . import views

app_name = 'pdf_manager'

urlpatterns = [
    path('', views.pdf_document_list, name='pdf_list'),
    path('upload/', views.upload_pdf_document, name='pdf_upload'),
    
    # NEW: URLs for Detail, Update, and Delete views
    path('pdf/<int:pk>/', views.PDFDocumentDetailView.as_view(), name='pdf_detail'),
    path('pdf/<int:pk>/update/', views.PDFDocumentUpdateView.as_view(), name='pdf_update'),
    path('pdf/<int:pk>/delete/', views.PDFDocumentDeleteView.as_view(), name='pdf_delete'),
]
