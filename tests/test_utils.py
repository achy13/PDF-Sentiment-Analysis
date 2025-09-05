from app.utils import split_into_paragraphs, analyze_paragraph, extract_pdf

# --- Tests for the function split_into_paragraphs ---
# Checks that an empty string returns an empty list
def test_split_empty_text():
    assert split_into_paragraphs("") == []

# Checks that a string containing only newlines returns an empty list
def test_split_only_newlines():
    assert split_into_paragraphs("\n\n\n") == []

# Checks that text with leading/trailing spaces and newlines
# is cleaned and split correctly into paragraphs
def test_split_lines_with_spaces():
    text = " Hello \n World "
    assert split_into_paragraphs(text) == ["Hello", "World"]


# --- Tests for the function analyze_paragraph ---
# Checks that analyzing an empty paragraph returns a score as float
# and that the score is within the range [-1, 1]
def test_analyze_empty_paragraph():
    result = analyze_paragraph("")
    assert isinstance(result['score'], float)
    assert -1 <= result['score'] <= 1

# Checks that analyzing a negative paragraph returns a score as float
# and that the score is within the range [-1, 1]
def test_analyze_negative_paragraph():
    paragraph = "I hate bugs!"
    result = analyze_paragraph(paragraph)
    assert isinstance(result['score'], float)
    assert -1 <= result['score'] <= 1


# --- Tests for the function extract_pdf ---
# Checks that the text extracted from a PDF is a string
# and contains the expected text "Hello World!"
def test_extract_pdf():
    pdf_path = "data/test.pdf"
    text = extract_pdf(pdf_path)
    assert isinstance(text, str)
    assert "Hello World!" in text

