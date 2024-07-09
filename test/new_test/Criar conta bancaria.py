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


API1 = "http://172.16.103.1:3050"
API2 = "http://172.16.103.2:3050"
API3 = "http://172.16.103.3:3050"
API4 = "http://172.16.103.4:3050"

contas_thiago = [
    {'user_name': 'thiago001', 'password': '12345678', 'type_account': 'PF', 'pix_type': 'CPF', 'users': [],
     'value_init': 50.0},
    {'user_name': 'thiago001', 'password': '12345678', 'type_account': 'PF', 'pix_type': 'USER_NAME', 'users': [],
     'value_init': 50.0},
    {'user_name': 'thiago001', 'password': '12345678', 'type_account': 'PF', 'pix_type': 'RANDOM', 'users': [],
     'value_init': 50.0}
]

contas_mara = [
    {'user_name': 'mara21', 'password': '12345678', 'type_account': 'PF', 'pix_type': 'USER_NAME', 'users': [],
     'value_init': 50.0},
    {'user_name': 'mara21', 'password': '12345678', 'type_account': 'PF', 'pix_type': 'NUM_CONTA', 'users': [],
     'value_init': 50.0},
    {'user_name': 'mara21', 'password': '12345678', 'type_account': 'CONJUNTA', 'pix_type': 'RANDOM',
     'users': ["thiago001", "juninho123"], 'value_init': 150.0},
]

contas_silvio = [
    {'user_name': 'juninho123', 'password': '12345678', 'type_account': 'PF', 'pix_type': 'USER_NAME', 'users': [],
     'value_init': 50.0},
    {'user_name': 'juninho123', 'password': '12345678', 'type_account': 'PF', 'pix_type': 'NUM_CONTA', 'users': [],
     'value_init': 50.0}
]

post_request("create_account", API1, contas_thiago[0])
post_request("create_account", API2, contas_thiago[1])
post_request("create_account", API3, contas_thiago[1])
post_request("create_account", API4, contas_thiago[2])

post_request("create_account", API1, contas_mara[0])
post_request("create_account", API2, contas_mara[1])
post_request("create_account", API3, contas_mara[2])

post_request("create_account", API1, contas_silvio[0])
post_request("create_account", API2, contas_silvio[1])
