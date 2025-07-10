from flask import jsonify
from ..services import scarpperService
from urllib.parse import urlparse

def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc])
    except Exception:
        return False
    
def get_data(url):
    if is_valid_url(url):
        data = scarpperService.scrape_cdiscount_reviews_paginated(url)
        if data:
            return jsonify(data), 200
        return jsonify({"error": "donnée non trouvé"}), 404
    return jsonify({"error": "url non valide"}), 400