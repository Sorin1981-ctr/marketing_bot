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
# 5. CHAT INTELIGENT (mini‑ChatGPT fără API extern)
# ---------------------------------------------------------
class ChatRequest(BaseModel):
    message: str

# memorie simplă pentru context
CONVERSATION_HISTORY: list[dict] = []
MAX_HISTORY = 10


def add_to_history(role: str, content: str):
    CONVERSATION_HISTORY.append({"role": role, "content": content})
    if len(CONVERSATION_HISTORY) > MAX_HISTORY:
        del CONVERSATION_HISTORY[0:len(CONVERSATION_HISTORY) - MAX_HISTORY]


def generate_et_reply(history: list[dict], user_message: str) -> str:
    text = user_message.lower().strip()

    # -------------------------
    # IDENTITATE
    # -------------------------
    if "cine ești" in text or "cine esti" in text:
        return (
            "Sunt ET 👽 — asistentul tău premium pentru marketingul cărților. "
            "Te ajut să creezi postări, reclame, emailuri și campanii complete pentru promovarea cărților tale."
        )

    # -------------------------
    # CE POATE FACE
    # -------------------------
    if "ce poți" in text or "ce poti" in text or "ce știi" in text or "ce stii" in text:
        return (
            "Pot să te ajut cu:\n"
            "• postări pentru Facebook\n"
            "• texte pentru reclame Google Ads\n"
            "• emailuri de lansare\n"
            "• descrieri scurte și lungi\n"
            "• campanii lunare\n\n"
            "Spune-mi ce ai nevoie și mă ocup eu."
        )

    # -------------------------
    # FACEBOOK
    # -------------------------
    if "facebook" in text or "postare" in text:
        return (
            "Iată o postare scurtă pentru Facebook, ton prietenos:\n\n"
            "📚 Descoperă o carte care îți poate schimba perspectiva! "
            "Fiecare pagină te poartă într-o călătorie plină de emoție și inspirație. 💚\n\n"
            "Vrei și o variantă mai scurtă sau mai serioasă?"
        )

    # -------------------------
    # ADS
    # -------------------------
    if "ads" in text or "reclam" in text:
        return (
            "Iată 3 variante de reclame Google Ads:\n\n"
            "1️⃣ Descoperă cartea care îți schimbă perspectiva. Comandă acum!\n"
            "2️⃣ O poveste captivantă care te prinde de la primele pagini. Află mai mult!\n"
            "3️⃣ Inspirație, emoție și idei noi — totul într-o singură carte."
        )

    # -------------------------
    # EMAIL
    # -------------------------
    if "email" in text:
        return (
            "Iată un email de lansare:\n\n"
            "Subiect: A sosit momentul! 📚\n\n"
            "Salut!\n\n"
            "Sunt încântat să îți prezint o carte specială — o lectură care inspiră și captivează. "
            "Dacă vrei să descoperi o poveste care te scoate din rutină, aceasta este alegerea perfectă. "
            "Comandă acum și bucură-te de o experiență memorabilă!\n\n"
            "Cu drag,\nET 👽"
        )

    # -------------------------
    # CAMPANIE
    # -------------------------
    if "campanie" in text or "plan" in text:
        return (
            "Iată o campanie lunară simplă:\n\n"
            "📅 Săptămâna 1: Teasing + citate din carte\n"
            "📅 Săptămâna 2: Povestea autorului + making-of\n"
            "📅 Săptămâna 3: Recenzii + testimoniale\n"
            "📅 Săptămâna 4: Ofertă specială + call to action\n\n"
            "Vrei să o adaptez pentru Facebook, Instagram sau email?"
        )

    # -------------------------
    # RĂSPUNSURI CONVERSAȚIONALE
    # -------------------------
    if "mulțumesc" in text or "mersi" in text:
        return "Cu drag! Dacă vrei, pot crea și alte texte pentru cartea ta. 🙂"

    if "ok" in text or "bine" in text:
        return "Perfect. Spune-mi ce vrei să mai lucrăm."

    if "nu" in text and "îmi place" not in text:
        return "Nicio problemă. Spune-mi ce ton preferi și ajustez imediat."

    # -------------------------
    # FALLBACK INTELIGENT
    # -------------------------
    return (
        "Am înțeles. Spune-mi dacă ai nevoie de o postare, o reclamă, un email, "
        "o descriere sau un plan de campanie și creez eu textul pentru tine."
    )


@app.post("/chat")
def chat(req: ChatRequest):
    user_message = req.message
    add_to_history("user", user_message)

    reply = generate_et_reply(CONVERSATION_HISTORY, user_message)

    add_to_history("assistant", reply)
    return {"reply": reply}

# ---------------------------------------------------------
# 6. RUTELE PENTRU CĂRȚI ȘI GENERARE CONȚINUT
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
