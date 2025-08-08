# app/services/semantic_search.py
from app.core.embeddings import get_embedding_model
from app.core.config import settings
import faiss
import numpy as np

embedding_model = get_embedding_model()

def build_faiss_index(chunks):
    vectors = embedding_model.encode(chunks, normalize_embeddings=True)  # normalize for cosine similarity
    index = faiss.IndexFlatIP(vectors.shape[1])  # Inner product = cosine similarity with normalized vectors
    index.add(vectors)
    return index, vectors

def get_similar_chunks(chunks, questions):
    index, vectors = build_faiss_index(chunks)
    q_vectors = embedding_model.encode(questions, normalize_embeddings=True)

    results = []
    for vec in q_vectors:
        _, indices = index.search(np.array([vec]), k=settings.TOP_K)
        similar = [chunks[i] for i in indices[0]]
        results.append(similar)
    return results
