from flask import request
from ..services.iaService import query_ollama
from ..services import scarpperService
from ..controllers import scrapperControllers
def generate():
    url = request.get_json()
    data, status = scrapperControllers.get_data(url["url"])
    # tmp = scarpperService.scrape_cultura_reviews( "https://www.cultura.com/p-logitech-gaming-mouse-g203-lightsync-souris-optique-6-boutons-filaire-usb-noir-5099206089167.html")
    # return tmp
    if not data :
        return {"error": "Prompt is required"}, 400
    
    try:
        result = query_ollama(data.get_json())
        return {"response": result}
    except Exception as e:
        return {"error": f"Erreur lors de l'appel au modèle: {str(e)}"}, 500
    