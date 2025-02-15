from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.books.models import Book
from src.books.schemas import BookUpdateModel, BookCreateModel

class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book)
        result = await session.execute(statement)
        return result.scalars().all()
    
    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.execute(statement)
        book = result.first()
        return book if book is not None else None
        
    
    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        print(book_data_dict)
        new_book = Book(**book_data_dict)
        session.add(new_book)
        await session.commit()
        return new_book    
    
    async def update_book(self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession):
        book_to_update = self.get_book(book_uid, session)
        update_data_dict = update_data.model_dump()
        for k, v in update_data.items():
            setattr(book_to_update, k, v)
        await session.commit()
        return book_to_update
    
    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = self.get_book(book_uid, session)
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
        else:
            return None