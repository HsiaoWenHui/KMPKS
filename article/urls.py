from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from article import views

urlpatterns = [
  # url(r'^(\d+)/$',views.articleIndex),
  path('all/',views.all),
  url(r'^(\d+)/$',views.articleIndex),
  # url(r'^content/(\d+)/$',views.articleView.as_view()),
  url(r'^(\d+)/edit/$',views.editArticle),
  url(r'^(\d+)/remove/$',views.removeArticle),
  path('add/',views.addArticle),
  # path('test/',views.test),
  url(r'^tags/(\d+)/$',views.tags),
  url(r'^category/(\d+)/$',views.categories),
  url(r'^(\d+)/(\d+)/delete/$',views.del_comment),
  url(r'^search/$',views.search),
]
