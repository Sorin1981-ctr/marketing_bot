from models import Book
from typing import List


def generate_facebook_post(book: Book, tone: str) -> str:
    benefits = ", ".join(book.main_benefits)
    return (
        f"📚 {book.title}\n\n"
        f"{book.description}\n\n"
        f"Această carte este pentru {book.target_audience}. "
        f"Te ajută să obții: {benefits}.\n\n"
        f"Comandă aici: {book.purchase_link}\n"
        f"#carte #lectura #autor"
    )


def generate_ad_texts(book: Book, emotion: str, main_benefit: str) -> List[str]:
    t1 = (
        f"Simți că ai nevoie de mai mult {emotion}? "
        f"Cartea \"{book.title}\" te ajută să obții {main_benefit}. "
        f"Comandă aici: {book.purchase_link}"
    )
    t2 = (
        f"Nu mai amâna. {book.title} îți aduce {main_benefit}. "
        f"Perfectă pentru {book.target_audience}. "
        f"Vezi detalii: {book.purchase_link}"
    )
    t3 = (
        f"Cauți o carte de {book.genre} care chiar să te ajute? "
        f"{book.title} îți oferă {main_benefit}. "
        f"Intră aici: {book.purchase_link}"
    )
    return [t1, t2, t3]


def generate_long_description(book: Book) -> str:
    benefits = ", ".join(book.main_benefits)
    return (
        f"{book.title}\n\n"
        f"{book.description}\n\n"
        f"Public țintă: {book.target_audience}.\n"
        f"Beneficii: {benefits}.\n\n"
        f"Comandă aici: {book.purchase_link}"
    )


def generate_launch_email(book: Book) -> dict:
    subjects = [
        f"Noua mea carte: {book.title}",
        f"{book.title} – disponibilă acum",
        f"O carte nouă pentru tine",
        f"Dacă iubești {book.genre}, vei iubi {book.title}",
        f"{book.title} – descoperă povestea",
    ]

    body = (
        f"Salut,\n\n"
        f"Sunt autorul cărții \"{book.title}\" și sunt bucuros să îți spun că este acum disponibilă.\n\n"
        f"{book.description}\n\n"
        f"Cartea este pentru {book.target_audience} și te ajută să obții:\n"
        f"- " + "\n- ".join(book.main_benefits) + "\n\n"
        f"Comandă aici: {book.purchase_link}\n\n"
        f"Mulțumesc pentru susținere!"
    )

    return {"subjects": subjects, "body": body}


def generate_monthly_campaign(book: Book) -> List[dict]:
    posts = []
    for i in range(1, 13):
        posts.append(
            {
                "title": f"Postarea {i}",
                "text": f"Campanie pentru {book.title} – postarea {i}.",
                "visual": "Imagine cu coperta cărții.",
            }
        )
    return posts
