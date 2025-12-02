import os

#OLLAMA_MODEL = "gpt-oss:20b"  
OLLAMA_MODEL = "llama3.1:8b"  

OLLAMA_ADDRESS = "http://localhost:11434"
EMBEDDING_MODEL_NAME = "BAAI/bge-large-en-v1.5"

VECTOR_STORE_PATH = os.path.abspath("data/vectorstore")
PDF_FOLDER_PATH = os.path.abspath("data/pdf")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
K_RETRIEVAL = 5

PROMPT_TEMPLATE = """
You are an assistant based on wine knowledge and recommendations.
Use the following pieces of context to answer the question at the end.
Don't invent your own answers, look for them in the context and only use the information you know.
Use three sentences maximum and keep the answer as concise as possible.
You **must** answer in the language of the question. 
Look for keywords in question and context. 
Make sure to give the name of the wines.
For recommendations, they usually are in the "acompagnement" section of the context. 


Context:
{context}

Question:
{input}


Answer:
"""
