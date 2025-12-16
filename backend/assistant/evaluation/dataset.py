from dotenv import load_dotenv 
from langsmith import Client

load_dotenv()

client = Client()

from langsmith import Client

client = Client()

# register dataset
dataset_name = "wine_evaluation_v4"
dataset = client.create_dataset(dataset_name)

client.create_examples(
    dataset_id=dataset.id,
    examples = [
        {
            "inputs": {"question": "Quel vin suggères-tu pour accompagner de la cuisine chinoise ?"},
            "outputs": {"answer": "Vous pouvez opter pour le Dahu Rosé [Source: Page 47] ou le Château Conthey (Sauvignon/Chardonnay) [Source: Page 57], qui s'accordent tous deux avec la cuisine chinoise."},
        },
        {
            "inputs": {"question": "Je vais manger une charbonnade. As-tu un vin rouge à me conseiller ?"},
            "outputs": {"answer": "Oui, la Syrah AOC Valais [Source: Page 23] ou la Cuvée Rouge Barrique [Source: Page 83] sont recommandées pour accompagner une charbonnade."},
        },
        {
            "inputs": {"question": "Quel vin servir avec une terrine de foie de volaille ?"},
            "outputs": {"answer": "L'Humagne Blanche AOC Valais est un excellent choix pour les terrines de foie de volaille [Source: Page 61]."},
        },
        {
            "inputs": {"question": "Un vin pour accompagner des huîtres ?"},
            "outputs": {"answer": "Je recommande le Petite Arvine AOC Valais [Source: Page 64] ou le Sans Culotte Fendant [Source: Page 85] qui se marient très bien avec les huîtres."},
        },
        {
            "inputs": {"question": "Quels sont les cépages utilisés pour le Clos du Château ?"},
            "outputs": {"answer": "Le Clos du Château est un assemblage de Pinot Noir et de Merlot [Source: Page 73]."},
        },
        {
            "inputs": {"question": "Comment est vinifiée la Dôle Blanche AOC Valais ?"},
            "outputs": {"answer": "La Dôle Blanche est vinifiée par saignée (un vin obtenu par saignée) [Source: Page 9]."},
        },
        {
            "inputs": {"question": "Quel est le terroir spécifique du Cornalin AOC Valais ?"},
            "outputs": {"answer": "Le terroir du Cornalin se situe à Sion, notamment au Domaine Les Balettes [Source: Page 81]."},
        },
        {
            "inputs": {"question": "Quelle est le prix du Saint-Eloi, Johannisberg doux AOC Valais ?"},
            "outputs": {"answer": "Son prix est de 19,50 CHF"},
        },
        {
            "inputs": {"question": "Quels arômes peut-on sentir dans le Viognier AOC Valais ?"},
            "outputs": {"answer": "Le Viognier présente un nez intense de fleurs d'oranger, de lilas, ainsi que des arômes d'abricot, de pêche et une note d'amande [Source: Page 19]."},
        },
        {
            "inputs": {"question": "Décris-moi le nez du Cornalin."},
            "outputs": {"answer": "Le Cornalin a un nez de fruits noirs (cerise noire, myrtille, sureau) avec des notes de cacao, de café grillé et de chocolat noir [Source: Page 25]."},
        },
        {
            "inputs": {"question": "À quoi ressemble le Dahu Frisé ?"},
            "outputs": {"answer": "Le Dahu Frisé a une robe abricot et est un vin mousseux de Pays Suisse, avec des bulles élégantes et fines. Il présente un bouquet de fleurs et de fruits, et est sec, frais et revigorant. [Source: vins_2021.pdf | Page: 50]"},
        },
        {
            "inputs": {"question": "À quelle température doit-on servir le Syrah Grand Cru ?"},
            "outputs": {"answer": "Le Syrah Grand Cru se sert idéalement entre 16 et 18°C [Source: Page 41]."},
        },
        {
            "inputs": {"question": "Combien de temps peut-on garder le Cuvée Or, Grain Noble ConfidenCiel ?"},
            "outputs": {"answer": "Le Cuvée Or a un extraordinaire potentiel de garde de plus de 10 ans [Source: Page 95]."},
        },
        {
            "inputs": {"question": "Est-ce que le Sans Culotte Fendant est un vin de garde ?"},
            "outputs": {"answer": "Non, le Sans Culotte Fendant s'apprécie de préférence jeune [Source: Page 85]."},
        },
        {
            "inputs": {"question": "Donne moi des vins pour accompagner une raclette."},
            "outputs": {"answer": "Soleil du Valais, Heida, Sans Culotte"},
        },
        {
            "inputs": {"question": "Peux tu me donner la capitale de la Suisse ?"},
            "outputs": {"answer": "Désolé, je ne peux que vous aider pour des questions de vin. Je suis incapable de répondre à votre question."},
        },
        {
            "inputs": {"question": "Quelle est la teneur en alcool du Coquet, Gamay ?"},
            "outputs": {"answer": "13%"},
        },
        {
            "inputs": {"question": "Avec quels mets accompagner le Château Conthey, Sauvignon, Chardonnay AOC Valais ?"},
            "outputs": {"answer": "Apéritif, entrées fines en tous genres, terrines de poissons, melon et jambon, saumon fumé, poissons grillés, cuisine chinoise"},
        },
        {
            "inputs": {"question": "Quelle est la quantité minimale pour pouvoir commander le Cornalin Nobles Cépages, AOC Valais?"},
            "outputs": {"answer": "La quantité minimale est de 6 bouteilles."},
        }
    ]
)