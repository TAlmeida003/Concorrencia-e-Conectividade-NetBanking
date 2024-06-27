import src.view.utils.utils as utils
import src.view.utils.prints as prints
import src.view.utils.request as request
import src.view.screen.screen as screen


def register():
    dict_user: dict = {}
    screen.register_menu()
    dict_user["name"]: str = input((" " * 45) + "* Informe o NOME COMPLETO do usuário: ")
    dict_user["type_person"]: str = input((" " * 45) + "* Informe o TIPO DE PESSOA do usuário: ")
    num_id: str = input((" " * 45) + "* Informe o NÚMERO DE IDENTIFICAÇÃO do usuário: ")

    try:
        if dict_user["type_person"] == "PF":
            dict_user["num_cadastro"] = utils.formatar_cpf(num_id)
        elif dict_user["type_person"] == "PJ":
            dict_user["num_cadastro"] = utils.formatar_cnpj(num_id)
        else:
            raise RuntimeError("O tipo de pessoa deve ser 'PF' ou 'PJ'")

    except RuntimeError as error:
        prints.get_clear_prompt()
        prints.get_report_error(str(error))
        return

    prints.get_clear_prompt()
    screen.register_menu()
    dict_user["user_name"]: str = input((" " * 45) + "* Informe o NOME DE USUÁRIO do usuário: ")
    dict_user["password"]: str = input((" " * 45) + "* Informe a SENHA do usuário: ")

    prints.get_clear_prompt()
    dict_response, status = request.post_register_user(dict_user)
    if status == 200:
        prints.get_report_action(dict_response["descript"])
    elif status == 400:
        prints.get_report_error(dict_response["descript"])
    else:
        prints.get_report_error("Erro ao tentar registrar o usuário.")
