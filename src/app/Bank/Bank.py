from src.app.Bank.User import User
from src.app.Bank.Account import Account
from src.app.Exception.BackException import BankException
from src.app.utils import utils, request
from src.app.enums import Option_Bank


class Bank:
    def __init__(self, id_node, list_nodes: list[str]):
        self.id = id_node
        self.list_nodes: list[str] = list_nodes

        self.dict_user: dict[str, User] = {}
        self.dict_account: dict[int, Account] = {}
        self.dict_pix: dict[str, int] = {}  # key: pix, value: num_account

    def register_user(self, name: str, user_name: str, num_register: str, user_password: str, type_person: str):
        user: User = User(user_name, name, num_register, user_password, type_person)
        self.dict_user[user.user_name] = user

    def exe_operation(self, dict_data: dict, type_operation: str) -> None:
        if type_operation == Option_Bank.REGISTER.value:
            self.register_user(dict_data['name'], dict_data['user_name'], dict_data['num_cadastro'],
                               dict_data['password'], dict_data['type_person'])

    def test_exe_operation(self, dict_data: dict, type_operation: str) -> dict[str: str | bool]:
        try:
            if type_operation == Option_Bank.REGISTER.value:
                self.register_user_valid(dict_data['user_name'], dict_data['num_cadastro'])

            return {"code": True, "descript": "Operação realizada com sucesso"}
        except BankException as e:
            return {"code": False, "descript": "Falha na operação: " + str(e) + f" no banco {self.id}"}

    def register_user_valid(self, user_name: str, num_register: str):
        if user_name in self.dict_user:
            raise BankException(f'Nome de usuário "{user_name}" já existe')

        for user in self.dict_user.values():
            if user.num_cadastro == num_register:
                type_cadastro = 'CPF' if user.type_person == 'PF' else 'CNPJ'
                raise BankException(f'{type_cadastro} "{num_register}" já cadastrado')

    def login(self, user_name: str, user_password: str) -> dict[str, str | dict]:
        if user_name not in self.dict_user:
            raise BankException('Usuário não encontrado')

        dict_dados_user: dict[str, str | dict] = self.dict_user[user_name].login(user_password)

        list_accounts: list[list[int | float]] = []
        for account in self.dict_user[user_name].accounts:
            list_accounts.append([account, self.dict_account[account].balance])
        dict_dados_user['accounts'] = {str(self.id): list_accounts}

        for node in range(len(self.list_nodes)):
            if node != self.id:
                dict_dados_user['accounts'] = (dict_dados_user['accounts'] |
                                               request.get_accounts_user(user_name, node, self.list_nodes))
        return dict_dados_user

    def create_conta(self, user_name: str, type_account: str, password: str, pix_type: str, users: list[str]) -> None:
        if user_name not in self.dict_user:
            raise BankException('Usuário não encontrado')

        num_account: int = utils.get_account(list(self.dict_account))
        kay_pix: str = utils.generate_pix_key(user_name, num_account, pix_type, self.dict_user[user_name].num_cadastro,
                                              list(self.dict_pix))

        account: Account = Account(type_account, password, num_account)
        account.add_users(user_name)
        account.set_pix_key(kay_pix)

        self.add_user_account(users, type_account, num_account, account)

        self.dict_account[num_account] = account
        self.dict_pix[kay_pix] = num_account
        self.dict_user[user_name].add_account(num_account)

    def add_user_account(self, users: list[str], type_account: str, num_account: int, account: Account) -> None:
        if users and type_account == 'CONJUNTA':
            for user in users:
                if user not in self.dict_user:
                    raise BankException(f'Usuário {user} não encontrado')
                account.add_users(user)
                self.dict_user[user].add_account(num_account)
