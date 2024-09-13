from pydantic import BaseModel
from datetime import datetime

class ChatSchema(BaseModel):
    humanmsg: str
    aimessage: str
    session:str
    timestamp: datetime