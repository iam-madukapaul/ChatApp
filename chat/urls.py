from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='login'),
    path('<str:room_name>/<str:username>/', views.room, name='room'),
]