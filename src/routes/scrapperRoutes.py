from flask import Blueprint
from ..controllers import scrapperControllers

scrapper = Blueprint('scapper_routes', __name__)

@scrapper.route('/scrapper/<path:url>', methods=['GET'])
def get_data(url):
    return scrapperControllers.get_data(url)
