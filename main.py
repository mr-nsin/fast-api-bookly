from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get('/')
async def read_root():
    return {"message": "Hello World"}

@app.get('/greet/{name}')
async def greet_name(name: str):
    return {"message": f"Hello {name}"}

if __name__ == '__main__':
    uvicorn.run("main:app", port=9000, reload=True)