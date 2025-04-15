from pydantic import BaseModel
from typing import List
from datetime import datetime

class MessageBase(BaseModel):
    role: str
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class ChatRequest(BaseModel):
    message: str
