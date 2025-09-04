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