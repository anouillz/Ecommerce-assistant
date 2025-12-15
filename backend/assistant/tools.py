from langchain_core.tools import tool
from data_handling.qr_retriever import extract_qr_from_page
from config import PDF_FOLDER_PATH
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


@tool
def get_wine_video_or_qr(wine_name: str) -> str:
    """
    Utilise cet outil quand l'utilisateur demande une VIDÉO, un LIEN, ou un QR CODE sur un vin.
    Utilise cet outil aussi quand l'utilisateur demande des détails sur un vin et qu'une vidéo pourrait être disponible.
    Ne l'utilise pas pour des infos textuelles.
    Input: Le nom du vin (ex: "Fendant", "Heida", "Syrah").
    """
    # page name
    docs = rag.retriever.invoke(wine_name)
    
    if not docs:
        return "Désolé, je n'ai pas trouvé ce vin dans le catalogue."
    
    # get best matching doc
    best_doc = docs[0]
    page_num = best_doc.metadata.get('page')
    
    if page_num is None:
        return "Impossible de localiser la page de ce vin."

    full_path = f"{PDF_FOLDER_PATH}/vins_2021.pdf"
    
    # get url from qr code
    url = extract_qr_from_page(full_path, int(page_num))
    
    if url:
        return f"J'ai trouvé un code QR sur la fiche du {wine_name} ! Voici le lien vidéo/info : {url}"
    else:
        return f"J'ai vérifié la fiche du {wine_name} (Page {page_num}), mais je n'ai pas trouvé de QR code dessus."

# format documents with sources 
def format_docs(docs):
    if not docs:
        return "Aucune information trouvée dans la base de données."
    
    formatted = []
    for doc in docs:
        source = doc.metadata.get('source', 'Inconnu').split('/')[-1]
        page = doc.metadata.get('page', '?')
        content = doc.page_content.replace('\n', ' ').strip()
        language = doc.metadata.get('language')
        if source.lower().endswith("pdf"):
            formatted.append(f"[Source: {source} | Page: {page}] | langue: {language} Contenu: {content}")
        else:
            formatted.append(f"[Source: Voir la source du produit]({doc.metadata.get('source')}) | langue: {language} Contenu: {content}")

    return "\n\n".join(formatted)


tools = [find_wine_pairing, check_wine_details, get_wine_video_or_qr]