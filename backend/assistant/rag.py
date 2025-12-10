from data_handling.retrieve_data import create_vectorestore

from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL_NAME, PDF_FOLDER_PATH, VECTOR_STORE_PATH, K_RETRIEVAL as K

class Rag:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        self.vectorstore = create_vectorestore(self.embedding_model, VECTOR_STORE_PATH, PDF_FOLDER_PATH)
        self.retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": K}
        )


rag = Rag()