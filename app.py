from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Query required"})
    
    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    results = []
    for r in soup.find_all('div', class_='result', limit=5):
        title = r.find('a', class_='result__a')
        snippet = r.find('a', class_='result__snippet')
        results.append({
            "title": title.get_text() if title else "",
            "snippet": snippet.get_text() if snippet else "",
        })
    
    return jsonify({"query": query, "results": results})

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "API is running! 🔥"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)