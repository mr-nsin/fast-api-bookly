from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import CONFIG

engine = AsyncEngine(
        create_engine(
            url=CONFIG.DATABASE_URL,
             echo=True
        )
    )
