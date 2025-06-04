from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("API key is not set in environment")

client = OpenAI(api_key=api_key)

class Vocab(BaseModel):
    word_list: list[str]

class Definition(BaseModel):
    definition: list[str]

def extract_prompt(n: int = 10) -> str:
    return f"Extract {n} key vocabulary words from the following text to help me study. Return only a valid JSON list of strings. Do not explain and do not add any extra text or words."

def define_prompt() -> str:
    return f"For each of the following words, create a concise English definition. Return only a valid JSON list of strings in the same order. Do not explain and do not add any extra text or words."

def extract_vocab(m, num):
    extraction = client.responses.parse(
        model="gpt-4o-2024-08-06",
        input=[
            {"role":"system","content":extract_prompt(num)},
            {"role":"user", "content":m}
        ],
    text_format=Vocab
    )
    return extraction.output_parsed

def define_vocab(m):
    definition = client.responses.parse(
        model="gpt-4o-2024-08-06",
        input=[
            {"role":"system","content":define_prompt()},
            {"role":"user","content":m}
        ],
    text_format=Definition
    )
    return definition.output_parsed
    