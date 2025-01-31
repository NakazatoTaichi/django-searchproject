from django.urls import path
from . import views

app_name = 'my_collection'

urlpatterns = [
    path('home/', views.collection_home, name='home'),
]