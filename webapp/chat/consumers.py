import json
import random
import string

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

@sync_to_async
def generate_room_name(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    
    return password


class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = await generate_room_name(20)
        self.room_group_name = f'chat_{self.room_name}'

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from web socket
    async def receive(self, text_data):
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text_data,
            }
        )
    
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }))