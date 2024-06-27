import re
from typing import Dict

from src.app.Exception.UserException import UserException


class User:
    def __init__(self, user_name: str, name: str, num_cadastro: str, user_password: str, type_person: str):

        self.user_name: str = user_name
        self.name: str = name
        self.num_cadastro: str = num_cadastro
        self.type_person: str = type_person
        self.user_password: str = user_password

        self.accounts: list[int] = []

    def login(self, user_password: str) -> dict[str, str | list]:
        if self.user_password != user_password:
            raise UserException('Senha inválidos')

        return {'user_name': self.user_name,
                'name': self.name,
                'num_cadastro': self.num_cadastro,
                'type_person': self.type_person}

    def add_account(self, account: int) -> None:
        self.accounts.append(account)

    def __str__(self):
        return f'{self.user_name} - {self.name} - {self.num_cadastro} - {self.user_password}'
