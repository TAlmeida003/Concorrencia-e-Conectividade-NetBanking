import asyncio
import json
import random
import aiohttp


async def fazer_requisicao(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            resposta = await response.text(encoding='utf-8')
            response_json = json.loads(resposta)
            print(response_json, response.status)


async def main(urls):
    tasks = [fazer_requisicao(url[0], url[1]) for url in urls]
    await asyncio.gather(*tasks)


API1 = "http://172.16.103.1:3050"
API2 = "http://172.16.103.2:3050"
API3 = "http://172.16.103.4:3050"
API4 = "http://172.16.103.5:3050"

user = [
    {"name": "Thiago Neri", "num_cadastro": "123.123.123-01", "user_name": "thiago001", "password": "12345678",
     "type_person": "PF"},
    {"name": "Samara Ferreira", "num_cadastro": "123.123.123-02", "user_name": "mara21", "password": "12345678",
     "type_person": "PF"},
    {"name": "Silvio Azevedo", "num_cadastro": "123.123.123-03", "user_name": "juninho123", "password": "12345678",
     "type_person": "PF"},
    {"name": "Americanas", "num_cadastro": "12.123.123/0001-01", "user_name": "americanas001",
     "password": "12345678", "type_person": "PJ"},
    {"name": "Thiago Neri", "num_cadastro": "123.123.123-01", "user_name": "thiago001", "password": "12345678",
     "type_person": "PF"},
    {"name": "Samara Ferreira", "num_cadastro": "123.123.123-02", "user_name": "mara21", "password": "12345678",
     "type_person": "PF"}
]

urls = [
    (f"{API1}/register-customer", user[0]),
    (f"{API2}/register-customer", user[1]),
    (f"{API3}/register-customer", user[2]),
    (f"{API4}/register-customer", user[3]),
    (f"{API3}/register-customer", user[4]),
    (f"{API4}/register-customer", user[5])
]

asyncio.run(main(urls))
