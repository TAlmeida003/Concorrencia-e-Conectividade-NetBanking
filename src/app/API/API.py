import os

from src.app.Node.Node import Node
from src.app.Node.Event import Event
import src.app.utils.utils as utils
from src.app.Exception.BackException import BankException
from src.app.Exception.UserException import UserException
from src.app.Exception.AccountException import AccountException
from src.app.enums import Option_Bank
from flask import Flask, jsonify, request, Response


app = Flask(__name__)

PORT = os.getenv('P', '3050')
node = Node(utils.LIST_NODES.index(PORT), utils.LIST_NODES)

'''
                            ============= ROTAS DA ORDENAÇÃO TOTAL ==============
'''


@app.route('/proposer/<string:value>', methods=['POST'])
def proposer(value):
    value = eval(value)
    node.propose_value(value, "TESTE")
    return Response(status=200)


@app.route('/receiver_message/', methods=['POST'])
def receiver_message():
    event = request.json
    event = Event(
        event['sender'],
        event['timestamp'],
        event['type_msg'],
        event['id'],
        event['msg'],
        event['number_of_acks']
    )
    node.receiver_message(event)
    return Response(status=200)


@app.route('/receiver_ack/<string:event_id>', methods=['POST'])
def receiver_ack(event_id):
    node.receiver_ack(event_id)
    return Response(status=200)


@app.route('/init_check_queue/<string:event_id>', methods=['POST'])
def init_check_queue(event_id):
    dict_mgs = request.json
    node.send_one_queue(event_id, dict_mgs)
    return Response(status=200)


@app.route('/receiver_one_queue/<string:event_id>', methods=['POST'])
def receiver_one_queue(event_id):
    mgs = request.json
    node.receiver_one_queue(event_id, mgs)
    return Response(status=200)


@app.route('/check', methods=['GET'])
def check():
    return Response(status=200)


@app.route('/node_fail/<string:node_id>', methods=['GET'])
def node_fail(node_id):
    node.dict_peers_online[node_id] = False
    return Response(status=200)


@app.route('/get_queue', methods=['GET'])
def get_queue():
    return jsonify([event.__dict__ for event in node.FIFO_evento])


@app.route('/get_ack', methods=['GET'])
def get_ack():
    return jsonify(node.dict_ack)


'''
                                    ============= ROTAS  DO BANCO ==============                                 
'''


@app.route('/register-customer', methods=['POST'])
def register_customer() -> tuple[Response, int]:
    dict_customer: dict = request.json
    try:
        utils.is_data_register_user_valid(
            dict_customer['name'],
            dict_customer['user_name'],
            dict_customer['num_cadastro'],
            dict_customer['password'],
            dict_customer['type_person']
        )
        event: Event = node.propose_value(dict_customer, Option_Bank.REGISTER.value)

        while not event.exe:
            pass

        if event.can_be_executed:
            return jsonify({'descript': f'Cliente {dict_customer['user_name']} criado com sucesso'}), 200
        else:
            return jsonify({'descript': event.mgs_executed}), 400

    except (BankException, UserException) as e:
        return jsonify({'descript': e.__str__()}), 400


@app.route('/login', methods=['GET'])
def login() -> tuple[Response, int]:
    dict_login: dict = request.json
    try:
        dict_data_user: dict[str, str | dict] = node.bank.login(
            dict_login['user_name'],
            dict_login['password']
        )
        return jsonify({"descript": "Logado com sucesso", "data": dict_data_user}), 200
    except (BankException, UserException) as e:
        return jsonify({'descript': e.__str__()}), 400


@app.route('/create_account', methods=['POST'])
def create_account() -> tuple[Response, int]:
    dict_account: dict = request.json

    try:
        node.bank.create_conta(
            dict_account['user_name'],
            dict_account['type_account'],
            dict_account['password'],
            dict_account['pix_type'],
            dict_account['users'],
            dict_account['value_init']
        )
        return jsonify({'descript': 'Conta criada com sucesso'}), 200
    except (BankException, AccountException) as e:
        return jsonify({'descript': e.__str__()}), 400


@app.route('/accounts_user/<string:user_name>', methods=['GET'])
def get_count(user_name: str) -> tuple[dict[int, list[list[int | float]]], int]:
    list_accounts_value: list[list[int | float]] = []
    for account in node.bank.dict_user[user_name].accounts:
        list_accounts_value.append([account, node.bank.dict_account[account].balance, node.bank.dict_account[account].kay_pix])
    return {str(utils.LIST_NODES.index(PORT)): list_accounts_value}, 200


@app.route('/get_users', methods=['GET'])
def get_users() -> tuple[Response, int]:
    return jsonify([user.__dict__ for user in node.bank.dict_user.values()]), 200


@app.route('/operations', methods=['POST'])
def operations() -> tuple[Response, int]:
    operations_package: dict = request.json
    event: Event = node.propose_value(operations_package, Option_Bank.PACKAGE.value)

    while not event.exe:
        pass

    if event.can_be_executed:
        return jsonify({"descript": "Operações realizada com sucesso"}), 200
    else:
        return jsonify({'descript': event.mgs_executed}), 400


@app.route('/receiver_pix', methods=['POST'])
def receiver_pix() -> Response:
    dict_data: dict = request.json
    node.bank.receiver_pix(dict_data)
    return Response(status=200)


@app.route('/receiver_pix_all/<string:pix>', methods=['POST'])
def receiver_pix_all(pix: str) -> Response:
    node.bank.list_pix_all.append(pix)
    return Response(status=200)


@app.route('/get_pix_all', methods=['GET'])
def get_pix_all() -> tuple[Response, int]:
    return jsonify(node.bank.list_pix_all), 200


@app.route('/get_account/<string:account>', methods=['GET'])
def get_account(account: str):
    try:
        return jsonify(node.bank.dict_account[int(account)].__dict__), 200
    except KeyError:
        return jsonify({'descript': 'Conta não encontrada'}), 400
