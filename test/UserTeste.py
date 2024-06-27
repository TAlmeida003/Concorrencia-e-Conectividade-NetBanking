import requests


def post_request(route, base_url, data):
    url = f"{base_url}/{route}"
    response = requests.post(url, json=data)
    print(response.json(), response.status_code)
    print()


def get_request(route, base_url):
    url = f"{base_url}/{route}"
    response = requests.get(url)
    print(response.json(), response.status_code)
    print()


list_ports = [3050, 3051, 3052, 3053]
IP1 = "127.0.0.1"

# Cadastrar Usuário 1
data = {"name": "Thiago Neri", "num_cadastro": "123.123.123-01", "user_name": "thiago001", "password": "12345678", "type_person": "PF"}
post_request("register-customer", f"http://{IP1}:{list_ports[0]}", data)


# Cadastrar Usuário 2
data = {"name": "Samara ferreira", "num_cadastro": "123.123.123-02", "user_name": "samara001", "password": "12345678", "type_person": "PF"}
post_request("register-customer", f"http://{IP1}:{list_ports[0]}", data)

# Cadastrar Usuário já existente
data = {"name": "Thiago Neri", "num_cadastro": "123.123.123-01", "user_name": "thiago002", "password": "12345678", "type_person": "PF"}
post_request("register-customer", f"http://{IP1}:{list_ports[0]}", data)
#
# # Cadastrar User com cpf errado
data = {"name": "Thiago Neri", "num_cadastro": "123.123.123-013", "user_name": "thiago003", "password": "12345678", "type_person": "PF"}
post_request("register-customer", f"http://{IP1}:{list_ports[0]}", data)

# Cadastrar pessoa jurídica
data = {"name": "Thiago Neri", "num_cadastro": "12.123.123/0001-01", "user_name": "thiago002", "password": "12345678", "type_person": "PJ"}
post_request("register-customer", f"http://{IP1}:{list_ports[0]}", data)

# ver lista de usuários
get_request("get_users", f"http://{IP1}:{list_ports[0]}")
