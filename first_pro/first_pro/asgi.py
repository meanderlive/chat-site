"""import os
import django
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_pro.settings')
django.setup()

import firstapp.routing

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            firstapp.routing.websocket_urlpatterns
        )
    ),
})"""

'''import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import django
django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_pro.settings')


import firstapp.routing  # Import your routing configuration

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            firstapp.routing.websocket_urlpatterns
        )
    ),
})'''

import os
import django
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_pro.settings')


import firstapp.routing  # Import your routing configuration

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            firstapp.routing.websocket_urlpatterns
        )
    ),
})



"""import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_pro.settings')
application = get_asgi_application()"""

