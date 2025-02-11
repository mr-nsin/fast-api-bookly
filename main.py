from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def life_span(app: FastAPI):
    print('Starting up...')
    yield
    print('Shutting down...')

version = 'v1'

app = FastAPI(
    title="Bookly",
    description="A REST API for a book review web service",
    version=version,
    lifespan=life_span
)

app.include_router(book_router, prefix=f'/api/{version}/books', tags=['books'])


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)