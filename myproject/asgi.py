"""
ASGI config for myproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import wsPattern

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

#this the normal asgi django use to handle http request, but we want more that that, that is to also handle the websocket request.
#application = get_asgi_application()

http_response_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': http_response_app,
    'websocket': URLRouter(wsPattern),
})

#since we have a new application, we have to register it in our DJANGO_SETTINGS_MODULE