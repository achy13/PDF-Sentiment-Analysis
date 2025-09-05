from fastapi import FastAPI, UploadFile, File, HTTPException, Path
from fastapi.responses import JSONResponse
from app.utils import extract_pdf, split_into_paragraphs, analyze_paragraph
from app.database import create_tables, insert_document, insert_paragraph, update_document_score, fetch_document

app = FastAPI()

@app.post("/analyze_pdf")
async def analyze_pdf(file: UploadFile = File(...)):
    pdf_path = f"data/{file.filename}"
    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    doc_id = insert_document(filename=file.filename, overall_sentiment=None)
    text = extract_pdf(pdf_path)
    paragraphs = split_into_paragraphs(text)

    scores = []
    for p in paragraphs:
        result = analyze_paragraph(p)
        insert_paragraph(doc_id, p, result['score'])
        scores.append(result['score'])

    if scores:
        overall_score = sum(scores) / len(scores)
    else:
        overall_score = 0
    update_document_score(doc_id, overall_score)

    return JSONResponse({"document_id": doc_id, "overall_score": overall_score})

@app.get("/analysis/{document_id}")
def get_analysis(document_id: int = Path(...)):
    document = fetch_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

'''
if __name__=="__main__":
    create_tables()

    pdf_path = "data/test_sentiment.pdf"
    text = extract_pdf(pdf_path)
    print(text)
    doc_id = insert_document(filename=pdf_path, overall_sentiment=None)
    
    paragraphs = split_into_paragraphs(text)
    print(paragraphs)

    scores = []
    for p in paragraphs:
        result = analyze_paragraph(p)
        insert_paragraph(doc_id, p, result['score'])
        scores.append(result['score'])
        print(result)

    overall_score = sum(scores) / len(paragraphs)
    update_document_score(doc_id, overall_score)
'''
