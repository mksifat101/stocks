from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/',views.LoginPage,name="login"),
    path('logout/',views.LogoutUser,name="logout"),
    #path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html')),
    #path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html')),
]   