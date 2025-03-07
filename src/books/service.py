from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.books.models import Book
from datetime import datetime
from src.books.schemas import BookUpdateModel, BookCreateModel
import uuid

class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book)
        result = await session.execute(statement)
        return result.scalars().all()
    
    
    async def get_user_books(self, user_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.user_uid == uuid.UUID(user_uid))
        result = await session.execute(statement)        
        books = result.scalars().all()
        return books
    
    
    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == uuid.UUID(book_uid))
        result = await session.execute(statement)
        book = result.scalar_one_or_none()
        return book if book is not None else None
    
    async def create_book(self, book_data: BookCreateModel, user_id : str, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)

        new_book.published_date = datetime.strptime(book_data_dict['published_date'], '%Y-%m-%d')
        new_book.user_uid = uuid.UUID(user_id)

        session.add(new_book)
        await session.commit()
        return new_book    
    
    async def update_book(self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession):
        book_to_update = await self.get_book(book_uid, session)
        if book_to_update is None:
            return book_to_update
        update_data_dict = update_data.model_dump()
        for k, v in update_data_dict.items():
            setattr(book_to_update, k, v)
        await session.commit()
        return book_to_update
    
    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()

            return {}