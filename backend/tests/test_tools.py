from langchain_core.documents import Document
from backend.assistant.tools import format_docs

def test_format_docs_pdf():
    """Test formatting for PDF documents"""
    docs = [
        Document(
            page_content="Wine details...", 
            metadata={"source": "/data/pdf/vins_2021.pdf", "page": 10}
        )
    ]
    result = format_docs(docs)
    
    assert "[Source: vins_2021.pdf | Page: 10]" in result
    assert "Wine details..." in result

def test_format_docs_web():
    """Test formatting for Web documents"""
    docs = [
        Document(
            page_content="Price info...", 
            metadata={"source": "https://shop.celliers.ch/vin.html", "language": "en"}
        )
    ]
    result = format_docs(docs)
    
    # Check if it creates a clickable link
    assert "[Source: Voir la source du produit](https://shop.celliers.ch/vin.html)" in result