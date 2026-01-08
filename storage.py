import json
import os
from typing import List, Optional
from models import Book, CreateBook

BOOKS_FILE = "books.json"
BOOKS_DB: List[Book] = []
_next_id = 1


def load_books():
    global BOOKS_DB, _next_id
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            BOOKS_DB = [Book(**item) for item in data]
            if BOOKS_DB:
                _next_id = max(book.id for book in BOOKS_DB) + 1


def save_books():
    with open(BOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump([book.dict() for book in BOOKS_DB], f, ensure_ascii=False, indent=2)


def add_book(data: CreateBook) -> Book:
    global _next_id
    book = Book(
        id=_next_id,
        title=data.title,
        subtitle=data.subtitle,
        description=data.description,
        genre=data.genre,
        target_audience=data.target_audience,
        main_benefits=data.main_benefits,
        purchase_link=data.purchase_link,
    )
    BOOKS_DB.append(book)
    _next_id += 1
    save_books()
    return book


def get_books() -> List[Book]:
    return BOOKS_DB


def get_book_by_id(book_id: int) -> Optional[Book]:
    for b in BOOKS_DB:
        if b.id == book_id:
            return b
    return None
