from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import CONFIG

# Define the base model
Base = declarative_base()

# Ensure the DATABASE_URL uses aiosqlite
DATABASE_URL = CONFIG.DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite:///")

# Create the async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

# Create a configured "Session" class
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    async with engine.begin() as conn:
        from src.books.models import Book
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

