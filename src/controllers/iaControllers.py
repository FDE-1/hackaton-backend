from flask import request
from ..services.iaService import query_ollama
from ..controllers import scrapperControllers
def generate():
    url = request.get_json()
    data = scrapperControllers.get_data(url)
    # print(data)
    if not data or not data.get('prompt'):
        return {"error": "Prompt is required"}, 400
    
    try:
        result = query_ollama(data['prompt'])
        return {"response": result}
    except Exception as e:
        return {"error": f"Erreur lors de l'appel au modèle: {str(e)}"}, 500
    