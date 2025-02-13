<<<<<<< HEAD
from fastapi import FastAPI, Header
from pydantic import BaseModel
from datetime import datetime
import uvicorn

app = FastAPI()

class BookCreateModel(BaseModel):
    title: str
    author: str
    
    
@app.get('/')
async def read_root():
    return {"message": "Hello World"}

# Query Parameters Example
@app.get('/greet')
async def greet_name(name: str, age: int) -> dict:
    return {"message": f"Hello {name}"}


@app.post('/create_book')
async def create_book(request: BookCreateModel):
    return {
        "title": request.title,
        "author": request.author
    }

@app.get('/get_headers')
async def get_headers(
    accept: str = Header(None),
    content_type: str = Header(None),
    user_agent: str = Header(None)
):
    request_headers = {}
    request_headers["Accept"] = accept
    request_headers["Content-Type"] = content_type
    request_headers["User-Agent"] = user_agent

    return request_headers

if __name__ == '__main__':
    uvicorn.run("main:app", port=9000, reload=True)
=======
from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def life_span(app: FastAPI):
    print('Starting up...')
    await init_db()
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
>>>>>>> 8b4138dcde94296f3a9e2077d90d689119e9feaa
