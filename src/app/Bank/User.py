import re

from src.app.Exception.UserException import UserException


class User:
    def __init__(self, user_name: str, name: str, num_cadastro: str, user_password: str, type_person: str):

        self.user_name: str = user_name
        self.name: str = name
        self.num_cadastro: str = num_cadastro
        self.type_person: str = type_person
        self.user_password: str = user_password
        
    def __str__(self):
        return f'{self.user_name} - {self.name} - {self.num_cadastro} - {self.user_password}'
