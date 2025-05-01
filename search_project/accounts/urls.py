from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import SignUpView
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import CustomLoginView


app_name = 'accounts'

urlpatterns = [
    path('signup', SignUpView.as_view(), name="signup"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='accounts:login'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)