from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama

import sys
import os

# set paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
assistant_dir = os.path.dirname(current_dir)

sys.path.append(assistant_dir)

from config import OLLAMA_MODEL, OLLAMA_ADDRESS

# evaluation is made by another LLM that grades the answers

# prompt for evaluation LLM
eval_instructions = "Tu es un expert pour évaluer des réponses d'éleves à des question sur le vin. Tu dois répondre par CORRECT si la réponse de l'élève est correcte et par INCORRECT sinon. Si la réponse de l'élèe contient partiellement la bonne réponse, réponds par CORRECT. Ne donne aucune explication, réponds uniquement par CORRECT ou INCORRECT."

def correctness(inputs: dict, outputs: dict, reference_outputs: dict) -> bool:    
    llm = ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_ADDRESS,
        temperature=0.1, 
    )

    user_content = f"""Tu évalues les réponses suivantes:
    {inputs['question']}
    
    Voici la bonne réponse:
    {reference_outputs['answer']}
    
    Tu évalues la réponse prédite suivante:
    {outputs.get('response', 'Pas de réponse fournie')}
    
    Réponds EXACTEMENT par 'CORRECT' ou 'INCORRECT':
    Grade:"""

    messages = [
        SystemMessage(content=eval_instructions),
        HumanMessage(content=user_content),
    ]

    ai_message = llm.invoke(messages)

    grade = ai_message.content.strip().upper()

    return "CORRECT" in grade

