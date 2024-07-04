import requests

list_host: list[str] = ['172.16.103.1', '172.16.103.2', '172.16.103.3', '172.16.103.4', '172.16.103.5', '172.16.103.6',
                        '172.16.103.7', '172.16.103.8', '172.16.103.9', '172.16.103.10', '172.16.103.11',
                        '172.16.103.12', '172.16.103.13', '172.16.103.14']
PORT = 3050


def post_request(route, base_url, data):
    url = f"{base_url}/{route}"
    response = requests.post(url, json=data)
    return response.json(), response.status_code


def get_test_1(route, base_url):
    url = f"{base_url}/{route}"
    response = requests.get(url, timeout=5)
    return response.status_code


def get_request(route, base_url, data):
    url = f"{base_url}/{route}"
    response = requests.get(url, json=data)
    return response.json(), response.status_code


def post_register_user(data, node=0):
    try:
        return post_request("register-customer", f"http://{list_host[node]}:{PORT}", data)
    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout) as e:
        return {"descript": "Erro ao tentar conectar com o banco."}, 500


def get_test(node):
    try:
        return get_test_1("check", f"http://{list_host[node]}:{PORT}")
    except (
    requests.exceptions.RequestException, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
        return 500


def post_login_user(dict_data, node):
    try:
        return get_request("login", f"http://{list_host[node]}:{PORT}", dict_data)
    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout) as e:
        return {"descript": "Erro ao tentar conectar com o banco."}, 500


def post_create_account(data, node):
    try:
        return post_request("create_account", f"http://{list_host[node]}:{PORT}", data)
    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout) as e:
        return {"descript": "Erro ao tentar conectar com o banco."}, 500


def get_account(data, node):
    try:
        return get_request(f"get_account/{data}", f"http://{list_host[node]}:{PORT}", data)
    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout) as e:
        return {"descript": "Erro ao tentar conectar com o banco."}, 500


def post_operations(data, node):
    try:
        return post_request("operations", f"http://{list_host[node]}:{PORT}", data)
    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout) as e:
        return {"descript": "Erro ao tentar conectar com o banco."}, 500
