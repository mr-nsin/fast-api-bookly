from fastapi import APIRouter, status, HTTPException
from typing import List
from src.books.schemas import Book, BookUpdateModel
from src.books.book_data import books
from src.books.service import BookService
from src.db.main import AsyncSessionLocal

book_router = APIRouter()


@book_router.get("/", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_all_books():
    with AsyncSessionLocal() as session:
        books = BookService().get_all_books(session)
        return books

# @book_router.post('/', response_model=BookModel, status_code=status.HTTP_201_CREATED)
# async def create_a_book(book_data: BookModel) -> dict:
#     new_book = book_data.model_dump()

#     return new_book

# @book_router.get('/{book_id}', response_model=BookModel, status_code=status.HTTP_200_OK)
# async def get_book(book_id: int) -> dict:
#     for book in books:
#         if book['id'] == book_id:
#             return book
        
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')

# @book_router.put('/{book_id}', response_model=BookModel, status_code=status.HTTP_200_OK)
# async def update_book(book_id: int, book_update_data: BookUpdateModel) -> dict:
#     for book in books:
#         if book['id'] == book_id:
#             book.update(book_update_data.dict())
#             return book
        
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')

# @book_router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
# async def delete_book(book_id: int):
#     for index, book in enumerate(books):
#         if book['id'] == book_id:
#             books.pop(index)
#             return
        
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
