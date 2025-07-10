from flask import Blueprint, request
from ..controllers.iaControllers import generate

ia_routes = Blueprint('ia_routes', __name__)

@ia_routes.route('/generate', methods=['POST'])
def generate_route():
    return generate()