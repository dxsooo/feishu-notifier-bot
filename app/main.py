from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/notify")
async def notify():
    return {"message": "Hello World"}
