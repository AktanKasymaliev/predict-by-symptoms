from typing import Any
import json

from langchain.callbacks.base import AsyncCallbackHandler

from .schemas import Chat

class StreamingLLMCallbackHandler(AsyncCallbackHandler):

    def __init__(self, consumer) -> None:
        self.consumer = consumer
    
    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        resp = Chat(username="Bot", message=token, type="stream")
        await self.consumer.send(text_data=json.dumps(resp.dict()))