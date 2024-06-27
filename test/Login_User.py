import requests


list_ports = [3050, 3051, 3052, 3053]
IP1 = "127.0.0.1"


def post_request(route, base_url, data):
    url = f"{base_url}/{route}"
    response = requests.post(url, json=data)
    print(response.json(), response.status_code)
    print()


def get_request(route, base_url, data):
    url = f"{base_url}/{route}"
    response = requests.get(url, json=data)
    print(response.json(), response.status_code)
    print()


# Cadastrar Usuário 1
data = {"name": "Thiago Neri", "num_cadastro": "123.123.123-01", "user_name": "thiago001", "password": "12345678", "type_person": "PF"}
post_request("register-customer", f"http://{IP1}:{list_ports[0]}", data)

data = {'user_name': 'thiago001', 'password': '12345678', 'type_account': 'PF', 'pix_type': 'CPF', 'users': []}
post_request("create_account", f"http://{IP1}:{list_ports[0]}", data)

data = {'user_name': 'thiago001', 'password': '12345678', 'type_account': 'PF', 'pix_type': 'CPF', 'users': []}
post_request("create_account", f"http://{IP1}:{list_ports[1]}", data)

get_request("login", f"http://{IP1}:{list_ports[0]}", {"user_name": "thiago001", "password": "12345678"})

get_request("login", f"http://{IP1}:{list_ports[1]}", {"user_name": "thiago001", "password": "12345678"})

get_request("login", f"http://{IP1}:{list_ports[2]}", {"user_name": "thiago001", "password": "12345678"})

get_request("login", f"http://{IP1}:{list_ports[0]}", {"user_name": "thiago001", "password": "1234568"})
