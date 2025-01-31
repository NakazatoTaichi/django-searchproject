from django.urls import path
from . import views

app_name = 'mycollection'

urlpatterns = [
    path('home', views.collection_home, name='home'),
]