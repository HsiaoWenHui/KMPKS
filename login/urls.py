from django.urls import path
from django.conf.urls import include
from django.contrib.auth import views
from home import views as h
from login.views import logout,register,login
urlpatterns = [
    path('login/',login),
    path('logout/', logout),
    path('registration/', register),
    path('accounts/profile/',h.home )
]