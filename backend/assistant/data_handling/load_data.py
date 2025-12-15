import re
from langchain_community.document_loaders import PyPDFLoader, RecursiveUrlLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from typing import List
from config import CHUNK_SIZE, CHUNK_OVERLAP

from bs4 import BeautifulSoup

# html extractor 
def bs4_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # list of CSS selectors to remove, they contain information that is not related to the wine itself
    selectors_to_remove = [
        "header#header",               # The top navigation menu and logo
        "footer#footer",               # The bottom footer 
        "footer.page-footer",          # The small footer inside the main section
        "section.featured-products",   # "Les clients qui ont acheté ce produit..."
        
        ".an_verification_modal-wrap", # Age verification popup
        ".pswp",                       # Hidden code for image galleries (PhotoSwipe)
        ".modal",                      # Hidden popups (Quick view, etc.)
        "#search_widget",              # Search bar text
        ".blockcart",                  # Shopping cart text
        ".amega-menu",                 # Mega menu text
        "nav.breadcrumb"               # "Accueil > Shop > Vin" 
    ]

    # loop through the list and remove the tags
    for selector in selectors_to_remove:
        for tag in soup.select(selector):
            tag.decompose() # destroys the tag and its content

    # extract the remaining text
    text = soup.get_text(separator="\n", strip=True)

    # clean up excessive newlines to keep it readable
    return re.sub(r"\n{3,}", "\n\n", text).strip()

def load_chunk_documents(
    file_paths: List[str],
    url,
    base_url,
    chunk_size= CHUNK_SIZE,
    chunk_overlap= CHUNK_OVERLAP
):
    documents = []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=['\n\n', '\n', '(?<=\. )', '(?<=\, )', ' ', '']
    )

    web_loader = RecursiveUrlLoader(
        url, 
        extractor=bs4_extractor,
        max_depth=10,
        use_async=True,
        base_url=base_url
    )
    web_docs = web_loader.load()
    valid_docs = []
    # only keep .html links
    for doc in web_docs:
        source_url = doc.metadata["source"]
        if ".html" in source_url:
            print(f"liens valides: {source_url}")
            valid_docs.append(doc)
    print(f"Loaded {len(valid_docs)} documents")
    # web documents could be splitted in chunks such as pdf documents but to keep all information about one wine together and avoid hallucinations, I kept it full
    documents.extend(valid_docs)
    
    # load and process pdf files
    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        pdf_docs = loader.load()
        print(f"Loaded {len(pdf_docs)} documents from {file_path}.")

        # Tokenize PDFs
        documents.extend(text_splitter.split_documents(pdf_docs))

    print(f"Tokenized into {len(documents)} chunks.")
    return documents

