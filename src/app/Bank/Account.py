import datetime
from src.app.Exception.AccountException import AccountException


class Account:
    def __init__(self, type_account: str, password: str, num_account: int, value_init: float) -> None:
        self.valid_data(type_account, value_init)

        self.user_names: list[str] = []
        self.transactions: list[dict[str, str | float]] = []

        self.type_account: str = type_account
        self.password: str = password
        self.kay_pix: str = ""

        self.num_account: int = num_account
        self.balance: float = value_init

        if self.type_account == 'PJ' or self.type_account == 'CONJUNTA':
            self.joint: bool = True
        else:
            self.joint: bool = False

    def valid_data(self, type_account: str, value_init: float) -> None:
        if type_account not in ['PF', 'PJ', 'CONJUNTA']:
            raise AccountException('Tipo de conta inválida')
        elif value_init < 50 and (type_account == 'PF' or type_account == 'CONJUNTA'):
            raise AccountException('Valor inicial inválido, valor mínimo de R$50,00 para pessoas físicas e conjuntas')
        elif value_init < 100 and type_account == 'PJ':
            raise AccountException('Valor inicial inválido, valor mínimo de R$100,00 para pessoas jurídicas')

    def add_users(self, user_name: str) -> None:
        if self.user_names and not self.joint:
            raise AccountException("A conta não é conjunta")
        self.user_names.append(user_name)

    def set_pix_key(self, kay_pix: str) -> None:
        self.kay_pix = kay_pix

    def set_joint(self) -> None:
        self.joint = True

    def deposit(self, value: float, sender: str, bank_id) -> None:
        self.balance += value
        self.insert_transaction('Deposito', value, sender, self.balance - value, self.balance, bank_id)

    def withdraw(self, value: float, sender: str, bank_id) -> None:
        self.is_operation_valid(value, bank_id)
        self.balance -= value
        self.insert_transaction('Saque', -value, sender, self.balance + value, self.balance, bank_id)

    def transfer(self, value: float, sender: str, bank_id) -> None:
        self.is_operation_valid(value, bank_id)
        self.balance -= value
        self.insert_transaction('Transferência pix', -value, sender, self.balance + value, self.balance, bank_id)

    def receive(self, value: float, sender: str, bank_id: int) -> None:
        self.balance += value
        self.insert_transaction('Recepção pix', value, sender, self.balance - value, self.balance, bank_id)

    def insert_transaction(self, type_transaction: str, value: float, sender: str, previous_balance: float,
                           new_balance: float, bank_id: int) -> None:
        data_hora = datetime.datetime.now()
        self.transactions.append({
            'type': type_transaction,
            'value': value,
            'previous_balance': previous_balance,
            'app_balance': new_balance,
            'date': '{}/{}/{}'.format(data_hora.day, data_hora.month, data_hora.year),
            'time': '{}:{}:{}'.format(data_hora.hour, data_hora.minute, data_hora.second),
            'made_by': sender,
            'bank_sender': bank_id
        })

    def is_operation_valid(self, value: float, id_bank: int) -> None:
        if self.balance < value:
            raise AccountException(f'Saldo da conta {self.num_account} insuficiente ({self.balance}) no banco {id_bank}')

    def value_neg(self, value: float):
        if value < 0:
            raise AccountException('Valor inválido')
