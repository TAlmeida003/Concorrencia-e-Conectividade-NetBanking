import asyncio
import aiohttp

API1 = "http://192.168.0.105:3050"
API2 = "http://127.0.0.1:3051"
API3 = "http://127.0.0.1:3052"
API4 = "http://127.0.0.1:3053"
API5 = "http://127.0.0.1:3054"
API6 = "http://127.0.0.1:3055"
API7 = "http://127.0.0.1:3056"
API8 = "http://127.0.0.1:3057"
API9 = "http://127.0.0.1:3058"
API10 = "http://127.0.0.1:3059"



async def fazer_requisicao(url, timeout):
    timeout_setting = aiohttp.ClientTimeout(total=timeout)
    async with aiohttp.ClientSession(timeout=timeout_setting) as session:
        try:
            async with session.post(url) as response:
                return await response.text(encoding='utf-8')
        except asyncio.TimeoutError:
            return f"Timeout occurred for {url}"

async def main():
    urls = [
        f"{API1}/proposer/" + {"mgs_teste: ": "oi"}.__str__(),
        f"{API2}/proposer/" + {"mgs_teste: ": "sam"}.__str__(),
        f"{API3}/proposer/" + {"mgs_teste: ": "tchau"}.__str__(),
        f"{API1}/proposer/" + {"mgs_teste: ": "Bem-vindo"}.__str__(),
        f"{API2}/proposer/" + {"mgs_teste: ": "adeus"}.__str__(),
        f"{API3}/proposer/" + {"mgs_teste: ": "silvio"}.__str__(),
        # f"{API7}/proposer/foi",
        # f"{API8}/proposer/porta",
        # f"{API9}/proposer/aberta",
        # f"{API10}/proposer/hj",
    ]
    timeout = 30  # Define o timeout em segundos
    tasks = [fazer_requisicao(url, timeout) for url in urls]
    resultados = await asyncio.gather(*tasks)
    for resultado in resultados:
        print(resultado)

asyncio.run(main())
