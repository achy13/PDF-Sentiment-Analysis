from utils import extract_pdf, split_into_paragraphs, analyze_paragraph

if __name__=="__main__":
    pdf_path = "data/test_sentiment.pdf"
    text = extract_pdf(pdf_path)
    print(text)

    paragraphs = split_into_paragraphs(text)
    print(paragraphs)

    for p in paragraphs:
        result = analyze_paragraph(p)
        print(result)

