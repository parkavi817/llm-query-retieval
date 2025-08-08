from app.core.config import settings
import nltk
from nltk.tokenize import sent_tokenize

# Download tokenizer once (quiet to avoid clutter)
nltk.download('punkt', quiet=True)

def chunk_text(text, chunk_size=settings.CHUNK_SIZE):
    sentences = sent_tokenize(text, language='english')
    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) < chunk_size:
            current += sentence + " "
        else:
            chunks.append(current.strip())
            current = sentence + " "
    if current:
        chunks.append(current.strip())
    return chunks
