# Flashcard Generator

AI-powered flashcard creation from PDF, DOCX, and HTML files using OpenAI's GPT models.

## Features

- Upload PDF, DOCX, or HTML files
- Extract vocabulary words automatically
- Generate definitions using AI
- Store flashcard sets in PostgreSQL database
- Retrieve saved flashcard sets via API

## API Endpoints

- `POST /create_cards` - Upload file and generate flashcards
- `GET /flashcard_sets` - Retrieve all saved flashcard sets

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- OpenAI API
- Pydantic
