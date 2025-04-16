from django.urls import path
from .consumers import ChatConsumer

wsPattern = [
    path('ws/messages/<str:room_name>/', ChatConsumer.as_asgi()),
]

#Note; we want to tell the system, if it is the normal http request, then use the normal asgi application, 
# but if it is a web socket request, then use the chat consumer. hence configure asgi.py project level.