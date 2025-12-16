from backend.assistant.data_handling.load_data import bs4_extractor

# html mockup
MOCK_HTML = """
<html>
    <header id="header">Useless Menu</header>
    <nav class="breadcrumb">Home > Shop > Red Wine</nav>
    
    <div class="product-detail">
        <h1>Fendant 2021</h1>
        <p>This is a delicious white wine from Valais.</p>
        <span class="price">15.00 CHF</span>
    </div>

    <section class="featured-products">Other wines you might like...</section>
    <footer id="footer">Copyright 2025</footer>
    <div class="an_verification_modal-wrap">Age Check Popup</div>
</html>
"""

def test_extractor_removes_noise():
    """Checks if headers, footers, and popups are removed"""
    cleaned_text = bs4_extractor(MOCK_HTML)
    
    # check unwanted elements are not here
    assert "Useless Menu" not in cleaned_text
    assert "Copyright 2025" not in cleaned_text
    assert "Age Check Popup" not in cleaned_text
    assert "Other wines" not in cleaned_text  # section.featured-products

def test_extractor_keeps_content():
    """Checks if the wine name and description remain."""
    cleaned_text = bs4_extractor(MOCK_HTML)
    
    # check that important data is still here
    assert "Fendant 2021" in cleaned_text
    assert "delicious white wine" in cleaned_text
    assert "15.00 CHF" in cleaned_text