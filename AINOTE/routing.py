from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import group.routing




application = ProtocolTypeRouter({
  # (http->django views is added by default)
  'websocket': AuthMiddlewareStack(
    URLRouter(
      group.routing.websocket_urlpatterns
    )
  ),
})