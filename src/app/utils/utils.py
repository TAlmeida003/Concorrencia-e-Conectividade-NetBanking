import random
import re
import time

from src.app.Exception.UserException import UserException
from src.app.Node import Event

LIST_NODES: list[str] = ['3050', '3051', '3052']


def delay_time(time_init: float) -> None:
    final_time: float = time.time()
    if final_time - time_init < 5:
        time.sleep(5 - (final_time - time_init))


def init_dict_peers_online(dict_peers_online: dict[str:bool]) -> None:
    for node in LIST_NODES:
        dict_peers_online[node] = True


def fail_dict_peers_online(dict_peers_online: dict[str:bool]) -> None:
    for node in LIST_NODES:
        dict_peers_online[node] = False


def get_id_event(id_node: int, FIFO_event: list[Event]) -> str:
    id_test: str = "EV" + str(random.randint(0, 1000)) + "-" + LIST_NODES[id_node]
    while is_id_in_queue(id_test, FIFO_event):
        id_test: str = "EV" + str(random.randint(0, 1000)) + "-" + LIST_NODES[id_node]
    return id_test


def is_id_in_queue(id_test: str, FIFO_event: list[Event]) -> bool:
    for event in FIFO_event:
        if event.id == id_test:
            return True
    return False


def get_index_event(event_id: str, FIFO_event: list[Event]) -> int:
    for i in range(len(FIFO_event)):
        if FIFO_event[i].id == event_id:
            return i
    return -1


def len_nodes_online(dict_peers_online: dict[str:bool]) -> int:
    count: int = 0
    for node in LIST_NODES:
        if dict_peers_online[node]:
            count += 1
    return count


def report_fail_node(id_node: int, dict_peers_online: dict[str:bool]) -> None:
    for node in LIST_NODES:
        if node != LIST_NODES[id_node]:
            dict_peers_online[node] = False


def is_data_register_user_valid(user_name: str, name: str, num_cadastro: str, user_password: str, type_person: str):
    cpf_standard = re.compile(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$')
    cnpj_standard = re.compile(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$')

    if not bool(cpf_standard.match(num_cadastro)) and type_person == 'PF':
        raise UserException('CPF inválido')
    elif not bool(cnpj_standard.match(num_cadastro)) and type_person == 'PJ':
        raise UserException('CNPJ inválido')
    elif type_person != 'PF' and type_person != 'PJ':
        raise UserException('Tipo de pessoa inválido')
    elif len(user_password) < 8:
        raise UserException('Senha deve ter no mínimo 8 caracteres')
    elif len(name) < 3:
        raise UserException('Nome inválido')
    elif len(user_name) < 3:
        raise UserException('Nome de usuário inválido')
