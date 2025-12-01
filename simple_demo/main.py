from utils import start_ollama_server, pull_model, stop_ollama_server
from get_data import load_data, store_vectors

from pathlib import Path
import json
from langdetect import detect  

from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama  
from langchain.tools import tool  
from rich.console import Console
from rich.markdown import Markdown
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv(override=True)
console = Console()

OLLAMA_ADDRESS = "http://localhost:11434" 
model_name = "llama3.1:8b"

llm = ChatOllama(
    model=model_name,
    base_url=OLLAMA_ADDRESS,
    temperature=0.6, # temperature controls randomness in output, closer to 0 is more deterministic
)

EMBEDDING_MODEL_NAME = "BAAI/bge-large-en-v1.5"
#embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL_NAME,
    # to use the "cuda" configuration, you need an nvidia GPU, and to install 
    # On Kaggle, you set to use as accelerator GPU P100 (you need a verified account)
    # model_kwargs={"device": "cpu"}, # change to cuda -> cpu if you do not have a Nvdia GPU
    model_kwargs={"device": "cpu"}, # change to mps for MacOS M1/M2
    encode_kwargs={"normalize_embeddings": True},
)

#documents
documents = []
VECTORSTORES_DIR = Path("simple_demo/data/vectorstores_pdf")

prompt = """
You are an agent based on wine knowledge and recommendations.
Use the following pieces of context to answer the question at the end.
Don't try to make up an answer and only use the information you know.
Use three sentences maximum and keep the answer as concise as possible.
You must answer in the language of the question. 
Look for keywords in question and context. 
Make sure to give the name of the wines.
Don't invent your own answers, look for them in the context. 
For recommendations, they usually are in the "acompagnement" section of the context. 
Context:
{context}

Question:
{input}

Answer:
"""

prompt_template = PromptTemplate(input_variables=["context", "input"], template=prompt)
prompt_template

#load and store vectors
if VECTORSTORES_DIR.exists():
    console.print("Loading existing vectorstore...")
    vectorstore = FAISS.load_local(str(VECTORSTORES_DIR), embedding_model, allow_dangerous_deserialization=True)
else:
    console.print("Creating new vectorstore...")
    documents = load_data()
    vectorstore = FAISS.from_documents(documents=documents, embedding=embedding_model)
    vectorstore.save_local(str(VECTORSTORES_DIR))
    console.print("Vectorstore saved.")


# Top k of chunks to retrieve from the vectorstore
NB_RETRIVED_CHUNKS = 30

question_answer_chain = create_stuff_documents_chain(llm=llm, prompt=prompt_template)
retriever = vectorstore.as_retriever(
    search_type="mmr", #  Can be "similarity" (default), "mmr", or "similarity_score_threshold".
    search_kwargs={
        "k": NB_RETRIVED_CHUNKS,
    }
)

chain_with_retriever = create_retrieval_chain(retriever, question_answer_chain)


@tool
def food_pairing_tool(query: str) -> str:
    """
    Provides wine pairing recommendations for a given food question.
    Use this tool when the user asks for wine recommendations based on food. Pass the full question as query.
    """
    result = chain_with_retriever.invoke(input={"input": query})
    return result["answer"]

@tool
def wine_type_tool(query: str) -> str:
    """
    Filters wines based on their type (white or red) and retrieves relevant information. 
    Use this tool ONLY when the query explicitly mentions white or red wine."
    """
    # Multilingual keywords for wine types
    wine_keywords = {
        "en": {"white": "white", "red": "red"},
        "fr": {"white": "blanc", "red": "rouge"},
    }

    try:
        # Detect the language of the query
        language = detect(query)
        if language not in wine_keywords:
            return "Unsupported language for wine type filtering."

        # Check if the query specifies "white" or "red" in the detected language
        wine_type = None
        if wine_keywords[language]["white"] in query.lower():
            wine_type = wine_keywords[language]["white"]
        elif wine_keywords[language]["red"] in query.lower():
            wine_type = wine_keywords[language]["red"]

        if wine_type:
            filtered_query = f"{query} {wine_type}"
            result = chain_with_retriever.invoke(input={"input": filtered_query})
            return result["answer"]
        else:
            # no relevant wine type mentioned
            return "This tool is only for queries explicitly mentioning white or red wines."
    except Exception as e:
        return f"Error detecting language: {str(e)}"


available_functions = {
    "food_pairing_tool": food_pairing_tool,
    "wine_type_tool": wine_type_tool,
}

tools = [
    {
        "type": "function",
        "function": {
            "name": name,
            "description": func.__doc__,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The full user question."},
                },
                "required": ["query"],
            },
        },
    }
    for name, func in available_functions.items()
]

def answer_question(user_question: str):
    messages = [
        {"role": "system", "content": "You are a wine recommendation assistant. Answer in the language of the user's question. Use tools only when the query explicitly requires their functionality. For example, use the wine_type_tool only when the user mentions white or red wine. Otherwise, answer the question directly."},
        {"role": "user", "content": user_question}
    ]
    response = llm.invoke(messages, tools=tools)

    #console.print("Tool Calls:", json.dumps(response.tool_calls, indent=2))  # Pretty print tool calls

    if response.tool_calls:
        tool_call = response.tool_calls[0]
        function_name = tool_call["name"]
        arguments = tool_call["args"]

        # Validate tool call relevance
        if function_name == "wine_type_tool" and not any(keyword in user_question.lower() for keyword in ["white", "red", "blanc", "rouge"]):
            #console.print("Invalid tool call. Falling back to direct answer.")
            result = chain_with_retriever.invoke(input={"input": user_question})
            return result["answer"]

        if function_name in available_functions:
            function_output = available_functions[function_name].invoke(arguments)
            return function_output
    
    # If no tool called, fall back to direct RAG
    print("No tool called, using direct RAG.")
    result = chain_with_retriever.invoke(input={"input": user_question})
    #console.print(result)
    return result["answer"]

def main():
    #ollama_process = start_ollama_server()
 
    #pull_model(model_name)

    print("What is your question? (type 'quit' to exit)")
    while True:
        user_question = input(">> ")
        if user_question.lower() == 'quit':
            break
        answer = answer_question(user_question)
        console.print(Markdown(answer))

if __name__ == "__main__":
    main()