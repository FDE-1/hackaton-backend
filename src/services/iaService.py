import requests 
import json
import re

prompt_request = "– Donne moi un json sous cette forme : {\nMoyenne des notes parmi tous les avis récoltés ,Nombre d’avis total ,Les sujets les plus récurrents dans les avis sous format « top 5 » ({ '1' : « transport », '2' : « livraison », …}),Le Nombre d’avis négatif avec les avis associé (ex : { 'nb' : 6, 'avis' : }),Le Nombre d’avis neutre avec les avis associé (ex : { 'nb' : 6, 'avis' : { }}),Le Nombre d’avis positif avec les avis associé (ex : { 'nb' : 6, 'avis' : { }})}. Le résultat devra être un json valide. Retourne moi uniquement je json. Lis bien tout ce que je t'envoie n'hallucine pas"
def query_ollama(prompt: str):
    final_prompt = json.dumps(prompt) + prompt_request
    response = requests.post('http://localhost:8000/generate', json={
        'model': 'deepseek-r1',
        'prompt': final_prompt,
        'stream': False
    })
    if response.status_code != 200:
        raise Exception(response.text)
    
    response_data = response.json()
    response_text = response_data.get("response", "")
    
    # Extraire le contenu entre ```json
    json_match = re.search(r'```json\n([\s\S]*?)\n```', response_text)
    if not json_match:
        raise ValueError("Aucun contenu JSON trouvé dans la réponse")
    
    # Parser le contenu JSON extrait
    json_content = json_match.group(1)
    print(json_content)
    return json.loads(json_content)
    #return response.json()["response"]