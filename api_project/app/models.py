from datetime import datetime
from sqlalchemy import Column, String, DateTime
from .database import Base

class Message(Base):
    __tablename__ = 'messages'

    id = Column(String, primary_key=True)
    account_id = Column(String)
    sender_number = Column(String)
    receiver_number = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Message(id='{self.id}', account_id='{self.account_id}', sender_number='{self.sender_number}', receiver_number='{self.receiver_number}')>"
