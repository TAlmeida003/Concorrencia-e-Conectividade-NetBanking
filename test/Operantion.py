import json
import asyncio
import aiohttp
import requests

list_ports = [3050, 3051, 3052, 3053]
IP1 = "192.168.0.100"


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
    resultados = await asyncio.gather(*tasks)
    # for resultado in resultados:
    #     print(resultado)

# ======================================================================================================================

# Login do usuário 1 e 2

user1 = get_request("login", f"http://{IP1}:{list_ports[0]}",
                    {"user_name": "thiago001", "password": "12345678"})
user2 = get_request("login", f"http://{IP1}:{list_ports[0]}",
                    {"user_name": "mara21", "password": "12345678"})
user3 = get_request("login", f"http://{IP1}:{list_ports[0]}",
                    {"user_name": "juninho123", "password": "12345678"})

# ======================================================================================================================

user1_cont1 = user1['data']['accounts']['0'][0][0]
user1_cont2 = user1['data']['accounts']['1'][0][0]
user1_cont3 = user1['data']['accounts']['2'][0][0]

user2_cont1 = user2['data']['accounts']['0'][0][0]
user2_cont2 = user2['data']['accounts']['1'][0][0]
user2_cont3 = user2['data']['accounts']['2'][0][0]

user3_cont1 = user3['data']['accounts']['0'][0][0]
user3_cont2 = user3['data']['accounts']['1'][0][0]

# PIX
user1_pix1 = user1['data']['accounts']['0'][0][2]
user1_pix2 = user1['data']['accounts']['1'][0][2]
user1_pix3 = user1['data']['accounts']['2'][0][2]

user2_pix1 = user2['data']['accounts']['0'][0][2]
user2_pix2 = user2['data']['accounts']['1'][0][2]
user2_pix3 = user2['data']['accounts']['2'][0][2]

user3_pix1 = user3['data']['accounts']['0'][0][2]
user3_pix2 = user3['data']['accounts']['1'][0][2]


urls = [
    (f"http://{IP1}:{list_ports[0]}/operations",
     {
         0: {user1_cont1: {"package": [
                 {"type": "TRANSFER", "value": 500.0, "sender": user1_cont1, "pix": user2_pix1},
                 {"type": "TRANSFER", "value": 100.0, "sender": user1_cont1, "pix": user1_pix2},
                 {"type": "TRANSFER", "value": 450.0, "sender": user1_cont1, "pix": user3_pix1}]}},
     }),
    (f"http://{IP1}:{list_ports[2]}/operations",
     {
        0: {user2_cont1: {"package": [
            {"type": "DEPOSIT", "value": 2000.0, "sender": user2_cont1},
            {"type": "TRANSFER", "value": 1000.0, "sender": user2_cont1, "pix": user1_pix1},
            {"type": "TRANSFER", "value": 1000.0, "sender": user2_cont1, "pix": user3_pix1}]}}}
    ),
    (f"http://{IP1}:{list_ports[1]}/operations",
     {
        0: {user3_cont1: {"package": [
            {"type": "TRANSFER", "value": 10.0, "sender": user3_cont1, "pix": user1_pix1},
            {"type": "WITHDRAW", "value": 50.0, "sender": user3_cont1}]}}}
    ),
    (f"http://{IP1}:{list_ports[0]}/operations",
     {
         0: {user1_cont1: {"package": [
             {"type": "TRANSFER", "value": 500.0, "sender": user1_cont1, "pix": user2_pix1},
             {"type": "TRANSFER", "value": 100.0, "sender": user1_cont1, "pix": user1_pix2},
             {"type": "TRANSFER", "value": 450.0, "sender": user1_cont1, "pix": user3_pix1}]}},
     }),
    (f"http://{IP1}:{list_ports[2]}/operations",
     {
         0: {user2_cont1: {"package": [
             {"type": "DEPOSIT", "value": 2000.0, "sender": user2_cont1},
             {"type": "TRANSFER", "value": 1000.0, "sender": user2_cont1, "pix": user1_pix1},
             {"type": "TRANSFER", "value": 1000.0, "sender": user2_cont1, "pix": user3_pix1}]}}}
     ),
    (f"http://{IP1}:{list_ports[1]}/operations",
     {
         0: {user3_cont1: {"package": [
             {"type": "TRANSFER", "value": 10.0, "sender": user3_cont1, "pix": user1_pix1},
             {"type": "WITHDRAW", "value": 50.0, "sender": user3_cont1}]}}}
     ),
    (f"http://{IP1}:{list_ports[0]}/operations",
     {
         0: {user1_cont1: {"package": [
             {"type": "TRANSFER", "value": 500.0, "sender": user1_cont1, "pix": user2_pix1},
             {"type": "TRANSFER", "value": 100.0, "sender": user1_cont1, "pix": user1_pix2},
             {"type": "TRANSFER", "value": 450.0, "sender": user1_cont1, "pix": user3_pix1}]}},
     }),
    (f"http://{IP1}:{list_ports[2]}/operations",
     {
         0: {user2_cont1: {"package": [
             {"type": "DEPOSIT", "value": 2000.0, "sender": user2_cont1},
             {"type": "TRANSFER", "value": 1000.0, "sender": user2_cont1, "pix": user1_pix1},
             {"type": "TRANSFER", "value": 1000.0, "sender": user2_cont1, "pix": user3_pix1},
         {"type": "WITHDRAW", "value": 50.0, "sender": user3_cont1}]}}}
     ),
    (f"http://{IP1}:{list_ports[1]}/operations",
     {
         0: {user3_cont1: {"package": [
             {"type": "TRANSFER", "value": 10.0, "sender": user3_cont1, "pix": user1_pix1},
             {"type": "WITHDRAW", "value": 50.0, "sender": user3_cont1}]}}}
     )
]

asyncio.run(main(urls))

#====================================================================================================
# Login do usuário 1 e 2

user1 = get_request("login", f"http://{IP1}:{list_ports[0]}",
                    {"user_name": "thiago001", "password": "12345678"})
user2 = get_request("login", f"http://{IP1}:{list_ports[0]}",
                    {"user_name": "mara21", "password": "12345678"})
user3 = get_request("login", f"http://{IP1}:{list_ports[0]}",
                    {"user_name": "juninho123", "password": "12345678"})

