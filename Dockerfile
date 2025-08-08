# Stage 1: Builder image - install dependencies and build packages
FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    libpoppler-cpp-dev \
    libmagic1 \
    && apt-get clean

WORKDIR /app

COPY requirements.txt .

RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY ./streamlit_app ./streamlit_app

# Stage 2: Final runtime image
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    poppler-utils \
    libmagic1 \
    tini \
    && apt-get clean

WORKDIR /app

COPY --from=builder /install /usr/local
COPY --from=builder /app /app

EXPOSE 8000 8501

CMD ["tini", "--", "/bin/sh", "-c", "\
    uvicorn app.main:app --host 0.0.0.0 --port 8000 & \
    streamlit run streamlit_app/app.py --server.port=8501 --server.address=0.0.0.0 \
"]

