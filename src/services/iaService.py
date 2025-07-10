import requests 
import json
import re
from openai import OpenAI

prompt_request = "– Donne moi un json sous cette forme : {\nMoyenne des notes ,Nombre d’avis total ,Les sujets les plus récurrents dans les avis({ '1' : « transport », '2' : « livraison », …, '5' : ...}),Le Nombre d’avis négatif (ex : { 'nb' : 6, 'avis' :[...] }),Le Nombre d’avis positif (ex : { 'nb' : 6, 'avis' : [...] })}. Le résultat devra être un json valide. Retourne moi uniquement je json. Donne moi toutes les données et tous les avis en entier il ne faut aucun '...'. Lis bien tout ce que je t'envoie n'hallucine pas. Continue jusqu'à que tu fini ce que je t'ai demandé."
def query_ollama(prompt: str):
    final_prompt = json.dumps(prompt) + prompt_request
    print(final_prompt)
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",

    )

    completion = client.chat.completions.create(

        model="openai/gpt-4o",

        messages=[

            {

            "role": "user",

            "content": final_prompt

            }

        ]

    )
    response = completion.choices[0].message.content
    print(response)
    # Extraire le contenu entre ```json
    json_match = re.search(r'```json\n([\s\S]*?)\n```', response)
    if not json_match:
        raise ValueError("Aucun contenu JSON trouvé dans la réponse")
    
    # Parser le contenu JSON extrait
    json_content = json_match.group(1)
    data = json.loads(json_content)
    data["name"] = "Souris Gamer Filaire Logitech G203 LIGHTSYNC"
    data["description"] = "Souris gaming avec capteur optique, rétroéclairage RGB personnalisable et design ergonomique."
    return data
    #return response.json()["response"]