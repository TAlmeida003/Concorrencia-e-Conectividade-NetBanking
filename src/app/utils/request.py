import requests
from src.app.Node import Event

#PORT = "3050"
HOST = "192.168.0.100"
TIMEOUT = None
TIMEOUT_TESTE = 5


def post_receiver_message(event: Event, node: int, peers: list[str], dict_peers_online: dict[str:bool]) -> None:
    try:
        #requests.post(f'http://{peers[node]}:{PORT}/receiver_message/', json=event.__dict__, timeout=TIMEOUT)
        requests.post(f'http://{HOST}:{peers[node]}/receiver_message/', json=event.__dict__, timeout=TIMEOUT)

    except (
    requests.exceptions.RequestException, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, ConnectionResetError) as e:
        print("Error1: ", e)
        dict_peers_online[peers[node]] = False


def post_receiver_ack(event_id: str, node: int, peers: list[str], dict_peers_online: dict[str:bool]) -> None:
    try:
        #requests.post(f'http://{peers[node]}:{PORT}/receiver_ack/{event_id}', timeout=TIMEOUT)
        requests.post(f'http://{HOST}:{peers[node]}/receiver_ack/{event_id}', timeout=TIMEOUT)
    except (
    requests.exceptions.RequestException, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, ConnectionResetError) as e:
        print("Error2: ", e)
        dict_peers_online[peers[node]] = False


def post_init_check_queue(event_id: str, node: int, peers: list[str], dict_peers_online: dict[str:bool],
                          dict_mgs: dict[str: str | bool]) -> None:
    try:
        #requests.post(f'http://{peers[node]}:{PORT}/init_check_queue/{event_id}', timeout=TIMEOUT, json=dict_mgs)
        requests.post(f'http://{HOST}:{peers[node]}/init_check_queue/{event_id}', timeout=TIMEOUT, json=dict_mgs)

    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout, ConnectionResetError) as e:
        print("Error3: ", e)
        dict_peers_online[peers[node]] = False


def post_receiver_one_queue(event_id: str, mgs: dict[str: str | bool], node: int, peers: list[str],
                            dict_peers_online: dict[str:bool]) -> None:
    try:
        #requests.post(f'http://{peers[node]}:{PORT}/receiver_one_queue/{event_id}', timeout=TIMEOUT, json=mgs)
        requests.post(f'http://{HOST}:{peers[node]}/receiver_one_queue/{event_id}', timeout=TIMEOUT, json=mgs)
    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout, ConnectionResetError) as e:
        print("Error4: ", e)
        dict_peers_online[peers[node]] = False


def get_accounts_user(user_name: str, node: int, peers: list[str]) -> dict[str, list[list[int | float]]]:
    try:
        response = requests.get(f'http://{HOST}:{peers[node]}/accounts_user/{user_name}', timeout=TIMEOUT)

        #response = requests.get(f'http://{peers[node]}:{PORT}/accounts_user/{user_name}', timeout=TIMEOUT)
        return response.json()
    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout, ConnectionResetError) as e:
        print("Error5: ", e)
        return {"-1": []}


def post_receiver_pix_all(pix: str, node: int, peers: list[str], dict_peers_online: dict[str:bool]) -> None:
    try:
        requests.post(f'http://{HOST}:{peers[node]}/receiver_pix_all/{pix}', timeout=TIMEOUT)
        #requests.post(f'http://{peers[node]}:{PORT}/receiver_pix_all/{pix}', timeout=TIMEOUT)
    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout, ConnectionResetError) as e:
        print("Error6: ", e)
        dict_peers_online[peers[node]] = False


def post_receiver_pix(dict_data: dict, node: int, peers: list[str], dict_peers_online: dict[str:bool]) -> None:
    try:
        requests.post(f'http://{HOST}:{peers[node]}/receiver_pix', timeout=TIMEOUT, json=dict_data)
        #requests.post(f'http://{peers[node]}:{PORT}/receiver_pix', timeout=TIMEOUT, json=dict_data)
    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout, ConnectionResetError) as e:
        print("Error7: ", e)
        dict_peers_online[peers[node]] = False
