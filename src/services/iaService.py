import requests 

def query_ollama(prompt: str):
    response = requests.post('http://localhost:8000/generate', json={
        'model': 'deepseek-r1',
        'prompt': prompt,
        'stream': False
    })
    if response.status_code != 200:
        raise Exception(response.text)
    return response.json()["response"]