from pydantic import BaseModel
from datetime import datetime
from typing import List

class FlashcardBase(BaseModel):
    word: str
    definition: str

class Flashcard(FlashcardBase):
    id: int
    sid: int
    created_at: datetime

    class Config:
        from_attributes = True

class FlashcardSetBase(BaseModel):
    name: str

class FlashcardSet(FlashcardSetBase):
    id: int
    created_at: datetime
    flashcards: List[Flashcard] = []

    class Config:
        from_attributes = True

class CreateCardsResponse(BaseModel):
    sid: int
    cards: List[Flashcard]
    message: str