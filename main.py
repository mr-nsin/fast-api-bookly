from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get('/')
async def read_root():
    return {"message": "Hello World"}

# Query Parameters Example
@app.get('/greet')
async def greet_name(name: str, age: int) -> dict:
    return {"message": f"Hello {name}"}

if __name__ == '__main__':
    uvicorn.run("main:app", port=9000, reload=True)