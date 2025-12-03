from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langsmith import traceable
from config import PROMPT_TEMPLATE, K_RETRIEVAL

def setup_rag_chain(llm, retriever):
    # format documents for context
    def format_docs(docs):
        return "\n\n".join(
            f"Source: {doc.metadata.get('source', 'unknown')}, Page: {doc.metadata.get('page', 'unknown')}\nContent: {doc.page_content}"
            for doc in docs
        )

    rag_chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        | llm
        | StrOutputParser()
    )
    return rag_chain

def generate_response_with_rag(chain, query: str):
    response = chain.invoke(query)
    return {"text_response": response}

@traceable(name="Wine RAG Chain")  
def generate_response_with_rag_traced(chain, query: str):
    response = chain.invoke(query)
    return {"text_response": response}
