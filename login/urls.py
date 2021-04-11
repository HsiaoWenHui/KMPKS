from django.urls import path
from django.conf.urls import include
from django.contrib.auth import views
from home import views as h
from login.views import logout,register,login,change_password
urlpatterns = [
    path('login/',login),
    path('logout/', logout),
    path('registration/', register),
    path('password/',change_password),
    path('accounts/profile/',h.home )
]