from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Récupération des variables d'environnement (API_KEY et CX doivent être définies sur Render)
API_KEY = os.getenv("API_KEY")  # Stocké dans Render
CX = os.getenv("CX")  # Stocké dans Render

def search_google(query):
    """Effectue une recherche Google Custom Search et retourne les résultats."""
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX}&num=10"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Erreur API Google: {response.status_code}", "details": response.text}

def filter_valid_links(results):
    """Filtre les résultats pour récupérer les pages produits et les pages de recherche."""
    valid_sites = ["zalando", "zara", "asos", "jules", "celio", "b-z-b", "sarenza", "hm"]
    product_links, search_links = [], []
    
    if 'items' in results:
        for item in results['items']:
            link = item['link']
            if any(site in link for site in valid_sites):
                if (".html" in link or "/prd/" in link or "/dp/" in link or "p0000" in link or "productpage" in link or "product" in link or "products" in link):
                    product_links.append(link)
                else:
                    search_links.append(link)
    
    return product_links[:3], search_links[:3]

@app.route("/", methods=["GET"])
def home():
    """Route d'accueil pour vérifier que l'API fonctionne."""
    return jsonify({"message": "API en ligne et fonctionne ! 🚀"})

@app.route("/search", methods=["GET"])
def get_product_and_search_links():
    """Recherche des liens de produits et de pages de recherche en fonction d'un mot-clé."""
    search_query = request.args.get("query")
    
    if not search_query:
        return jsonify({"error": "Paramètre 'query' manquant"}), 400

    results = search_google(search_query)

    if "error" in results:
        return jsonify(results), 500  # Retourne l'erreur API Google

    product_links, search_links = filter_valid_links(results)
    return jsonify({"product_links": product_links, "search_links": search_links})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
