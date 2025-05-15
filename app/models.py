from sqlmodel import SQLModel, Field
from typing import Optional
import datetime

class ChatHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_message: str
    bot_response: str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
