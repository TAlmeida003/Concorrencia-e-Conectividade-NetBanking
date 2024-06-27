import os


def get_report_error(text: str) -> None:
    SIZE_CENTER_TEXT: int = 170
    NUM_BAR: int = 48

    print(get_paint_color("RED"), ('=-' * NUM_BAR).center(SIZE_CENTER_TEXT))
    print("ERRO!!!".center(SIZE_CENTER_TEXT + 1))
    print(text.center(SIZE_CENTER_TEXT))
    print(('=-' * NUM_BAR).center(SIZE_CENTER_TEXT + 3), get_paint_color())


def get_paint_color(color: str = "WHITE") -> str:
    dict_color: dict[str, str] = {"RED": "\033[1;31m", "BLUE": "\033[1;34m", "YELLOW": "\033[1;33m",
                                  "GREEN": "\033[1;32m"}
    if color in dict_color:
        return dict_color[color]

    return "\033[1;97m"


def get_report_action(text: str) -> None:
    SIZE_CENTER_TEXT: int = 170
    NUM_BAR: int = 48

    print(get_paint_color("GREEN"), ('=-' * NUM_BAR).center(SIZE_CENTER_TEXT))
    print("AÇÃO REALIZADA COM SUCESSO!!!".center(SIZE_CENTER_TEXT + 1))
    print(text.center(SIZE_CENTER_TEXT))
    print(('=-' * NUM_BAR).center(SIZE_CENTER_TEXT + 3), get_paint_color())


def get_clear_prompt() -> None:
    if os.name == 'nt':
        os.system('cls') or None
    else:
        os.system('clear') or None


def get_baseboard() -> None:
    SIZE_CENTER: int = 170
    print(("-=" * 45).center(SIZE_CENTER - 2))


def header(text: str) -> None:
    get_baseboard()
    print(f"|{text: ^86}|".center(168))
    get_baseboard()
    print(("=-" * 25).center(168))
    print(("=-" * 15).center(168))


def topic(text: str) -> None:
    print()
    print(f"=================== {text: ^15} ===================".center(170))
    print()


def jump_line(num: int) -> None:
    for i in range(num):
        print(f"|{'': ^86}|".center(168))


def get_display_option(num_option: str, name_option: str) -> None:
    jump_line(3)
    print(f"|{'[ ' + num_option + ' ] — ' + name_option: ^86}|".center(168))


def get_display_option_two(list_option: list[str]):
    for i in range(1, len(list_option), 2):
        print(f"[ {i: ^1} ] - {list_option[i - 1]:^26}        [ {i + 1:^1} ] - {list_option[i]:^26}".center(170))
        jump_line(3)
