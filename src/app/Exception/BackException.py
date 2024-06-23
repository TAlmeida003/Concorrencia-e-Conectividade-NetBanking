class BankException(RuntimeError):
    def __init__(self, mensagem):
        super().__init__(mensagem)

    def __str__(self):
        return super().__str__()
