from django.urls import re_path
from .consumers import ChatConsumer
#from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<username>[\w.@+-]+)/$', ChatConsumer.as_asgi()),
    #re_path(r'ws/chat/(?P<username>\w+)/$', ChatConsumer.as_asgi()),
    #re_path(r'ws/chat/(?P<username>\w+)/$', ChatConsumer.as_asgi()),
]
