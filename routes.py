from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from completions import extract_vocab, define_vocab
from typing import List
from contextlib import asynccontextmanager
from database import create_tables, get_db
from models import FlashcardSet, Flashcard
import schemas
from bs4 import BeautifulSoup
from docx import Document
import tempfile
import fitz
import os

def convert_to_text(filepath):
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()

    if ext == '.pdf':
        doc = fitz.open(filepath)
        return ''.join([page.get_text() for page in doc])

    elif ext == '.docx':
        doc = Document(filepath)
        return '\n'.join([p.text for p in doc.paragraphs])

    elif ext in ['.html', '.htm']:
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'lxml')
        return soup.get_text()

    else:
        raise ValueError("Unsupported file type")
    
@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/create_cards")
async def create_cards(file: UploadFile = File(...), num: int = 10, set_name: str = None, db: Session = Depends(get_db)):
    try:
        _, ext = os.path.splitext(file.filename)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        t = convert_to_text(tmp_path)
        os.remove(tmp_path)

        vocab = extract_vocab(t, num)
        vocab_words = "\n".join(vocab.word_list)
        definitions = define_vocab(vocab_words)

        flashcard_set_name = set_name or f"Cards from {file.filename}"
        db_flashcard_set = FlashcardSet(name=flashcard_set_name)
        db.add(db_flashcard_set)
        db.commit()
        db.refresh(db_flashcard_set)

        flashcards = []
        for vocab_word, definition in zip(vocab.word_list, definitions.definition):
            db_flashcard = Flashcard(
                sid=db_flashcard_set.id,
                word=vocab_word,
                definition=definition
            )
            db.add(db_flashcard)
            flashcards.append(db_flashcard)

        db.commit()
        
        for flashcard in flashcards:
            db.refresh(flashcard)

        return schemas.CreateCardsResponse(
            sid=db_flashcard_set.id,
            cards=[schemas.Flashcard.from_orm(card) for card in flashcards],
            message=f"Created {len(flashcards)} flashcards successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/flashcard_sets", response_model=List[schemas.FlashcardSet])
def get_flashcard_sets(db: Session = Depends(get_db)):
    sets = db.query(FlashcardSet).all()
    return sets