import requests

from src.view.utils import request
from src.view.utils import prints

LIST_OPTIONS: list[str] = ["Registrar Usuário", "Login do Usuário", "Encerrar Programa"]


def main_menu(bank) -> None:
    prints.header("NetBanking - Bancos Distribuídos")
    prints.topic("MENU PRINCIPAL")
    prints.get_baseboard()
    prints.jump_line(3)

    if bank != -1:
        string = f"O usuário está conectado ao banco {bank}"
    else:
        string = "O usuário não está conectado a nenhum banco"
    print(f"|{string: ^86}|".center(168))

    prints.jump_line(5)

    menu_options = [
        "Registrar Usuário",
        "Login do Usuário",
        "Selecionar Banco",
        "Encerrar Programa"
    ]
    prints.get_display_option_two(menu_options)
    prints.get_baseboard()


def register_menu() -> None:
    prints.header("NetBanking - Bancos Distribuídos")
    prints.topic("REGISTRAR USUÁRIO")
    prints.get_baseboard()
    prints.jump_line(3)

    instructions = [
        "Preencha os campos abaixo com as seguintes informações:",
        'O campo "Nome" deve conter apenas letras e espaços.',
        'O campo "Número de Identificação" deve conter o CPF ou CNPJ.',
        'O campo "Senha" deve conter letras, números e caracteres especiais.',
        'O campo "Nome de Usuário" deve conter letras, números e caracteres especiais.',
        'O campo "Tipo de Pessoa" deve ser "PF" (Pessoa Física) ou "PJ" (Pessoa Jurídica).'
    ]

    for instruction in instructions:
        print(f"|{instruction: ^86}|".center(168))
        prints.jump_line(2)

    prints.jump_line(2)
    prints.get_baseboard()


def select_banks() -> None:
    prints.header("NetBanking - Bancos Distribuídos")
    prints.topic("SELECIONAR BANCOS")
    prints.get_baseboard()
    prints.jump_line(3)

    banks = []

    for i in range(0, len(request.list_host), 2):
        if 10 <= i:
            string = f"[ {i: ^1} ] - Banco {i} HOST:{request.list_host[i]:^15}     [ {i + 1:^1} ] - Banco {i + 1} HOST: {request.list_host[i + 1]:^15}"
        else:
            string = f"[ {i: ^3} ] - Banco {i} HOST:{request.list_host[i]:^15}     [ {i + 1:^3} ] - Banco {i + 1} HOST:{request.list_host[i + 1]:^15}"
        print(f"|{string: ^86}|".center(168))
        prints.jump_line(2)
    prints.jump_line(2)
    prints.get_baseboard()


def screen_user(bank, dict_data) -> None:
    type_person = "Física" if dict_data['type_person'] == "PF" else "Jurídica"
    num = num_account(dict_data)
    name = f"Nome: {dict_data['name']: ^35}"
    bank = f"Banco {bank: ^2}"
    prints.get_baseboard()
    print(f"|{'NetBanking - Bancos Distribuídos': ^86}|".center(168))
    prints.get_baseboard()
    print(f"| {name + '            Acessando o banco: ' + bank: ^80} |".center(168))
    print(
        f"| Número de Identificação: {dict_data['num_cadastro']}                Tipo de Pessoa: {type_person: ^10}|".center(
            168))
    print(f"| Nome de Usuário: {dict_data['user_name']: ^15}                     Número de contas: {num: ^10}|".center(
        168))
    prints.get_baseboard()

    prints.topic("CONTAS e OPERAÇÕES BANCÁRIAS")

    prints.get_baseboard()
    prints.jump_line(1)
    print(f"|{('_' * 70): ^86}|".center(168))
    prints.jump_line(1)
    for node in dict_data["accounts"]:
        for account in dict_data["accounts"][node]:
            string = f"{'Banco: ' + str(node): ^10}              {'Conta: ' + str(account[0]): ^10}              {'Saldo: R$ ' + str(account[1]): ^10}"
            print(f"|{string: ^86}|".center(168))
            print(f"|{'    Chave pix: ' + account[2].split(':')[1]: ^83}   |".center(168))
            prints.jump_line(1)
            print(f"|{('_' * 70): ^86}|".center(168))
            prints.jump_line(1)
    print(f"|{'    [ 1 ] — Realizar Operações Bancarias      ' + '[ 2 ] — Recarregar Página    ': ^86}|".center(168))
    prints.jump_line(1)
    print(f"|{'    [ 3 ] — Desconectar Usuário    ' + '[ 4 ] — Criar conta    ': ^86}|".center(168))
    prints.jump_line(1)
    print(f"|{'    [ 5 ] — Consultar conta    ': ^86}|".center(168))
    prints.jump_line(1)
    prints.get_baseboard()


def num_account(dict_data) -> int:
    num = 0
    for node in dict_data["accounts"]:
        for _ in dict_data["accounts"][node]:
            num += 1
    return num


def operations_menu(dict_data) -> None:
    prints.header("NetBanking - Bancos Distribuídos")
    prints.topic("OPERAÇÕES BANCÁRIAS")
    prints.get_baseboard()
    prints.jump_line(3)

    print(f"|{'Suas Contas:': ^86}|".center(168))
    prints.jump_line(2)

    num = 0
    string = ""
    for node in dict_data:
        for account in dict_data[node]:
            string += f"     {'Banco: ' + str(node): ^10}     {'Conta: ' + str(account[0]): ^10}     "
            if num == 1:
                print(f"|{string: ^86}|".center(168))
                string = ""
                prints.jump_line(2)
                num = 0
            else:
                num += 1
    if num != 0:
        print(f"|{string: ^86}|".center(168))
        prints.jump_line(2)

    operations = [
        "Transferência",
        "Depósito",
        "Saque",
        "Finalizar Operações",
        "Voltar"
    ]

    prints.get_display_option_two(operations)
    prints.jump_line(0)
    prints.get_baseboard()


def pacote_final(dict_data):
    prints.header("NetBanking - Bancos Distribuídos")
    prints.topic("PACOTE FINAL")
    prints.get_baseboard()
    prints.jump_line(3)
    for node in dict_data:
        for account in dict_data[node]:
            for package in dict_data[node][account]['package']:
                string = f"{'banco: ' + str(node): ^2}              {'Conta de Operação: ' + str(account): ^10}              {'Tipo: ' + package['type']: ^10}"
                print(f"|{string: ^86}|".center(168))
                if package['type'] == "TRANSFER":
                    string = f"{'Valor: R$ ' + str(package['value']): ^10}              {'    Chave pix: ' + package['pix']: ^10}"
                else:
                    string = f"{'Valor: R$ ' + str(package['value']): ^10}"
                print(f"|{string: ^86}|".center(168))
                prints.jump_line(2)
    prints.jump_line(2)
    prints.get_baseboard()
    print("Tecle ENTER para voltar ao menu principal.".center(170))


def view_account(dict_data):
    prints.header("NetBanking - Bancos Distribuídos")
    prints.get_baseboard()
    string = f"N° da conta: {dict_data['num_account']: ^10}" + "   " + f"Tipo de conta: {dict_data['type_account']: ^10}"
    print(f"|{string: ^86}|".center(168))
    string = ""
    for user in dict_data['user_names']:
        string += f"{user: ^20}"
    print(f"|{'Usuários: ' + string: ^86}|".center(168))
    string = f"Saldo Atual: {'R$ ' + dict_data['balance'].__str__() : ^10}" + "   " + f"Chave PIX: {dict_data['kay_pix'].split(":")[1]: ^20}" +"   " + f"Número de transações: {len(dict_data['transactions'])}"
    print(f"|{string: ^86}|".center(168))
    prints.get_baseboard()
    prints.topic("HISTÓRICO DE TRANSAÇÕES")
    prints.get_baseboard()
    prints.jump_line(1)
    for transaction in dict_data['transactions']:
        string1 = (
                f"Saldo Atual: {'R$ ' + transaction['app_balance'].__str__(): ^15}" + "   " + f"Valor: {'R$ ' + transaction['value'].__str__(): ^15}"
                + "   " + f"Operação: {transaction['type']: ^16}")
        print(f"|{string1: ^86}|".center(168))
        strign2 = (
                f"Enviado por: {transaction['made_by']: ^10}" + "       " + f"Enviado pelo Banco: {transaction['bank_sender']: ^2}" + "       " + f"Data: {transaction['date']: ^11}")
        print(f"|{strign2: ^86}|".center(168))
        prints.jump_line(1)
    prints.get_baseboard()
    print("Tecle ENTER para voltar ao menu principal.".center(170))


def create_account():
    prints.header("NetBanking - Bancos Distribuídos")
    prints.topic("CRIAR CONTA")
    prints.get_baseboard()
    prints.jump_line(3)

    instructions = [
        "Preencha os campos abaixo com as seguintes informações:",
        "O campo 'Banco' deve ser '1', '2', '3' ou '4'.",
        "O campo 'Tipo de Conta' deve ser 'PF', 'PJ ou 'CONJUNTA'.",
        "O campo 'Tipo de PIX' deve ser 'CPF/CNPJ', 'USER_NAME' ou 'NUM_CONTA' ou 'RANDOM'.",
        "O campo 'Usuários' deve listar os nomes dos usuários, separados por '-'.",
        "O campo 'Valor Inicial' deve conter o valor inicial da conta."
    ]

    for instruction in instructions:
        print(f"|{instruction: ^86}|".center(168))
        prints.jump_line(2)

    prints.jump_line(2)
    prints.get_baseboard()
