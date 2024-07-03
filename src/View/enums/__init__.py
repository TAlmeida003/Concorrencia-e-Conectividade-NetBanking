from enum import Enum


class Option(Enum):
    REGISTER: str = "1"
    LOGIN: str = "2"
    SELECT_BANK: str = "3"
    END_OPTION: str = "4"
