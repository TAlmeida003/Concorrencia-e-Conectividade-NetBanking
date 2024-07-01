from src.app.Bank.User import User
from src.app.Bank.Account import Account
from src.app.Exception.AccountException import AccountException
from src.app.Exception.BackException import BankException
from src.app.utils import utils, request
from src.app.enums import Option_Bank
from threading import Thread


class Bank:
    def __init__(self, id_node, list_nodes: list[str], dict_online: dict[str, bool]) -> None:
        self.id = id_node
        self.list_nodes: list[str] = list_nodes

        self.dict_online: dict[str, bool] = dict_online
        self.dict_user: dict[str, User] = {}
        self.dict_account: dict[int, Account] = {}
        self.dict_pix: dict[str, int] = {}
        self.list_pix_all: list[str] = []

    def exe_operation(self, dict_data: dict, type_operation: str) -> None:
        if type_operation == Option_Bank.REGISTER.value:
            self.register_user(
                dict_data['name'],
                dict_data['user_name'],
                dict_data['num_cadastro'],
                dict_data['password'],
                dict_data['type_person']
            )
        elif type_operation == Option_Bank.PACKAGE.value:
            self.exe_package(dict_data)

    def test_exe_operation(self, dict_data: dict, type_operation: str) -> dict[str: str | bool]:
        try:
            if type_operation == Option_Bank.REGISTER.value:
                self.register_user_valid(dict_data['user_name'], dict_data['num_cadastro'])
            elif type_operation == Option_Bank.PACKAGE.value:
                self.valid_account(dict_data)

            return {"code": True, "descript": "Operação realizada com sucesso"}
        except (BankException, AccountException) as e:
            return {"code": False, "descript": "Falha na operação: " + str(e)}

    def valid_account(self, dict_data: dict[str, dict[int, dict[str, list[dict[str, str | float]]]]]) -> None:
        if dict_data.get(str(self.id)):
            for account in dict_data[str(self.id)]:
                if not self.dict_account.get(int(account)):
                    raise BankException(f'Conta {account} não encontrada no banco {self.id}')

                cont_deposit = 0
                cont_wt = 0
                for package in dict_data[str(self.id)][account]['package']:

                    self.dict_account[int(account)].value_neg(package['value'])
                    if package['type'] == Option_Bank.DEPOSIT.value:
                        cont_deposit += package['value']
                    elif package['type'] == Option_Bank.TRANSFER.value and package['pix'] not in self.list_pix_all:
                        raise BankException(f'Chave pix {package["pix"]} não encontrada')
                    elif package['type'] == Option_Bank.TRANSFER.value and not self.dict_online[self.list_nodes[int(package['pix'].split(':')[0])]]:
                        raise BankException(f'Banco {package["pix"].split(":")[0]} não está online para transferência')
                    else:
                        cont_wt += package['value']
                        value = cont_wt - cont_deposit
                        self.dict_account[int(account)].is_operation_valid(value, self.id)

        self.bank_is_package(dict_data)

    def exe_package(self, dict_data):
        if dict_data.get(str(self.id)):
            for account in dict_data[str(self.id)]:
                for package in dict_data[str(self.id)][account]['package']:
                    if package['type'] == Option_Bank.DEPOSIT.value:
                        self.dict_account[int(account)].deposit(package['value'], package['sender'], self.id)
                    elif package['type'] == Option_Bank.WITHDRAW.value:
                        self.dict_account[int(account)].withdraw(package['value'], package['sender'], self.id)
                    elif package['type'] == Option_Bank.TRANSFER.value:
                        self.transfer_main(package, int(account))

    def transfer_main(self, dict_data: dict[str, str | float], account: int) -> None:
        self.dict_account[account].transfer(dict_data['value'], dict_data['sender'], self.id)
        if dict_data['pix'].split(':')[0] != self.list_nodes[self.id]:  # Transferência entre bancos
            request.post_receiver_pix(dict_data, int(dict_data['pix'].split(':')[0]), self.list_nodes, self.dict_online)
        else:  # Transferência interna
            self.receiver_pix(dict_data)

    def receiver_pix(self, dict_data: dict[str, str | float]) -> None:
        account: int = self.dict_pix[dict_data['pix']]
        self.dict_account[account].receive(dict_data['value'], dict_data['sender'], self.id)

    def register_user(self, name: str, user_name: str, num_register: str, user_password: str, type_person: str):
        user: User = User(user_name, name, num_register, user_password, type_person)
        self.dict_user[user.user_name] = user

    def register_user_valid(self, user_name: str, num_register: str):
        if user_name in self.dict_user:
            raise BankException(f'Nome de usuário "{user_name}" já existe no banco {self.id}')

        for user in self.dict_user.values():
            if user.num_cadastro == num_register:
                type_cadastro = 'CPF' if user.type_person == 'PF' else 'CNPJ'
                raise BankException(f'{type_cadastro} "{num_register}" já cadastrado no banco {self.id}')

    def login(self, user_name: str, user_password: str) -> dict[str, str | dict]:
        if user_name not in self.dict_user:
            raise BankException('Usuário não encontrado')

        dict_dados_user: dict[str, str | dict] = self.dict_user[user_name].login(user_password)

        list_accounts: list[list[int | float]] = []
        for account in self.dict_user[user_name].accounts:
            list_accounts.append([account, self.dict_account[account].balance, self.dict_account[account].kay_pix])
        dict_dados_user['accounts'] = {str(self.id): list_accounts}

        for node in range(len(self.list_nodes)):
            if node != self.id and self.dict_online[self.list_nodes[node]]:
                dict_dados_user['accounts'] = (dict_dados_user['accounts'] |
                                               request.get_accounts_user(user_name, node, self.list_nodes)
                                               )
        return dict_dados_user

    def create_conta(self, user_name: str, type_account: str, password: str, pix_type: str,
                     users: list[str], value_init: float) -> None:
        if user_name not in self.dict_user:
            raise BankException('Usuário não encontrado')

        num_account: int = utils.get_account(list(self.dict_account))
        kay_pix: str = utils.generate_pix_key(user_name, num_account, pix_type, self.dict_user[user_name].num_cadastro,
                                              list(self.dict_pix), self.id
                                              )

        account: Account = Account(type_account, password, num_account, value_init)
        account.add_users(user_name)
        account.set_pix_key(kay_pix)

        self.add_user_account(users, type_account, num_account, account)
        self.dict_account[num_account] = account
        self.dict_pix[kay_pix] = num_account
        self.dict_user[user_name].add_account(num_account)
        self.list_pix_all.append(kay_pix)

        for node in range(len(self.list_nodes)):
            if node != self.id and self.dict_online[self.list_nodes[node]]:
                Thread(target=request.post_receiver_pix_all,
                       args=(kay_pix, node, self.list_nodes, self.dict_online)).start()

    def add_user_account(self, users: list[str], type_account: str, num_account: int, account: Account) -> None:
        if users and type_account == 'CONJUNTA':
            for user in users:
                if user not in self.dict_user:
                    raise BankException(f'Usuário {user} não encontrado')
                account.add_users(user)
                self.dict_user[user].add_account(num_account)

    def bank_is_package(self, dict_data) -> None:
        for node in dict_data:
            if not self.dict_online[self.list_nodes[int(node)]]:
                raise BankException(f'Banco {node} não está online')
