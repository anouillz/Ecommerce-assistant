from langchain_core.tools import tool
from rag import rag

@tool
def find_wine_pairing(food_query: str) -> str:
    """
    Utilise cet outil quand l'utilisateur cherche un vin pour accompagner un plat spécifique.
    Input example : "raclette", "poisson", "fromage", "foie gras", "chasse", "fish", "cheese"
    """
    docs = rag.retriever.invoke(f"accord vin plat {food_query}")
    return format_docs(docs)

@tool
def check_wine_details(wine_name: str) -> str:
    """
    Utilise cet outil pour trouver des détails spécifiques sur un vin 
    ou pour vérifier la source exacte dans le document.
    Exemple d'input : "Fendant", "Pinot Noir", "Dahu".
    """
    docs = rag.retriever.invoke(wine_name)
    return format_docs(docs)

# format documents with sources 
def format_docs(docs):
    if not docs:
        return "Aucune information trouvée dans la base de données."
    
    formatted = []
    for doc in docs:
        source = doc.metadata.get('source', 'Inconnu').split('/')[-1]
        page = doc.metadata.get('page', '?')
        content = doc.page_content.replace('\n', ' ').strip()
        formatted.append(f"[Source: {source} | Page: {page}] Contenu: {content}")
        
    return "\n\n".join(formatted)


tools = [find_wine_pairing, check_wine_details]