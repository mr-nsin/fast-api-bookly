from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from src.books.schemas import Book, BookUpdateModel, BookCreateModel
from src.books.service import BookService
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession

book_router = APIRouter()
book_service = BookService()

@book_router.get("/", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books

@book_router.post('/', response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session)) -> dict:
    new_book = await book_service.create_book(book_data, session)
    return new_book

@book_router.get('/{book_uid}', response_model=Book)
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.get_book(book_uid, session)
    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')

@book_router.patch('/{book_uid}')
async def update_book(book_uid: str, book_update_data: BookUpdateModel, session: AsyncSession = Depends(get_session)) -> dict:
    updated_book = await book_service.update_book(book_uid, book_update_data, session)

    if update_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')