from enum import Enum


class Option_Bank(Enum):
    REGISTER: str = "REGISTER"
    PACKAGE: str = "PACKAGE"
    DEPOSIT: str = "DEPOSIT"
    WITHDRAW: str = "WITHDRAW"
    TRANSFER: str = "TRANSFER"
