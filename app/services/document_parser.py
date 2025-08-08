# app/services/document_parser.py
import os
import requests
import tempfile
import fitz  # PyMuPDF
import docx
import email
from bs4 import BeautifulSoup

def download_document(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to download document from URL")
    tmp = tempfile.NamedTemporaryFile(delete=False)
    try:
        tmp.write(response.content)
        tmp.close()
        return tmp.name
    except Exception:
        tmp.close()
        os.unlink(tmp.name)
        raise

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()  # Important to close file handle
    return text

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_email(path):
    with open(path, 'rb') as f:
        msg = email.message_from_binary_file(f)
        body = ""
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_payload(decode=True).decode()
        return body

def parse_document(url):
    path = download_document(url)
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext == ".pdf":
            return extract_text_from_pdf(path)
        elif ext == ".docx":
            return extract_text_from_docx(path)
        elif ext in [".eml", ".msg"]:
            return extract_text_from_email(path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    finally:
        if os.path.exists(path):
            os.unlink(path)  # Clean up temp file
