from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from .models.love_note import LoveNote

app = FastAPI()

love_note = LoveNote()

templates = Jinja2Templates(directory="./app/templates")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "message": love_note.message})

@app.post("/save-note")
async def save_note(
    message: str = Form(...)
):
    love_note.message = message
    return {"message": "Note saved successfully"}

@app.get("/love-note")
async def get_love_note():
    return {"message": love_note.message}
