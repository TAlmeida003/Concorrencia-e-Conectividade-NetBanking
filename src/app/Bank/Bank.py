from src.app.Bank.User import User
from src.app.Exception.BackException import BankException


class Bank:
    def __init__(self):
        self.dict_user: dict[str: User] = {}

    def register_user(self, name: str, user_name: str, num_register: str, user_password: str, type_person: str):
        user: User = User(user_name, name, num_register, user_password, type_person)
        self.dict_user[user.user_name] = user

    def exe_operation(self, dict_data: dict, type_operation: str) -> None:
        if type_operation == "REGISTER":
            self.register_user(dict_data['name'], dict_data['user_name'], dict_data['num_cadastro'],
                               dict_data['password'], dict_data['type_person'])

    def test_exe_operation(self, dict_data: dict, type_operation: str) -> dict:
        try:
            if type_operation == "REGISTER":
                self.register_user_valid(dict_data['user_name'], dict_data['num_cadastro'])

            return {"code": True, "msg": "Operação realizada com sucesso"}
        except BankException as e:
            return {"code": False, "msg": str(e)}

    def register_user_valid(self, user_name: str, num_register: str):
        if user_name in self.dict_user:
            raise BankException('Nome de usuário já existe')

        for user in self.dict_user.values():
            if user.num_cadastro == num_register:
                type_cadastro = 'CPF' if user.type_person == 'PF' else 'CNPJ'
                raise BankException(f'{type_cadastro} já cadastrado')

