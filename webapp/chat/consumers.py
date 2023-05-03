import random
import string
import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .chatbot.prompts import get_intent_prompt
from .chatbot.chains import (
    get_stadealone_question_chain, get_intents_chain,
    get_answer_chain
    )
from .chatbot.utils import (
    init_vector_retriever, get_data_from_vectorstore
    )
from .chatbot.schemas import Chat

@sync_to_async
def get_health_data(user):
    data = f"""User health data:
    Gender: {user.gender};
    Age: {user.age};
    Weight: {user.weight} kilograms;
    Height: {user.height} centimeters;
    Health condition notes: {user.health_condition_notes}"""
    return data

@sync_to_async
def generate_room_name(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    
    return password


class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = await generate_room_name(20)
        self.room_group_name = f'chat_{self.room_name}'
        self.health_data = await get_health_data(self.scope["user"])
        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        self.retriever = await sync_to_async(init_vector_retriever)()
        self.intents_chain = await sync_to_async(get_intents_chain)()
        self.intents_prompt = await sync_to_async(get_intent_prompt)()

        response = Chat(username="Bot", message="I am ready to accept questions", type="info")
        await self.send(text_data=json.dumps(response.dict()))


    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from web socket
    async def receive(self, text_data):
        intent = await self.intents_chain.arun(input=text_data)
        if intent == "symptom":
            handler = "symptom_message"
        else:
            handler = "none_message"
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": handler,
                "message": text_data,
                "username": "you",
            }
        )

    async def symptom_message(self, event):
        message = event['message']
        q_chain = await sync_to_async(get_stadealone_question_chain)()

        question = (
            f"Original question: {message}.\nPatient health data: {self.health_data}"
        )
        remastred_q = await q_chain.arun(question=question)
        dataset = await sync_to_async(get_data_from_vectorstore)(self.retriever, remastred_q)
        ans_chain = await sync_to_async(get_answer_chain)()
        answer_to_patient = await ans_chain.arun(
            dataset=dataset,
            complain=message,
            person=self.health_data,
            intent="symptom"
        )

        en_response = Chat(username="Bot", message=answer_to_patient, type="stream")
        await self.send(text_data=json.dumps(en_response.dict()))

    # Receive message from room group
    async def none_message(self, event):
        text = """
        I'm sorry, I can not help you with this question.
        If you feel bad, please, tell me about your symptoms, I will try to help you.
        Or rephrase your question.
        """
        response = Chat(username="Bot", message=text, type="stream")
        await self.send(text_data=json.dumps(response.dict()))