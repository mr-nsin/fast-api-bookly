from pydantic import BaseModel, Field
from src.books.schemas import Book
from datetime import datetime
from typing import List, Optional
import uuid

class UserRequestModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
    

class UserResponseModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime
    books: Optional[List[Book]]

    class Config:
        orm_mode = True

class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)