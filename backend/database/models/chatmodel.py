from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime
)
import datetime

from ..configurations import Base
from sqlalchemy.schema import PrimaryKeyConstraint

class Chat(Base):
    __tablename__="chats"
    chat_id = Column(Integer,primary_key=True,autoincrement=True)
    chat_session = Column(String,nullable=False)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    human_msg = Column(String(200),nullable=False)
    timestamp = Column(DateTime,nullable=False)
    ai_msg = Column(String,nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint(chat_id,user_id,chat_session)
    )