import random
import string
import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .chatbot.prompts import get_chat_prompt, get_intent_prompt
from .chatbot.chains import get_chat_chain, get_intents_chain
from .chatbot.utils import init_vector_retriever
from .chatbot.schemas import Chat

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

        self.retriever = sync_to_async(init_vector_retriever)()

        self.chat_chain = sync_to_async(get_chat_chain)(self.retriever)
        self.intents_chain = sync_to_async(get_intents_chain)()

        self.chat_prompt = sync_to_async(get_chat_prompt)()
        self.intents_prompt = sync_to_async(get_intent_prompt)()

        response = Chat(username="Bot", message="I'am ready to accept questions", type="info")
        await self.send(text_data=json.dumps(response.dict()))


    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from web socket
    async def receive(self, text_data):
        print(text_data)
        response = Chat(username="Bot", message="", type="stream")
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            response.dict()
        )
    
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=message)