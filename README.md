# **PDF Sentiment Analysis API**


A FastAPI-based application for analyzing the sentiment of PDF documents. This project extracts text from PDFs, splits it into paragraphs, and evaluates the sentiment of each paragraph as well as the overall sentiment of the document.

---

## Features

- Upload PDF files via API
- Extract text and split into paragraphs
- Analyze sentiment using TextBlob
- Store results in SQLite database
- Unit and integration tests included
- Dockerized for easy deployment

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/achy13/PDF-Sentiment-Analysis.git
cd PDF-Sentiment-Analysis
```


2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## API Usage

Run FastAPI locally

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open http://localhost:8000/docs to access the interactive API documentation.

Endpoints

- POST /analyze_pdf → Upload a PDF and analyze sentiment

- GET /analysis/{document_id} → Retrieve analysis results for a document

---

## Database

SQLite database located in data/database.db

Tables:

- documents → Stores document metadata and overall sentiment

- paragraphs → Stores individual paragraph text and sentiment scores

Tables are automatically created if they do not exist.

--- 

## Docker

Build docker image

```bash
docker build -t pdf-api .
```

Run docker container

```bash
docker run -p 8000:8000 pdf-api
```

Using docker compose

```bash
docker-compose up --build
```

---

## Testing

Unit tests

```bash
pytest tests/test_utils.py
pytest tests/test_database.py
```

Integration tests

```bash
pytest tests/test_main.py
```



