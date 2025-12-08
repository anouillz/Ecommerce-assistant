import uuid
from rich.console import Console
from rich.markdown import Markdown
from langchain_core.messages import HumanMessage, AIMessage
from agent import agent
from langsmith import traceable

console = Console()

def main():
    console.print("[bold magenta]\nAssistant Sommelier IA")
    console.print("[dim]Type 'quit' to exit.\n")

    # thread for conversation memory
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    while True:
        try:
            user_input = console.input("[bold green]user : ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["quit", "exit", "bye"]:
                console.print("[yellow]Goodbye![/]")
                break

            # agent stream for steps
            events = agent.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config,
                stream_mode="values"
            )

            for event in events:
                messages = event["messages"]
                if not messages:
                    continue
                
                last_msg = messages[-1]
                
                # Display tool usage, debugging imfo
                if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                    for tool_call in last_msg.tool_calls:
                        console.print(f"[dim italic]Assistant is consulting: {tool_call['name']}...[/]")

                # Display final response
                if isinstance(last_msg, AIMessage) and last_msg.content:
                    # Avoid displaying empty content when calling a tool
                    if not last_msg.tool_calls: 
                        console.print("\n[bold cyan]Agent :")
                        console.print(Markdown(last_msg.content))

        except Exception as e:
            console.print(f"[bold red]Erreur : {e}[/]")

if __name__ == "__main__":
    main()