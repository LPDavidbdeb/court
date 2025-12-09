from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('story/<int:pk>/', views.story_scrollytelling_view, name='story_detail'),
    path('histoire/cinematique/<int:pk>/', views.story_cinematic_view, name='story_cinematic'),
]