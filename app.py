from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "AIzaSyDNnviCjlkFgMEQhW5aJ-ft8blZIF69pv8"
CX = "93648fcd23f714740"

def search_google(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX}&num=10"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def filter_valid_links(results):
    valid_sites = ["zalando", "zara", "asos", "jules", "celio", "b-z-b", "sarenza", "hm"]
    product_links, search_links = [], []
    
    if 'items' in results:
        for item in results['items']:
            link = item['link']
            if any(site in link for site in valid_sites):
                if (".html" in link or "/prd/" in link or "/dp/" in link or "p0000" in link or "productpage" in link):
                    product_links.append(link)
                else:
                    search_links.append(link)
    
    return product_links[:3], search_links[:3]

@app.route("/search", methods=["GET"])
def get_product_and_search_links():
    search_query = request.args.get("query")
    
    if not search_query:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    results = search_google(search_query)
    
    if results:
        product_links, search_links = filter_valid_links(results)
        return jsonify({"product_links": product_links, "search_links": search_links})
    else:
        return jsonify({"error": "No results found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)