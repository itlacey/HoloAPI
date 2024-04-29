from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/love-note")
async def root():
    return {"message": "This is from the HoloAPI"}