from typing import TypedDict, Annotated
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, ToolMessage, HumanMessage
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
    all_messages = state["messages"]
    
    # seperate last human message index to focus on current turn
    last_human_index = -1
    for i in range(len(all_messages) - 1, -1, -1):
        if all_messages[i].type == "human":
            last_human_index = i
            break
            
    # only use messages from current turn for tool analysis
    if last_human_index != -1:
        current_turn_messages = all_messages[last_human_index:]
    else:
        current_turn_messages = all_messages # Cas rare (début absolu)

    # check tools called in this turn
    tool_calls_in_turn = [
        m.name for m in current_turn_messages 
        if isinstance(m, ToolMessage)
    ]
    
    has_wine_info = ("check_wine_details" in tool_calls_in_turn or 
                     "find_wine_pairing" in tool_calls_in_turn)
    
    has_checked_video = "get_wine_video_or_qr" in tool_calls_in_turn
    
    messages_to_send = [SystemMessage(content=SYSTEM_PROMPT)] + all_messages

    # agent has checked info but not video
    if has_wine_info and not has_checked_video:
        # On le force à continuer vers l'étape 2
        guidance = """
        [ETAPE SUIVANTE REQUISE]
        Tu as les informations sur le vin. C'est bien.
        MAIS tu n'as pas encore vérifié s'il existe un QR Code.
        
        Règle : Tu DOIS appeler l'outil `get_wine_video_or_qr` maintenant.
        Ne réponds pas encore à l'utilisateur. Appelle l'outil.
        """
        messages_to_send.append(HumanMessage(content=guidance))
        
    # agent checked for video, need to conclude using all data 
    elif has_checked_video:
        guidance = """
        [SYNTHÈSE FINALE]
        Parfait, tu as toutes les données (Infos techniques + Vérification vidéo effectuée).
        

        Maintenant, rédige la réponse complète pour l'utilisateur.
        N'oublie pas d'inclure le lien vidéo si tu en as trouvé un.
        Si tu n'as pas trouvé de lien, ne mets rien à ce sujet.
        """
        has_checked_video = False
        messages_to_send.append(HumanMessage(content=guidance))

    response = llm_with_tools.invoke(messages_to_send)
    return {"messages": [response]}

workflow = StateGraph(AgentState)
workflow.add_node("chatbot", chatbot_node)
workflow.add_node("tools", ToolNode(tools))

workflow.set_entry_point("chatbot")
workflow.add_conditional_edges(
    "chatbot",
    tools_condition,
)
workflow.add_edge("tools", "chatbot")

memory = MemorySaver()
agent = workflow.compile(checkpointer=memory)

# generate agent graph image
img = agent.get_graph(xray=True).draw_mermaid_png()
with open("agent.png", "wb") as f:
    f.write(img)