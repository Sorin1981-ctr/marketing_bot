from fastapi import FastAPI, HTTPException
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from models import (
    Book, CreateBook, FacebookPostRequest, AdTextsRequest,
    LongDescriptionRequest, LaunchEmailRequest, MonthlyCampaignRequest
)
from storage import add_book, get_books, get_book_by_id, load_books
from ai import (
    generate_facebook_post, generate_ad_texts, generate_long_description,
    generate_launch_email, generate_monthly_campaign
)

# ---------------------------------------------------------
# 1. Creează aplicația FastAPI
# ---------------------------------------------------------
app = FastAPI(title="Marketing Bot pentru Cărți")

# ---------------------------------------------------------
# 2. Încarcă datele
# ---------------------------------------------------------
load_books()

# ---------------------------------------------------------
# 3. Montează fișiere statice (pentru HTML)
# ---------------------------------------------------------
app.mount("/static", StaticFiles(directory="."), name="static")

# ---------------------------------------------------------
# 4. Ruta pentru pagina HTML
# ---------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# ---------------------------------------------------------
# 5. Ruta pentru chat
# ---------------------------------------------------------
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    reply = f"Botul a primit: {req.message}"
    return {"reply": reply}

# ---------------------------------------------------------
# 6. Rutele pentru cărți și generare conținut
# ---------------------------------------------------------
@app.get("/books", response_model=List[Book])
def list_books():
    return get_books()

@app.post("/books", response_model=Book)
def create_book(data: CreateBook):
    return add_book(data)

def _get_book_or_404(book_id: int) -> Book:
    book = get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Cartea nu a fost găsită")
    return book

@app.post("/generate/facebook_post")
def create_facebook_post(req: FacebookPostRequest):
    book = _get_book_or_404(req.book_id)
    return {"text": generate_facebook_post(book, req.tone)}

@app.post("/generate/ad_texts")
def create_ad_texts(req: AdTextsRequest):
    book = _get_book_or_404(req.book_id)
    return {"texts": generate_ad_texts(book, req.emotion, req.main_benefit)}

@app.post("/generate/long_description")
def create_long_description(req: LongDescriptionRequest):
    book = _get_book_or_404(req.book_id)
    return {"text": generate_long_description(book)}

@app.post("/generate/launch_email")
def create_launch_email(req: LaunchEmailRequest):
    book = _get_book_or_404(req.book_id)
    return generate_launch_email(book)

@app.post("/generate/monthly_campaign")
def create_monthly_campaign(req: MonthlyCampaignRequest):
    book = _get_book_or_404(req.book_id)
    return {"posts": generate_monthly_campaign(book)}
