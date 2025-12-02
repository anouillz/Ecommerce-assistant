from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from typing import List, Optional
from config import CHUNK_SIZE, CHUNK_OVERLAP


def load_chunk_documents(
    file_paths: List[str],
    web_links: Optional[List[str]] = None,
    chunk_size= CHUNK_SIZE,
    chunk_overlap= CHUNK_OVERLAP
):
    documents = []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=['\n\n', '\n', '(?<=\. )', '(?<=\, )', ' ', '']
    )

    # TODO: Load web links

    # load and process pdf files
    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        pdf_docs = loader.load()
        print(f"Loaded {len(pdf_docs)} documents from {file_path}.")

        # Tokenize PDFs
        documents.extend(text_splitter.split_documents(pdf_docs))

    print(f"Tokenized into {len(documents)} chunks.")
    return documents

