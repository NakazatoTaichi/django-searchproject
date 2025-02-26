from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_runserver(request):
    return redirect('accounts:login')

urlpatterns = [
    path('', redirect_to_runserver),
    path('admin/', admin.site.urls),
    path('mycollection/', include('mycollection.urls')),
    path('search/', include('search_app.urls')),
    path('', include('accounts.urls')),
]