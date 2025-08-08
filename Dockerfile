# Dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY ./app /app/app
COPY ./requirements.txt /app

WORKDIR /app

# Install system dependencies for PDF, DOCX, emails if needed
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    libpoppler-cpp-dev \
    && apt-get clean

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
