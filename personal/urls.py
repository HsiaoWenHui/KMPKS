from django.urls import path
from django.conf.urls import include
from personal import views
from django.conf.urls import url
urlpatterns = [
  # path('',views.personalIndex),
  path('editProfile/',views.editProfile),
  url(r'^(\d+)/$',views.personalIndex)
]