import asyncio
import json

import aiohttp

API1 = "http://127.0.0.1:3050"
API2 = "http://127.0.0.1:3051"
API3 = "http://127.0.0.1:3052"
API4 = "http://127.0.0.1:3053"
API5 = "http://127.0.0.1:3054"
API6 = "http://127.0.0.1:3055"
API7 = "http://127.0.0.1:3056"
API8 = "http://127.0.0.1:3057"
API9 = "http://127.0.0.1:3058"
API10 = "http://127.0.0.1:3059"


async def fazer_requisicao(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            resposta = await response.text(encoding='utf-8')
            response_json = json.loads(resposta)
            return response_json


async def main():
    urls = [
        (f"{API1}/register-customer",
         {"name": "Thiago Neri", "num_cadastro": "123.123.123-01", "user_name": "thiago001", "password": "12345678",
          "type_person": "PF"}),
        (f"{API2}/register-customer",
         {"name": "Samara ferreira", "num_cadastro": "123.123.123-01", "user_name": "samara001", "password": "12345678",
          "type_person": "PF"}),
        (f"{API3}/register-customer",
         {"name": "Maria", "num_cadastro": "123.123.123-03", "user_name": "maria001", "password": "12345678",
          "type_person": "PF"}),
        (f"{API1}/register-customer",
         {"name": "Americanas", "num_cadastro": "12.123.123/0001-01", "user_name": "americanas001",
          "password": "12345678", "type_person": "PJ"}),
    ]
    tasks = [fazer_requisicao(url[0], url[1]) for url in urls]
    resultados = await asyncio.gather(*tasks)
    for resultado in resultados:
        print(resultado)


asyncio.run(main())
