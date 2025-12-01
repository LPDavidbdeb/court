from django.urls import path
from . import views

app_name = 'googlechat'

urlpatterns = [
    path('stream/', views.single_chat_stream, name='chat_stream'),
    path('api/load_more_messages/', views.load_more_messages, name='load_more_messages'),
    
    # New CRUD URLs for Chat Sequences
    path('sequences/', views.chat_sequence_list, name='sequence_list'),
    path('api/create_sequence/', views.create_sequence_ajax, name='create_sequence_ajax'),
    path('sequences/<int:pk>/delete/', views.delete_sequence, name='delete_sequence'),
]