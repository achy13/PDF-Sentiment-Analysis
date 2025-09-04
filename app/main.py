from utils import extract_pdf, split_into_paragraphs, analyze_paragraph
from database import create_tables, insert_document, insert_paragraph, update_document_score

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
