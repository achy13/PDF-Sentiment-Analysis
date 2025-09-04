import sqlite3

DATABASE_PATH = "data\database.db"

def create_tables():
    con = sqlite3.connect(DATABASE_PATH)
    c = con.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS documents(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              filename TEXT NOT NULL,
              overall_sentiment REAL         
              )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS paragraphs(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              document_id INTEGER NOT NULL,
              text TEXT NOT NULL,
              sentiment_score REAL,
              FOREIGN KEY(document_id) REFERENCES documents(id)
              )''')
    
    con.commit()
    con.close()


def insert_document(filename, overall_sentiment):
    con = sqlite3.connect(DATABASE_PATH)
    c = con.cursor()

    c.execute('''
        INSERT INTO documents (filename, overall_sentiment)
        VALUES (?, ?)
    ''', (filename, overall_sentiment))
    document_id = c.lastrowid
    con.commit()
    con.close()

    return document_id
    


def insert_paragraph(document_id, text, sentiment_score):
    con = sqlite3.connect(DATABASE_PATH)
    c = con.cursor()

    c.execute(''' 
              INSERT INTO paragraphs (document_id, text, sentiment_score)
              VALUES (?, ?, ?)
              ''', (document_id, text, sentiment_score))
    
    con.commit()
    con.close()


def update_document_score(document_id, overall_score):
    con = sqlite3.connect(DATABASE_PATH)
    c = con.cursor()

    c.execute(''' 
              UPDATE documents 
              SET overall_sentiment = ?
              WHERE id = ?
              ''', (overall_score, document_id))
    
    con.commit()
    con.close()

def fetch_document(document_id):
    try:
        document_id = int(document_id)
    except ValueError:
        return None

    con = sqlite3.connect(DATABASE_PATH)
    c = con.cursor()

    # земи документ
    c.execute('''
        SELECT id, filename, overall_sentiment
        FROM documents
        WHERE id = ?
    ''', (document_id,))  # <- запирка е многу важна
    doc_row = c.fetchone()
    if not doc_row:
        con.close()
        return None

    doc_id, filename, overall_sentiment = doc_row

    # земи параграфи
    c.execute('''
        SELECT id, text, sentiment_score
        FROM paragraphs
        WHERE document_id = ?
        ORDER BY id
    ''', (doc_id,))
    paragraphs_rows = c.fetchall() or []

    paragraphs = [
        {"paragraph_id": pid, "text": text, "score": sentiment_score}
        for pid, text, sentiment_score in paragraphs_rows
    ]

    con.close()

    return {
        "document_id": doc_id,
        "filename": filename,
        "overall_sentiment": overall_sentiment,
        "paragraphs": paragraphs
    }
