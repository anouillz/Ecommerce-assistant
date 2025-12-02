from rag import Rag
from rich.console import Console
from rich.markdown import Markdown

def main():
    rag = Rag()
    console = Console()

    print("Welcome to the Wine Assistant! Type 'quit' to exit.")

    while True:
        query = input("\nAsk a question: ")

        if query.lower() == 'quit':
            print("exit assistant...")
            break

        response = rag.generate_answer(query)
        console.print(Markdown(response['text_response']))

if __name__ == "__main__":
    main()