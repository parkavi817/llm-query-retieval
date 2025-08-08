# Stage 1: Build dependencies
FROM python:3.11-alpine AS builder

RUN apk add --no-cache build-base poppler-utils poppler-dev libmagic libffi-dev

WORKDIR /app

COPY requirements.txt .

RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY ./streamlit_app ./streamlit_app

# Stage 2: Final image
FROM python:3.11-alpine

RUN apk add --no-cache poppler-utils libmagic tini

WORKDIR /app

COPY --from=builder /install /usr/local
COPY --from=builder /app /app

EXPOSE 8000 8501

CMD ["tini", "--", "/bin/sh", "-c", "\
    uvicorn app.main:app --host 0.0.0.0 --port 8000 & \
    streamlit run streamlit_app/app.py --server.port=8501 --server.address=0.0.0.0 \
"]
