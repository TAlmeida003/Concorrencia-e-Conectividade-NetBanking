from utils import prints
from enums import Option
from screen import screen
from options import options


def main() -> None:
    try:
        print("\033[1;97m")
        prints.get_clear_prompt()
        menu_main()
    except KeyboardInterrupt:
        return


def menu_main() -> None:
    bank = options.banks()

    screen.main_menu(bank)
    user_choice: str = input((" " * 45) + "* Informe a opção desejada: ")

    while not (user_choice == Option.END_OPTION.value):
        if bank != -1 or user_choice == Option.SELECT_BANK.value:
            bank = get_option(user_choice, bank)
        else:
            prints.get_clear_prompt()
            prints.get_report_error("É necessário selecionar um banco que esteja disponível.")

        screen.main_menu(bank)
        user_choice = input((" " * 45) + "* Informe a opção desejada: ")


def get_option(user_choice: str, bank) -> int:
    match user_choice:
        case Option.REGISTER.value:
            prints.get_clear_prompt()
            options.register(bank)
        case Option.LOGIN.value:
            options.login(bank)
        case Option.SELECT_BANK.value:
            prints.get_clear_prompt()
            return options.banks()
        case _:  # default
            prints.get_clear_prompt()
            prints.get_report_error("Opção inválida! Tente novamente.")

    return bank


if __name__ == '__main__':
    main()
