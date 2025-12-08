from typing import TypedDict, Annotated
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from langsmith import traceable
from dotenv import load_dotenv

from config import OLLAMA_MODEL, OLLAMA_ADDRESS, SYSTEM_PROMPT
from tools import tools

load_dotenv()

llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_ADDRESS,
    temperature=0.1, 
)
# link tools with llm
llm_with_tools = llm.bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[list, "add_messages"]

@traceable(name="Chatbot Node")
def chatbot_node(state: AgentState):
    messages = state["messages"]
    current_prompt = SYSTEM_PROMPT
    
    # check if last message is from a tool 
    if len(messages) > 0 and messages[-1].type == "tool":
        current_prompt += "\n\nINFORMATION IMPORTANTE : Tu viens de recevoir les données de l'outil ci-dessus. UTILISE-LES pour répondre à l'utilisateur MAINTENANT. Ne pose pas de questions."

    sys_msg = SystemMessage(content=current_prompt)
    
    # build context 
    full_context = [sys_msg] + messages
    
    response = llm_with_tools.invoke(full_context)
    return {"messages": [response]}

# langgraph
workflow = StateGraph(AgentState)
workflow.add_node("chatbot", chatbot_node)
workflow.add_node("tools", ToolNode(tools))

workflow.set_entry_point("chatbot")
workflow.add_conditional_edges("chatbot", tools_condition)
workflow.add_edge("tools", "chatbot")

memory = MemorySaver()
agent = workflow.compile(checkpointer=memory)

# generate agent graph image
img = agent.get_graph(xray=True).draw_mermaid_png()
with open("agent.png", "wb") as f:
    f.write(img)
