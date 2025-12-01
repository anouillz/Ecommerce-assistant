import os
from pathlib import Path
import wget

from rich.console import Console
from rich.markdown import Markdown

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS

from langchain_text_splitters import RecursiveCharacterTextSplitter



console = Console()

PDF_FOLDER = Path("simple_demo/data/PDFs")
VECTORSTORES_DIR = Path("simple_demo/data/vectorstores_pdf")

def load_data():
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 100
    documents = []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=['\n\n', '\n', '(?<=\. )', '(?<=\, )', ' ', '']
    )

    # Load and process the text files
    loader = DirectoryLoader(PDF_FOLDER, glob="./*.pdf", loader_cls=PyPDFLoader)

    pdf_docs = loader.load()
    print(len(pdf_docs))

    # tokenize pdfs
    documents.extend(text_splitter.split_documents(pdf_docs))
    print(len(documents))
    return documents

def store_vectors(documents, vectorstore):
    vectorstore.save_local(VECTORSTORES_DIR)
    print("Vectors stored")


## testing

##load_data(documents)
#print(documents[0].page_content)
#print(documents[1].metadata) # metadata important to know source of chunk

#store_vectors(documents)