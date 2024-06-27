import datetime
from src.app.Exception.AccountException import AccountException


class Account:
    def __init__(self, type_account: str, password: str, num_account: int) -> None:
        self.valid_data(type_account)

        self.user_names: list[str] = []
        self.transactions: list[dict[str, str | float]] = []

        self.type_account: str = type_account
        self.password: str = password
        self.kay_pix: str = ""

        self.num_account: int = num_account
        self.balance: float = 0.0

        if self.type_account == 'PJ' or self.type_account == 'CONJUNTA':
            self.joint: bool = True
        else:
            self.joint: bool = False

    def valid_data(self, type_account: str) -> None:
        if type_account not in ['PF', 'PJ', 'CONJUNTA']:
            raise AccountException('Tipo de conta inválida')

    def add_users(self, user_name: str) -> None:
        if self.user_names and not self.joint:
            raise AccountException("A conta não é conjunta")
        self.user_names.append(user_name)

    def set_pix_key(self, kay_pix: str) -> None:
        if self.kay_pix:
            raise AccountException("Chave pix já cadastrada")

        self.kay_pix = kay_pix

    def set_joint(self) -> None:
        self.joint = True

