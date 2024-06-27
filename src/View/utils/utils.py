def formatar_cpf(numero: str) -> str:
    # Converte o número para string, caso ainda não seja
    cpf = str(numero)

    # Verifica se o comprimento é 11
    if len(cpf) != 11 or not cpf.isdigit():
        raise RuntimeError("O número deve conter 11 dígitos.")

    # Formata o CPF
    cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    return cpf_formatado


def formatar_cnpj(numero: str) -> str:
    # Converte o número para string, caso ainda não seja
    cnpj = str(numero)

    # Verifica se o comprimento é 14
    if len(cnpj) != 14 or not cnpj.isdigit():
        raise RuntimeError("O número deve conter 14 dígitos.")

    # Formata o CNPJ
    cnpj_formatado = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

    return cnpj_formatado
