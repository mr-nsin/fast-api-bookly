from sqlalchemy import Column, UUID, String, Integer, DateTime
from datetime import datetime
from src.db.main import Base
import uuid

class User(Base):
    __tablename__ = "users"
    uid: uuid.UUID = Column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4)
    username: str = Column(String, nullable=False)
    email: str
    first_name: str
    last_name: str
    is_verified: bool = False
    created_at: datetime
    updated_at: datetime