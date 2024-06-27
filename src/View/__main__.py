from utils import prints
from enums import Option
from screen import screen
from options import options

def main() -> None:
    try:
        prints.get_clear_prompt()
        menu_main()
    except KeyboardInterrupt:
        return


def menu_main() -> None:
    print("\033[1;97m")
    prints.get_clear_prompt()

    screen.main_menu()
    user_choice: str = input((" " * 45) + "* Informe a opção desejada: ")

    while not (user_choice == Option.END_OPTION.value):
        get_option(user_choice)
        screen.main_menu()
        user_choice = input((" " * 45) + "* Informe a opção desejada: ")


def get_option(user_choice: str) -> None:
    prints.get_clear_prompt()
    match user_choice:
        case Option.REGISTER.value:
            options.register()
        case Option.LOGIN.value:
            pass
        case _: # default
            prints.get_clear_prompt()
            prints.get_report_error("Opção inválida! Tente novamente.")


if __name__ == '__main__':
    main()
