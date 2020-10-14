from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from group import views
urlpatterns = [

  path('',views.allGroup),
  path('mygroups/',views.mygroups),
  path('add/',views.addGroup),
  path('search/',views.search),
  url(r'^(\d+)/search/$',views.article_search),
  url(r'^(\d+)/dashboard/$',views.dashboard),
  url(r'^(?P<group_id>[^/]+)/$',views.groupIndex),
  url(r'^(\d+)/remove/$',views.removeGroup),
  url(r'^(\d+)/edit/$',views.editGroup),
  url(r'^(\d+)/join/$',views.joinGroup),
  url(r'^(\d+)/(\d+)/addMember/$',views.addMember),
  url(r'^(\d+)/(\d+)/leaveGroup/$',views.leaveGroup),
  url(r'^(\d+)/(\d+)/delArticle/$',views.delArticle),
  url(r'^(\d+)/cancel/$',views.cancelGroup),
  # url(r'^(\d+)/allmembers/$',views.allmembers),
  url(r'^(\d+)/edit/addCategory/$',views.addCategory),
  url(r'^(\d+)/edit/updateCategory/$',views.updateCategory),
  url(r'^(\d+)/(\d+)/delCategory/$',views.delCategory),
  url(r'^(\d+)/(\d+)/category/$',views.categories),
  # url(r'^(\d+)/(\d+)/chat/$',views.chat),
  # url(r'^ws/chat/$',views.chat),
  # url(r'^chat/(?P<group_id>[^/]+)/$',views.chat),
]