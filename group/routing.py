from django.urls import re_path
from group import consumers
from django.conf.urls import url
websocket_urlpatterns = [
  url(r'^ws/group/(?P<group_id>[^/]+)/$', consumers.ChatConsumer),
]