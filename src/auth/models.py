from sqlalchemy import Column, UUID, String, Integer, DateTime, Boolean
from datetime import datetime
from src.db.main import Base
import uuid

class User(Base):
    __tablename__ = "users"
    uid: uuid.UUID = Column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4)
    username: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False)
    first_name: str = Column(String, nullable=False)
    last_name: str = Column(String, nullable=False)
    is_verified: bool = Column(Boolean, nullable=False, default=False)
    created_at: datetime = Column(DateTime, nullable=False, default=datetime.now)
    updated_at: datetime = Column(DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f'<User {self.username}, {self.email}, {self.first_name}, {self.last_name}, {self.is_verified}>'