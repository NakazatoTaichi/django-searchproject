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
    path('tag/register', views.collection_tag_register, name='collection_tag_register'),
    path('favorites', views.collection_favorites, name='collection_favorites'),
    path('add_favorite', views.collection_add_favorite, name='collection_add_favorite'),
    path('remove_favorite', views.collection_remove_favorite, name='collection_remove_favorite'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)