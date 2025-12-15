from langchain_community.vectorstores import FAISS

from rich.console import Console
from pathlib import Path 

from data_handling.load_data import load_chunk_documents 

console = Console()

def create_vectorestore(embedding_model, vector_store_path, pdf_folder_path, url, base_url):
    vector_store_path = Path(vector_store_path)
    pdf_folder_path = Path(pdf_folder_path)
    #load and store vectors
    if vector_store_path.exists():
        console.print("Loading existing vectorstore...")
        vectorstore = FAISS.load_local(str(vector_store_path), embedding_model, allow_dangerous_deserialization=True)
    else:
        console.print("Creating new vectorstore...")
        doc_list = [str(p) for p in pdf_folder_path.glob("*.pdf")]
        documents = load_chunk_documents(doc_list, url, base_url)
        vectorstore = FAISS.from_documents(documents=documents, embedding=embedding_model)
        vectorstore.save_local(str(vector_store_path))
        console.print("Vectorstore saved.")

    return vectorstore



