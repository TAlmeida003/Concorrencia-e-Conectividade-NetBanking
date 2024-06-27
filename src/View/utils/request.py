import requests

list_ports = [3050, 3051, 3052, 3053]
HOST = '127.0.0.1'


def post_request(route, base_url, data):
    url = f"{base_url}/{route}"
    response = requests.post(url, json=data)
    return response.json(), response.status_code


def post_register_user(data, node=0):
    return post_request("register-customer", f"http://{HOST}:{list_ports[node]}", data)
