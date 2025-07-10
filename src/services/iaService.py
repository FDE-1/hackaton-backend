import aiohttp

async def query_ollama(prompt: str):
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8000/generate', json={
            'model': 'deepseek-r1',
            'prompt': prompt,
            'stream': False
        }) as response:
            if response.status != 200:
                raise Exception(await response.text())
            return (await response.json())["response"]