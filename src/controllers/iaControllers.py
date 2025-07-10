from flask import request
from ..services.iaService import query_ollama

async def generate():
    data = request.get_json()
    print(data)
    if not data or not data.get('prompt'):
        return {"error": "Prompt is required"}, 400
    
    try:
        result = await query_ollama(data['prompt'])
        return {"response": result}
    except Exception as e:
        return {"error": f"Erreur lors de l'appel au modèle: {str(e)}"}, 500