import pytest
from fastapi.testclient import TestClient
from app.main import app
from io import BytesIO
from reportlab.pdfgen import canvas

client = TestClient(app)

def create_test_pdf_bytes(text="Hello World!"):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, text)
    c.save()
    buffer.seek(0)
    return buffer.read()

# --- Test the POST /analyze_pdf endpoint ---
def test_post_analyze_pdf(tmp_path):
    pdf_bytes = create_test_pdf_bytes("Integration Test PDF")
    pdf_file = tmp_path / "integration_test.pdf"
    pdf_file.write_bytes(pdf_bytes)

    with open(pdf_file, "rb") as f:
        response = client.post("/analyze_pdf", files={"file": ("integration_test.pdf", f, "application/pdf")})

    assert response.status_code == 200
    data = response.json()
    assert "document_id" in data
    assert "overall_score" in data

# --- Test the GET /analysis/{document_id} endpoint ---
def test_get_analysis(tmp_path):
    pdf_bytes = create_test_pdf_bytes("Integration GET PDF")
    pdf_file = tmp_path / "integration_get.pdf"
    pdf_file.write_bytes(pdf_bytes)

    with open(pdf_file, "rb") as f:
        post_resp = client.post("/analyze_pdf", files={"file": ("integration_get.pdf", f, "application/pdf")})

    doc_id = post_resp.json()["document_id"]
    get_resp = client.get(f"/analysis/{doc_id}")
    
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["document_id"] == doc_id
    assert "paragraphs" in data
    assert isinstance(data["paragraphs"], list)
