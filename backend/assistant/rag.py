from config import OLLAMA_MODEL, OLLAMA_ADDRESS, EMBEDDING_MODEL_NAME, VECTOR_STORE_PATH, PDF_FOLDER_PATH, K_RETRIEVAL as K

from langchain_ollama import ChatOllama 

from langchain_huggingface import HuggingFaceEmbeddings

from retrieve_data import create_vectorestore
from generate import setup_rag_chain, generate_response_with_rag

class Rag:
    def __init__(self):
        self.llm = ChatOllama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_ADDRESS,
            temperature=0.6,
        )

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

        self.chain = setup_rag_chain(self.llm, self.retriever)

    def generate_answer(self, query):
        # response only generated with the rag and no tools
        return generate_response_with_rag(self.chain, query)