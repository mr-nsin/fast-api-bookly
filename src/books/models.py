from sqlalchemy import Column, UUID, String, Integer, DateTime, ForeignKey
import sqlalchemy.dialects.sqlite as sLit
from src.db.main import Base
from datetime import datetime
import uuid
from typing import Optional


class Book(Base):
    __tablename__ = "books"
    
    uid: uuid.UUID = Column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4)
    title: str = Column(String, nullable=False)
    author: str = Column(String, nullable=False)
    publisher: str = Column(String, nullable=False)
    published_date: datetime = Column(DateTime, nullable=False)
    page_count: int = Column(Integer, nullable=False)
    language: str = Column(String, nullable=False)
    user_uid: Optional[uuid.UUID] = Column(UUID(as_uuid=True), ForeignKey('users.uid'), nullable=True, default=None)
    created_at: datetime = Column(DateTime, nullable=False, default=datetime.now)
    updated_at: datetime = Column(DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"<Book {self.title}, {self.author}, {self.publisher}, {self.published_date}, {self.page_count}, {self.language}>"