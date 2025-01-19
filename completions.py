from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()

PROMPT = {
    "extract":"",
    "define":""
}

class Vocab(BaseModel):
    word_list: list[str]

class Definition(BaseModel):
    definition: list[str]

def extract_vocab():
    extraction = client.beta.chat.completions.parse(
        model="",
        messages=[
            {"role":"system",
             "content":PROMPT["extract"]},
            {"role":"user", 
             "content":""}
        ],
    response_format=Vocab
    )
    return extraction.choices[0].message.parsed

def define_vocab():
    definition = client.beta.chat.completions.parse(
        model="",
        messages=[
            {"role":"system",
             "content":PROMPT["define"]},
            {"role":"user",
             "content":""}
        ],
    response_format=Definition
    )
    return definition.choices[0].message.parsed