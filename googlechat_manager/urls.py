from django.urls import path
from . import views

app_name = 'googlechat'

urlpatterns = [
    # The main, single-page chat stream view
    path('stream/', views.single_chat_stream, name='chat_stream'),
    
    # API endpoint for loading older messages via AJAX
    path('api/load_more_messages/', views.load_more_messages, name='load_more_messages'),
]