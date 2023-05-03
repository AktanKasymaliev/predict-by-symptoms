from pydantic import BaseModel, validator

class Chat(BaseModel):

    username: str
    message: str
    type: str

    @validator("username")
    def sender_must_be_bot_or_you(cls, v):
        if v not in ["Bot", "you"]:
            raise ValueError("username must be bot or you")
        return v

    @validator("type")
    def validate_message_type(cls, v):
        if v not in ["start", "stream", "end", "error", "info", "clarification"]:
            raise ValueError("type must be start, stream or end")
        return v