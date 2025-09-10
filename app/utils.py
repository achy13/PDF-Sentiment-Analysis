import pypdf
import re
from textblob import TextBlob

def extract_pdf(pdf_path):
    text = "" 
    with open(pdf_path, "rb") as file:
        render = pypdf.PdfReader(file)
        for page in render.pages:
            text += page.extract_text() + "\n"

    return text


def split_into_paragraphs(text):
    paragraphs = re.split(r'\n\s*\n', text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    return paragraphs


def analyze_paragraph(paragraph):
    blob = TextBlob(paragraph)
    score = blob.sentiment.polarity
    return {"parahraph": paragraph, "score": score}