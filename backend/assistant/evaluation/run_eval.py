import sys
import os
import uuid
from langchain_core.messages import HumanMessage
from langsmith.evaluation import evaluate
from dotenv import load_dotenv
from evaluate import correctness

current_dir = os.path.dirname(os.path.abspath(__file__))
assistant_dir = os.path.dirname(current_dir)

sys.path.append(assistant_dir)

from config import OLLAMA_MODEL, OLLAMA_ADDRESS
from agent import agent

load_dotenv()

# chatbot agent as target for evaluation
def target_agent(inputs: dict):
    question = inputs["question"]

    # threads for context retention
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    result = agent.invoke(
        {"messages": [HumanMessage(content=question)]},
        config=config 
    )
    
    last_message = result["messages"][-1]
    return {"response": last_message.content}


if __name__ == "__main__":
    dataset_name = "wine_evaluation" 
    
    print(f"Lancement de l'évaluation sur '{dataset_name}'...")
    
    # evaluation in langsmith
    results = evaluate(
        target_agent,              
        data=dataset_name,         
        evaluators=[correctness],  
        experiment_prefix="test-vins", 
        max_concurrency=1         
    )
    
    print("\n éval terminée")