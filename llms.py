from groq import Groq
import os

client = Groq(
    api_key=os.environ.get("groq_api_key")
)

extraction_message = '''

'''

definition_message = '''

'''

def extract_vocab():

    
    chat_completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role":"system",
                "content": extraction_message
            },
            {
                "role":"user",
                "content": user_content
            }
        ],
        
        temperature= 0,
        max_tokens= 8192,
        top_p= 1,
        stream= False
    )

    response_message = chat_completion.choices[0].message.content
    return response_message

def define_vocab():

    chat_completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role":"system",
                "content": definition_message
            },
            {
                "role":"user",
                "content": user_content
            }
        ],
        
        temperature= 0,
        max_tokens= 8192,
        top_p= 1,
        stream= False
    )

    response_message = chat_completion.choices[0].message.content
    return response_message