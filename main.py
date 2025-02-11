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