from config import K_RETRIEVAL, PDF_FOLDER_PATH

from langchain_community.vectorstores import FAISS

from typing import List, Dict
from rich.console import Console
from pathlib import Path 

from load_data import load_chunk_documents 

console = Console()

#TODO add web links when it is implemented in load_data.py
def create_vectorestore(embedding_model, vector_store_path, pdf_folder_path, web_links: List[str] = None):
    vector_store_path = Path(vector_store_path)
    pdf_folder_path = Path(pdf_folder_path)
    #load and store vectors
    if vector_store_path.exists():
        console.print("Loading existing vectorstore...")
        vectorstore = FAISS.load_local(str(vector_store_path), embedding_model, allow_dangerous_deserialization=True)
    else:
        console.print("Creating new vectorstore...")
        doc_list = [str(p) for p in pdf_folder_path.glob("*.pdf")]
        documents = load_chunk_documents(doc_list)
        vectorstore = FAISS.from_documents(documents=documents, embedding=embedding_model)
        vectorstore.save_local(str(vector_store_path))
        console.print("Vectorstore saved.")

    return vectorstore


def retrieve_relevant_docs(vectorstore: FAISS, query: str, top_k: int = K_RETRIEVAL) -> List[Dict]:
    """
    Embed query and retrieve top-k docs with sources.
    """
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
    return retriever.get_relevant_documents(query)


