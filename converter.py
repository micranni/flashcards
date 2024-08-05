import os
import fitz
from docx import Document
from bs4 import BeautifulSoup

def convert_to_txt(filepath):
    filename, file_extension = os.path.splitext(filepath)
    txt_filepath = f"{filename}.txt"
    print(f"Converting file: {filepath} to {txt_filepath}")

    if file_extension.lower() == '.pdf':
        doc = fitz.open(filepath)
        text = ''
        for page in doc:
            text += page.get_text()
        with open(txt_filepath, 'w') as f:
            f.write(text)

    elif file_extension.lower() == '.docx':
        doc = Document(filepath)
        with open(txt_filepath, 'w') as f:  
            for paragraph in doc.paragraphs:
                f.write(paragraph.text + '\n')

    elif file_extension.lower() in ['.html', '.htm']:
        with open(filepath, 'r') as f:
            soup = BeautifulSoup(f, 'lxml')
        text = soup.get_text()
        with open(txt_filepath, 'w') as f:
            f.write(text)

    else:
        print("Unsupported file type")  # Debug statement
        return None
    
    with open(txt_filepath, 'r') as f:
        text_content = f.read()

    os.remove(txt_filepath)
    
    return text_content