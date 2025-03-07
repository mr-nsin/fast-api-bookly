from sqlalchemy import Column, UUID, String, DateTime, Boolean
from sqlalchemy.orm import relationship, Mapped
from datetime import datetime
from src.db.main import Base
import uuid
from typing import List
from src.books import models

class User(Base):
    __tablename__ = "users"
    uid: uuid.UUID = Column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4)
    username: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False)
    first_name: str = Column(String, nullable=False)
    last_name: str = Column(String, nullable=False)
    role: str = Column(String, nullable=False, default='user')
    is_verified: bool = Column(Boolean, nullable=False, default=False)
    password: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, nullable=False, default=datetime.now)
    updated_at: datetime = Column(DateTime, nullable=False, default=datetime.now)
    books: Mapped[List['models.Book']] = relationship('Book', back_populates='user', lazy='selectin')

    def __repr__(self):
        return f'<User {self.username}, {self.email}, {self.first_name}, {self.last_name}, {self.is_verified}>'