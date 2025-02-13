from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'mycollection'

urlpatterns = [
    path('home', views.collection_home, name='home'),
    path('register', views.collection_register, name='collection_register'),
    path('edit/<int:pk>', views.collection_edit, name='collection_edit'),
    path('delete/<int:pk>', views.collection_delete, name='collection_delete'),
    path('category/register', views.collection_category_register, name='collection_category_register'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)