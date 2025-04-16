import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    #methods that define the behaviour of consumer.
    #first is the connect method
    async def connect(self):
        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
        #adding the consumer to a channel layer
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        #accepts an incoming socket
        await self.accept()
        
    #next, the disconnect method
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        self.close(code)
        
    #next the receive method
    async def receive(self, text_data):
        data_json = json.loads(text_data)
        
        #create an event, that broadcast messages when received.
        event = {
            'type': 'send_message',
            'message': data_json
        }
        
        await self.channel_layer.group_send(self.room_name, event)
        
    async def send_message(self, event):
        data = event['message']
        await self.create_message(data = data)
        
        response = {
            "sender": data["sender"],
            "message": data["message"],
        }
        
        await self.send(text_data=json.dumps({"message":response}))
        
    @database_sync_to_async
    def create_message(self, data):
        get_room = Room.objects.get(room_name=data['room_name'])
        if not Message.objects.filter(message=data['message'], sender=data["sender"]).exists():
            new_message = Message.objects.create(room=get_room, message = data['message'], sender=data["sender"])
        
        
        