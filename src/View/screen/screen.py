from src.view.utils import prints


LIST_OPTIONS: list[str] = ["Registrar Usuário", "Login do Usuário", "Encerrar Programa"]


def main_menu() -> None:
    prints.header("NetBanking - Bancos Distribuídos")
    prints.topic("MENU PRINCIPAL")

    prints.get_baseboard()
    menu_options = [
        ("1", "Registrar Usuário"),
        ("2", "Login do Usuário"),
        ("3", "Encerrar Programa")
    ]

    for option, description in menu_options:
        prints.get_display_option(option, description)

    prints.jump_line(3)
    prints.get_baseboard()


def register_menu() -> None:
    prints.header("NetBanking - Bancos Distribuídos")
    prints.topic("REGISTRAR USUÁRIO")
    prints.get_baseboard()
    prints.jump_line(3)

    instructions = [
        "Preencha os campos abaixo com as seguintes informações:",
        'O campo "Nome" deve conter apenas letras e espaços.',
        'O campo "Número de Identificação" deve conter o CPF ou CNPJ.',
        'O campo "Senha" deve conter letras, números e caracteres especiais.',
        'O campo "Nome de Usuário" deve conter letras, números e caracteres especiais.',
        'O campo "Tipo de Pessoa" deve ser "PF" (Pessoa Física) ou "PJ" (Pessoa Jurídica).'
    ]

    for instruction in instructions:
        print(f"|{instruction: ^86}|".center(168))
        prints.jump_line(1)

    prints.jump_line(3)
    prints.get_baseboard()
