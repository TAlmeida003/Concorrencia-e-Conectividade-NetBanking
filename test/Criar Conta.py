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


# ======================================================================================================================
# Criar conta para o usuário 1 no banco 0 e 1
data1 = {'user_name': 'thiago001', 'password': '12345678', 'type_account': 'PF', 'pix_type': 'CPF', 'users': [],
        'value_init': 50.0}

data2 = {'user_name': 'thiago001', 'password': '12345678', 'type_account': 'PF', 'pix_type': 'USER_NAME', 'users': [],
        'value_init': 50.0}

post_request("create_account", f"http://{IP1}:{list_ports[0]}", data1)
post_request("create_account", f"http://{IP1}:{list_ports[1]}", data2)
post_request("create_account", f"http://{IP1}:{list_ports[2]}", data2)


# Criar conta para o usuário 2 no banco 0, 1 e 2
data1 = {'user_name': 'mara21', 'password': '12345678', 'type_account': 'PF', 'pix_type': 'USER_NAME', 'users': [],
        'value_init': 50.0}

data2 = {'user_name': 'mara21', 'password': '12345678', 'type_account': 'PF', 'pix_type': 'NUM_CONTA', 'users': [],
        'value_init': 50.0}

data3 = {'user_name': 'mara21', 'password': '12345678', 'type_account': 'CONJUNTA', 'pix_type': 'RANDOM',
        'users': ["thiago001", "juninho123"], 'value_init': 50.0}

post_request("create_account", f"http://{IP1}:{list_ports[0]}", data1)

post_request("create_account", f"http://{IP1}:{list_ports[1]}", data2)

post_request("create_account", f"http://{IP1}:{list_ports[2]}", data3)

# Criar conta para o usuário 3 no banco 0 e 1

data1 = {'user_name': 'juninho123', 'password': '12345678', 'type_account': 'PF', 'pix_type': 'USER_NAME', 'users': [],
        'value_init': 50.0}

data2 = {'user_name': 'juninho123', 'password': '12345678', 'type_account': 'PF', 'pix_type': 'NUM_CONTA', 'users': [],
        'value_init': 50.0}

post_request("create_account", f"http://{IP1}:{list_ports[0]}", data1)

post_request("create_account", f"http://{IP1}:{list_ports[1]}", data2)