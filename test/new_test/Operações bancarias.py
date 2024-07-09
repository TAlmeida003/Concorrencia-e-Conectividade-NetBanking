import json
import asyncio
import aiohttp
import requests


def post_request(route, base_url, data):
    url = f"{base_url}/{route}"
    response = requests.post(url, json=data)
    print(response.json(), response.status_code)
    return response.json()


def get_request(route, base_url, data):
    url = f"{base_url}/{route}"
    response = requests.get(url, json=data)
    print(response.json(), response.status_code)
    return response.json()


async def fazer_requisicao(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            resposta = await response.text(encoding='utf-8')
            response_json = json.loads(resposta)
            print(response_json)
            return response_json


async def main(urls):
    tasks = [fazer_requisicao(url[0], url[1]) for url in urls]
    await asyncio.gather(*tasks)


API1 = "http://172.16.103.1:3050"
API2 = "http://172.16.103.2:3050"
API3 = "http://172.16.103.3:3050"
API4 = "http://172.16.103.4:3050"

# ======================================================================================================================
# Login do usuário 1, 2 e 3
user1 = get_request("login", API2,
                    {"user_name": "thiago001", "password": "12345678"})
user2 = get_request("login", API1,
                    {"user_name": "mara21", "password": "12345678"})
user3 = get_request("login", API3,
                    {"user_name": "juninho123", "password": "12345678"})

contas_thiago = []
pix_thiago = []
for cont_bank in user1['data']['accounts']:
    if user1['data']['accounts'][cont_bank]:
        contas_thiago.append(user1['data']['accounts'][cont_bank][0][0])
        pix_thiago.append(user1['data']['accounts'][cont_bank][0][2])

contas_samara = []
pix_samara = []
for cont_bank in user2['data']['accounts']:
    if user2['data']['accounts'][cont_bank]:
        contas_samara.append(user2['data']['accounts'][cont_bank][0][0])
        pix_samara.append(user2['data']['accounts'][cont_bank][0][2])

contas_silvio = []
pix_silvio = []
for cont_bank in user3['data']['accounts']:
    if user3['data']['accounts'][cont_bank]:
        contas_silvio.append(user3['data']['accounts'][cont_bank][0][0])
        pix_silvio.append(user3['data']['accounts'][cont_bank][0][2])

operation_thiago = [
    {0: {contas_thiago[0]: {"package": [{"type": "DEPOSIT", "value": 2000.0, "sender": contas_thiago[0]}]}},
     1: {contas_thiago[1]: {"package": [{"type": "DEPOSIT", "value": 1000.0, "sender": contas_thiago[1]}]}},
     2: {contas_thiago[2]: {"package": [{"type": "DEPOSIT", "value": 500.0, "sender": contas_thiago[2]}]}},
     },
    {0: {contas_thiago[0]: {"package": [{"type": "WITHDRAW", "value": 50.0, "sender": contas_thiago[0]}]}},
     1: {contas_thiago[1]: {"package": [{"type": "WITHDRAW", "value": 100.0, "sender": contas_thiago[1]}]}},
     2: {contas_thiago[2]: {"package": [{"type": "WITHDRAW", "value": 150.0, "sender": contas_thiago[2]}]}},
     },
    {0: {contas_thiago[0]: {"package": [{"type": "TRANSFER", "value": 500.0, "sender": contas_thiago[0],
                                         "pix": pix_samara[0]}]}},
     1: {contas_thiago[1]: {"package": [{"type": "TRANSFER", "value": 100.0, "sender": contas_thiago[1],
                                         "pix": pix_thiago[0]}]}},
     2: {contas_thiago[2]: {"package": [{"type": "TRANSFER", "value": 150.0, "sender": contas_thiago[2],
                                         "pix": pix_samara[2]}]}},
     3: {contas_thiago[3]: {"package": [{"type": "TRANSFER", "value": 50.0, "sender": contas_thiago[3],
                                         "pix": pix_samara[1]}]}}
     }
]

operation_samara = [
    {0: {contas_samara[0]: {"package": [{"type": "DEPOSIT", "value": 864.0, "sender": contas_samara[0]}]}},
     1: {contas_samara[1]: {"package": [{"type": "DEPOSIT", "value": 700.0, "sender": contas_samara[1]}]}}
     },
    {0: {contas_samara[0]: {"package": [{"type": "TRANSFER", "value": 500.0, "sender": contas_samara[0],
                                         "pix": pix_silvio[1]}]}},
     1: {contas_samara[1]: {"package": [{"type": "TRANSFER", "value": 200.0, "sender": contas_samara[1],
                                         "pix": pix_thiago[0]}]}}
    }
]

operation_silvio = [
    {0: {contas_silvio[0]: {"package": [{"type": "WITHDRAW", "value": 50.0, "sender": contas_silvio[0]}]}},
     1: {contas_silvio[1]: {"package": [{"type": "WITHDRAW", "value": 100.0, "sender": contas_silvio[1]}]}}}
]

urls = [
    (f"{API2}/operations", operation_thiago[0]),
    (f"{API1}/operations", operation_thiago[1]),
    (f"{API3}/operations", operation_thiago[2]),
]

asyncio.run(main(urls))

# Login do usuário 1, 2 e 3
user1 = get_request("login", API2,
                    {"user_name": "thiago001", "password": "12345678"})
user2 = get_request("login", API1,
                    {"user_name": "mara21", "password": "12345678"})
user3 = get_request("login", API3,
                    {"user_name": "juninho123", "password": "12345678"})