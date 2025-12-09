from typing import TypedDict, Annotated
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph.message import add_messages
from langsmith import traceable
from dotenv import load_dotenv

from config import OLLAMA_MODEL, OLLAMA_ADDRESS, SYSTEM_PROMPT
from tools import tools

load_dotenv()

llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_ADDRESS,
    temperature=0, 
)

#link tools with llm
llm_with_tools = llm.bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

@traceable(name="Chatbot Node")
def chatbot_node(state: AgentState):
    messages = state["messages"]
    sys_msg = SystemMessage(content=SYSTEM_PROMPT)
    full_context = [sys_msg] + messages
    
    if len(messages) > 0 and hasattr(messages[-1], 'type') and messages[-1].type == "tool":
        
        last_human_msg = None
        for m in reversed(messages):
            if m.type == "human":
                last_human_msg = m.content
                break
        
        if last_human_msg:
            reminder_text = f"""
            STOP ! Ne cherche plus. Tu as les infos. 
            Pas besoin de t'excuser. 
            Pas besoin de dire que tu utilises l'outil.
            Réponds UNIQUEMENT à ma question : "{last_human_msg}".
            Réponds dans la langue de cette question: "{last_human_msg}".
            Ignore les autres vins du texte s'ils ne correspondent pas.
            """
            full_context.append(HumanMessage(content=reminder_text))
        
        # use llm without tools to answer question with retrieved context
        response = llm.invoke(full_context)
        
    else:
        response = llm_with_tools.invoke(full_context)

    return {"messages": [response]}

#langgraph
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