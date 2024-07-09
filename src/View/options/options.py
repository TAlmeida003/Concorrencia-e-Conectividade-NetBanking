import src.view.utils.utils as utils
import src.view.utils.prints as prints
import src.view.utils.request as request
import src.view.screen.screen as screen


def register(bank: int) -> None:
    dict_user: dict = {}
    screen.register_menu()
    dict_user["name"]: str = input((" " * 45) + "* Informe o NOME COMPLETO do usuário: ")
    dict_user["type_person"]: str = input((" " * 45) + "* Informe o TIPO DE PESSOA do usuário: ")
    num_id: str = input((" " * 45) + "* Informe o NÚMERO DE IDENTIFICAÇÃO do usuário: ")

    try:
        if dict_user["type_person"] == "PF":
            dict_user["num_cadastro"] = utils.formatar_cpf(num_id)
        elif dict_user["type_person"] == "PJ":
            dict_user["num_cadastro"] = utils.formatar_cnpj(num_id)
        else:
            raise RuntimeError("O tipo de pessoa deve ser 'PF' ou 'PJ'.")

    except RuntimeError as error:
        prints.get_clear_prompt()
        prints.get_report_error(str(error))
        return

    prints.get_clear_prompt()
    screen.register_menu()
    dict_user["user_name"]: str = input((" " * 45) + "* Informe o NOME DE USUÁRIO do usuário: ")
    dict_user["password"]: str = input((" " * 45) + "* Informe a SENHA do usuário: ")

    prints.get_clear_prompt()
    dict_response, status = request.post_register_user(dict_user, int(bank))
    if status == 200:
        prints.get_report_action(dict_response["descript"])
    elif status == 400:
        prints.get_report_error(dict_response["descript"])
    else:
        prints.get_report_error("Erro ao tentar registrar o usuário.")


def banks() -> int:
    screen.select_banks()
    bank: str = input((" " * 45) + "* Informe o BANCO desejado: ")
    prints.get_clear_prompt()

    if bank not in [str(num) for num in range(len(request.list_host))]:
        prints.get_report_error("Banco não está disponível.")
        return -1

    status = request.get_test(int(bank))
    if status != 200:
        prints.get_report_error("Erro ao tentar conectar com o banco.")
        return -1

    prints.get_report_action("Banco selecionado com sucesso.")
    return int(bank)


def login(bank: int) -> None:
    user_name: str = input((" " * 45) + "* Informe o NOME DE USUÁRIO: ")
    password: str = input((" " * 45) + "* Informe a SENHA: ")
    dict_data = {"user_name": user_name, "password": password}

    prints.get_clear_prompt()
    dict_response, status = request.post_login_user(dict_data, bank)
    if status == 200:
        prints.get_report_action(dict_response["descript"])
    elif status == 400:
        prints.get_report_error(dict_response["descript"])
        return
    else:
        prints.get_report_error("Erro ao tentar logar o usuário.")
        return

    screen.screen_user(bank, dict_response["data"])
    option: str = input((" " * 45) + "* Informe a opção desejada: ")

    while option != "3":
        if option == "1":
            prints.get_clear_prompt()
            operations(bank, dict_response["data"]["accounts"])
        elif option == "2":
            dict_resp, status = request.post_login_user(dict_data, bank)
            if status != 200 and status != 400:
                prints.get_report_error("Erro ao tentar recarregar o usuário.")
                return
            dict_response = dict_resp
            prints.get_clear_prompt()
        elif option == "4":
            prints.get_clear_prompt()
            create_account(user_name, password)
        elif option == "5":
            try:
                node = int(input((" " * 45) + "* Informe o BANCO DESEJADO: "))
                if node in [num for num in range(len(request.list_host))]:
                    num_account = input((" " * 45) + "* Informe o NÚMERO DA CONTA: ")
                    dict_response2, status = request.get_account(num_account, node)
                    if status != 200 and status != 400:
                        prints.get_report_error("Erro ao tentar acessar a conta.")
                        return

                    prints.get_clear_prompt()
                    screen.view_account(dict_response2)
                    input()
                    prints.get_clear_prompt()
                else:
                    prints.get_clear_prompt()
                    prints.get_report_error("Banco não está disponível.")

            except ValueError:
                prints.get_clear_prompt()
                prints.get_report_error("O banco deve ser um número.")

        else:
            prints.get_clear_prompt()
            prints.get_report_error("Opção inválida! Tente novamente.")

        screen.screen_user(bank, dict_response["data"])
        option: str = input((" " * 45) + "* Informe a opção desejada: ")


def create_account(user_name: str, password: str) -> None:
    dict_data = {"user_name": user_name, "password": password}
    screen.create_account()

    bank = input((" " * 45) + "* Informe o BANCO desejado: ")
    if bank not in [str(num) for num in range(len(request.list_host))]:
        prints.get_report_error("Banco não está disponível.")
        return
    dict_data['type_account'] = input((" " * 45) + "* Informe o TIPO DE CONTA: ")
    dict_data['pix_type'] = input((" " * 45) + "* Informe o TIPO DE PIX: ")
    users = input((" " * 45) + "* Informe os USUÁRIOS: ").split("-")
    try:
        dict_data['value_init'] = float(input((" " * 45) + "* Informe o VALOR INICIAL: "))
    except ValueError:
        prints.get_clear_prompt()
        prints.get_report_error("O valor inicial deve ser um número.")
        return

    if users == ['']:
        users = []
    dict_data['users'] = users
    dict_resp, status = request.post_create_account(dict_data, int(bank) - 1)
    prints.get_clear_prompt()

    if status == 200:
        prints.get_report_action(dict_resp["descript"])
    elif status == 400:
        prints.get_report_error(dict_resp["descript"])
    else:
        prints.get_report_error("Erro ao tentar criar a conta.")


def operations(bank: int, dict_da) -> None:
    package = {}
    screen.operations_menu(dict_da)
    option = input((" " * 45) + "* Informe a opção desejada: ")

    while option != "4":
        if option == "1":  # Trasferencia
            try:
                bank_t = int(input((" " * 45) + "* Informe o BANCO que a conta está: "))
                num_account = int(input((" " * 45) + "* Informe o NÚMERO DA CONTA: "))
                value = float(input((" " * 45) + "* Informe o VALOR DA TRANSFERÊNCIA: "))
                banco_dest = int(input((" " * 45) + "* Informe o BANCO DESTINO: "))
                pix = input((" " * 45) + "* Informe a CHAVE PIX: ")

                dict_data = {"type": "TRANSFER", "value": value, "sender": num_account, "pix": f"{banco_dest}:{pix}"}
                if bank_t not in package:
                    package[bank_t] = {}

                if num_account not in package[bank_t]:
                    package[bank_t][num_account] = {"package": [dict_data]}
                else:
                    package[bank_t][num_account]["package"].append(dict_data)

                prints.get_clear_prompt()
                prints.get_report_action("Transferência adicionada com sucesso.")

            except ValueError:
                prints.get_clear_prompt()
                prints.get_report_error("O banco e o número da conta devem ser números.")

        elif option == "2":  # Deposito
            try:
                bank_t = int(input((" " * 45) + "* Informe o BANCO que a conta está: "))
                num_account = int(input((" " * 45) + "* Informe o NÚMERO DA CONTA: "))
                value = float(input((" " * 45) + "* Informe o VALOR DO DEPÓSITO: "))

                dict_data = {"type": "DEPOSIT", "value": value, "sender": num_account}
                if bank_t not in package:
                    package[bank_t] = {}

                if num_account not in package[bank_t]:
                    package[bank_t][num_account] = {"package": [dict_data]}
                else:
                    package[bank_t][num_account]["package"].append(dict_data)

                prints.get_clear_prompt()
                prints.get_report_action("Depósito adicionado com sucesso.")
            except ValueError:
                prints.get_clear_prompt()
                prints.get_report_error("O banco e o número da conta devem ser números.")
        elif option == "3":  # Saque
            try:
                bank_t = int(input((" " * 45) + "* Informe o BANCO que a conta está: "))
                num_account = int(input((" " * 45) + "* Informe o NÚMERO DA CONTA: "))
                value = float(input((" " * 45) + "* Informe o VALOR DO SAQUE: "))

                dict_data = {"type": "WITHDRAW", "value": value, "sender": num_account}
                if bank_t not in package:
                    package[bank_t] = {}

                if num_account not in package[bank_t]:
                    package[bank_t][num_account] = {"package": [dict_data]}
                else:
                    package[bank_t][num_account]["package"].append(dict_data)

                prints.get_clear_prompt()
                prints.get_report_action("Saque adicionado com sucesso.")
            except ValueError:
                prints.get_clear_prompt()
                prints.get_report_error("O banco e o número da conta devem ser números.")
        else:
            prints.get_clear_prompt()
            prints.get_report_error("Opção inválida! Tente novamente.")

        screen.operations_menu(dict_da)
        option = input((" " * 45) + "* Informe a opção desejada: ")

    prints.get_clear_prompt()
    screen.pacote_final(package)
    input()

    dict_resp, status = request.post_operations(package, bank)
    if status == 200:
        prints.get_report_action(dict_resp["descript"])
    elif status == 400:
        prints.get_report_error(dict_resp["descript"])
    else:
        prints.get_report_error("Erro ao tentar realizar as operações.")
