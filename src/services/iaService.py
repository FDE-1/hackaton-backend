import requests 

prompt_request = "– Donne moi un json sous cette forme : {\nMoyenne des notes parmi tous les avis récoltés (ex : note : 3,4),Nombre d’avis total (ex : 147),Les sujets les plus récurrents dans les avis sous format « top 5 » (ex : { 1 : « transport », 2 : « livraison », …}),Le Nombre d’avis négatif avec les avis associé (ex : { nb : 6, avis : { « c’est de la merde », « nul »…}}),Le Nombre d’avis neutre avec les avis associé (ex : { nb : 6, avis : { « c’est de la merde », « nul »…}}),Le Nombre d’avis positif avec les avis associé (ex : { nb : 6, avis : { « c’est de la merde », « nul »…}})}"

def query_ollama(prompt: str):
    final_prompt = prompt + prompt_request
    response = requests.post('http://localhost:8000/generate', json={
        'model': 'deepseek-r1',
        'prompt': final_prompt,
        'stream': False
    })
    if response.status_code != 200:
        raise Exception(response.text)
    return response.json()["response"]