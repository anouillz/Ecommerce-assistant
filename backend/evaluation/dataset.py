import os
from dotenv import load_dotenv 
from langsmith import Client

load_dotenv()

client = Client()

# register dataset
dataset_name = "wine_evaluation_dataset"
dataset = client.create_dataset(dataset_name)

from langsmith import Client

client = Client()

dataset_name = "wine_evaluation"
dataset = client.create_dataset(dataset_name)

client.create_examples(
    dataset_id=dataset.id,
    examples=[
        {
            "inputs": {"question": "Un bon vin pour accompagner une raclette ?"},
            "outputs": {"answer": "Soleil du Valais, Fendant AOC Valais - Heida AOC Valais - Brûlefer, Fendant de Sion AOC Valais - Sans Culotte, Fendant, AOC VALAIS"},
        },
        {
            "inputs": {"question": "Décris moi le vin Soleil du Valais."},
            "outputs": {"answer": "Vin blanc sec, élevé en cuve. Nez fin, élégant, minéral, tilleul, sensations fruitées. Potentiel de garde 1 à 3 ans. Accompagnements: apéritifs, raclette, mets au fromage, vianmde séchée, poissons du lac. "},
        },
        {
            "inputs": {"question": "Avec quel plat je peux accompagner un Heida AOC Valais ?"},
            "outputs": {"answer": "Le Heida AOC Valais s'accompagne bien avec des apéritifs, les viandes froides, les asperges et la raclette."},
        },
        {
            "inputs": {"question": "Où est le terroir de la Petite Arvine AOC Valais ?"},
            "outputs": {"answer": "Le terroir de la Petite Arvine AOC Valais se trouve à Sion."},
        },
        {
            "inputs": {"question": "Quel cépage est utilisé pour le Blandice blanc AOC Valais ?"},
            "outputs": {"answer": "Les cépages sont l'ermitage, amigne et petite arvine"},
        },
        {
            "inputs": {"question": "Comment conserver un Terra Cotta, Pinot noir AOC Valais ?"},
            "outputs": {"answer": "Le Terra Cotta, Pinot noir AOC Valais se bonifie durant les 3 à 4 prochaines années et se sert à une température de 14-15°C."},
        }
    ]
)