import requests
import os

# Path to uploaded file
file_path = "uploads/Devops unit 1.pdf"  # .pdf, .docx, or .txt

# Extract text from uploaded file (reuse your service functions)
from app.services.document_parser import extract_text_from_pdf, extract_text_from_docx

def load_document_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

# Load text from file
document_text = load_document_text(file_path)

# ✅ Fix: wrap document_text in a list
data = {
    "documents": [document_text],
    "questions": [
        "What is DevOps?",
        "Explain benefits of DevOps",
        "Define CI/CD in DevOps context"
    ]
}

# Call the endpoint
response = requests.post("http://localhost:8000/api/v1/hackrx/run", json=data)

# Output result
print("🔍 Response:\n", response.json())
