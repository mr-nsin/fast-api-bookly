from sqlalchemy.ext.asyncio import AsyncSession
from src.books.models import Book
from src.books.schemas import BookCreateModel, BookUpdateModel

class BookService:
    async def get_all_books(self, session: AsyncSession):
        return await session.execute(Book.select())
    
    # async def get_book(self, session: AsyncSession, book_id: int):
    #     return await session.execute(Book.select().where(Book.id == book_id))
    
    # async def create_book(self, session: AsyncSession, book_data: BookCreateModel):
    #     new_book = Book(**book_data)
    #     session.add(new_book)
    #     await session.commit()
    #     return new_book
    
    # async def update_book(self, session: AsyncSession, book_id: int, book_data: BookUpdateModel):
    #     book = await self.get_book(session, book_id)
    #     book.update(book_data)
    #     await session.commit()
    #     return book
    
    # async def delete_book