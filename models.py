from pydantic import BaseModel
from typing import List, Optional


class Book(BaseModel):
    id: int
    title: str
    subtitle: Optional[str] = None
    description: str
    genre: str
    target_audience: str
    main_benefits: List[str]
    purchase_link: str


class CreateBook(BaseModel):
    title: str
    subtitle: Optional[str] = None
    description: str
    genre: str
    target_audience: str
    main_benefits: List[str]
    purchase_link: str


class FacebookPostRequest(BaseModel):
    book_id: int
    tone: str = "inspirational"


class AdTextsRequest(BaseModel):
    book_id: int
    emotion: str
    main_benefit: str


class LongDescriptionRequest(BaseModel):
    book_id: int


class LaunchEmailRequest(BaseModel):
    book_id: int


class MonthlyCampaignRequest(BaseModel):
    book_id: int
