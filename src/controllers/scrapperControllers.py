from flask import jsonify
from ..services import scarpperService

def get_data(url):
    data = scarpperService.scrape_cdiscount_reviews_paginated(url)
    if data:
        return jsonify(data), 200
    return jsonify({"error": "data not found"}), 404
