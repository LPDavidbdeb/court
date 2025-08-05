from django.urls import path
from .views import email_namager_view, email_manager_1

app_name = 'email_manager'

urlpatterns = [
    # path('search/', email_manager_1.email_search_view, name='email_search'),
    path('search/', email_namager_view.email_search_view, name='email_search'),
    path('save_email/', email_namager_view.save_email_view, name='save_email'),
    path('email/<int:pk>/', email_namager_view.email_detail_view, name='email_detail'),
    path('emails/', email_namager_view.email_list_view, name='email_list'),
    path('/email/<int:pk>/delete/', email_namager_view.email_delete_view, name='email_delete'),
    path('upload_eml/', email_namager_view.upload_eml_view, name='upload_eml'),
]