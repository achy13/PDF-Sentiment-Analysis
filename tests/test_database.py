import pytest
import sqlite3
from app import database

@pytest.fixture
def db_connection():
    con = sqlite3.connect(":memory:")
    c = con.cursor()
    c.execute('''CREATE TABLE documents(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  filename TEXT NOT NULL,
                  overall_sentiment REAL         
                  )''')
    c.execute('''CREATE TABLE paragraphs(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  document_id INTEGER NOT NULL,
                  text TEXT NOT NULL,
                  sentiment_score REAL,
                  FOREIGN KEY(document_id) REFERENCES documents(id)
                  )''')
    con.commit()
    yield con
    con.close()

# --- Test inserting and fetching a document ---
def test_insert_and_fetch_document(db_connection):
    con = db_connection
    doc_id = database.insert_document(filename="test.pdf", overall_sentiment=None)
    
    doc = database.fetch_document(doc_id)
    assert doc is not None
    assert doc["document_id"] == doc_id
    assert doc["filename"] == "test.pdf"
    assert doc["overall_sentiment"] is None

# --- Test inserting a paragraph linked to a document ---
def test_insert_paragraph(db_connection):
    con = db_connection
    doc_id = database.insert_document("test.pdf", None)
    database.insert_paragraph(doc_id, "Para text", 0.5)
    
    doc = database.fetch_document(doc_id)
    assert len(doc["paragraphs"]) == 1
    assert doc["paragraphs"][0]["text"] == "Para text"

# --- Test updating the overall sentiment score of a document ---
def test_update_document_score(db_connection):
    con = db_connection
    doc_id = database.insert_document("test.pdf", None)
    database.update_document_score(doc_id, 0.7)
    
    doc = database.fetch_document(doc_id)
    assert doc["overall_sentiment"] == 0.7
