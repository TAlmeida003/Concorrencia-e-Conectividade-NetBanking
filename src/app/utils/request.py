import asyncio
import time

import aiohttp
import requests
from src.app.Node import Event
from src.app.utils.utils import LIST_NODES, delay_time

HOST = "192.168.25.109"
TIMEOUT = None
TIMEOUT_TESTE = 5


def post_receiver_message(event: Event, node: int, peers: list[str], dict_peers_online: dict[str:bool]) -> None:
    try:
        requests.post(f'http://{HOST}:{peers[node]}/receiver_message/', json=event.__dict__, timeout=TIMEOUT)
    except requests.exceptions.RequestException as e:
        print("Error1: ", e)
        dict_peers_online[peers[node]] = False


def post_receiver_ack(event_id: str, node: int, peers: list[str], dict_peers_online: dict[str:bool]) -> None:
    try:
        requests.post(f'http://{HOST}:{peers[node]}/receiver_ack/{event_id}', timeout=TIMEOUT)
    except requests.exceptions.RequestException as e:
        print("Error2: ", e)
        dict_peers_online[peers[node]] = False


def post_init_check_queue(event_id: str, node: int, peers: list[str], dict_peers_online: dict[str:bool],
                          dict_mgs: dict[str: str | bool]) -> None:
    try:
        requests.post(f'http://{HOST}:{peers[node]}/init_check_queue/{event_id}', timeout=TIMEOUT, json=dict_mgs)
    except requests.exceptions.RequestException as e:
        print("Error3: ", e)
        dict_peers_online[peers[node]] = False


def post_receiver_one_queue(event_id: str, mgs: dict[str: str | bool], node: int, peers: list[str],
                            dict_peers_online: dict[str:bool]) -> None:
    try:
        requests.post(f'http://{HOST}:{peers[node]}/receiver_one_queue/{event_id}', timeout=TIMEOUT, json=mgs)
    except requests.exceptions.RequestException as e:
        print("Error4: ", e)
        dict_peers_online[peers[node]] = False


def get_accounts_user(user_name: str, node: int, peers: list[str]) -> dict[int, list[list[int | float]]]:
    try:
        response = requests.get(f'http://{HOST}:{peers[node]}/accounts_user/{user_name}', timeout=TIMEOUT)
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error5: ", e)
        return {-1: []}


def post_receiver_pix_all(pix: str, node: int, peers: list[str], dict_peers_online: dict[str:bool]) -> None:
    try:
        requests.post(f'http://{HOST}:{peers[node]}/receiver_pix_all/{pix}', timeout=TIMEOUT)
    except requests.exceptions.RequestException as e:
        print("Error6: ", e)
        dict_peers_online[peers[node]] = False


def post_receiver_pix(dict_data: dict, node: int, peers: list[str], dict_peers_online: dict[str:bool]) -> None:
    try:
        requests.post(f'http://{HOST}:{peers[node]}/receiver_pix', timeout=TIMEOUT, json=dict_data)
    except requests.exceptions.RequestException as e:
        print("Error7: ", e)
        dict_peers_online[peers[node]] = False


async def request_get_check(url, id_node: str, dict_peers_online: dict[str:bool]) -> None:
    timeout_setting = aiohttp.ClientTimeout(total=TIMEOUT_TESTE)

    async with aiohttp.ClientSession(timeout=timeout_setting) as session:
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    if dict_peers_online[id_node]:
                        pass
                    dict_peers_online[id_node] = False
                else:
                    dict_peers_online[id_node] = True
        except (asyncio.TimeoutError, aiohttp.ClientError):
            dict_peers_online[id_node] = False


async def main_check(id_node: int, dict_peers_online: dict[str:bool]) -> None:
    time_init: float = time.time()

    list_urls: list[tuple[str, str]] = get_urls(id_node)
    tasks = [request_get_check(url[0], url[1], dict_peers_online) for url in list_urls]
    await asyncio.gather(*tasks)
    delay_time(time_init)


def get_urls(id_node: int) -> list[tuple[str, str]]:
    list_urls: list[tuple[str, str]] = []
    for node in LIST_NODES:
        if node != LIST_NODES[id_node]:
            list_urls.append((f"http://{HOST}:{node}/check", node))
    return list_urls
