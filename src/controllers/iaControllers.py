from fastapi import HTTPException
from pydantic import BaseModel
from ..services.iaService import query_ollama

class PromptRequest(BaseModel):
    prompt: str

async def generate(request: PromptRequest):
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    
    try:
        result = await query_ollama(request.prompt)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'appel au modèle: {str(e)}")