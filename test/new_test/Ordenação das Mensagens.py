import asyncio
import random
import aiohttp

LIST_NODES: list = [
    '172.16.103.1',
    '172.16.103.2',
    '172.16.103.3',
    '172.16.103.4',
    '172.16.103.5',
    '172.16.103.6',
    '172.16.103.7',
    '172.16.103.8',
    '172.16.103.9',
    '172.16.103.10',
    '172.16.103.11',
    '172.16.103.12',
    '172.16.103.13',
    '172.16.103.14'
]

PORT: int = 3050


async def fazer_requisicao(url):
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as response:
            return await response.text(encoding='utf-8')


async def main(list_URLs):
    tasks = [fazer_requisicao(url) for url in list_URLs]
    await asyncio.gather(*tasks)


msgs = ["oi", "sam", "tchau", "Bem-vindo", "silvio", "thiago", "mara", "juninho", "silvio", "mara"]

list_urls = []

for c in msgs:
    list_urls.append(f"http://{LIST_NODES[random.randint(0, len(LIST_NODES) - 1)]}:{PORT}/proposer/" + {"mgs_teste: ": c}.__str__())

asyncio.run(main(list_urls))
