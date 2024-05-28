from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.middleware.sessions import SessionMiddleware
from .models.love_note import LoveNote
from dotenv import load_dotenv, find_dotenv
import os

if not os.getenv("SECRET_KEY") or not os.getenv("USER_PASSWORD") or not os.getenv("USER_NAME"):
    # Load environment variables from .env file if they are not set
    load_dotenv(find_dotenv())

# Access environment variables
secret_key = os.getenv("SECRET_KEY")
user_password = os.getenv("USER_PASSWORD")
user_name = os.getenv("USER_NAME")

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.add_middleware(SessionMiddleware, secret_key=secret_key)

love_note = LoveNote()
templates = Jinja2Templates(directory="./app/templates")

# Simulated user database
fake_users_db = {
    "user": {
        "username": user_name,
        "password": user_password
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or user["password"] != password:
        return False
    return True

@app.get("/", response_class=HTMLResponse)
async def login_form(request: Request):
    if request.session.get("user"):
        return RedirectResponse(url="/form")
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if authenticate_user(username, password):
        request.session["user"] = username
        return RedirectResponse(url="/form", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/form", response_class=HTMLResponse)
async def get_form(request: Request):
    if not request.session.get("user"):
        return RedirectResponse(url="/")
    return templates.TemplateResponse("form.html", {"request": request, "message": love_note.message})

@app.post("/save-note")
async def save_note(request: Request, message: str = Form(...)):
    if not request.session.get("user"):
        return RedirectResponse(url="/")
    love_note.message = message
    return {"message": "Note saved successfully"}

@app.get("/love-note")
async def get_love_note():
    return {"message": love_note.message}
