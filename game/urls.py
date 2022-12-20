from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
   path('',views.homegame,name='homegame'),
   path('gamestarted',views.gamestarted,name='gamestarted')
]
