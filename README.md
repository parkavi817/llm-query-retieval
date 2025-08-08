# LLM Query-Retrieval API

This project is a FastAPI backend for an intelligent document query and retrieval system powered by large language models (LLMs). It supports uploading and parsing multiple document types (PDF, DOCX, email, TXT), chunking large texts, semantic search, and clause matching to extract fact-based answers.

---

## Features

- Upload and parse various document types: PDF, DOCX, EML, MSG, TXT
- Text chunking with NLTK sentence tokenizer
- Semantic similarity search for relevant chunks
- LLM-powered clause matching with OpenRouter API
- FastAPI REST API with endpoints for uploading, parsing, and querying documents
- CORS enabled for frontend integration

---

## Getting Started

### Prerequisites

- Python 3.8+
- Pip package manager