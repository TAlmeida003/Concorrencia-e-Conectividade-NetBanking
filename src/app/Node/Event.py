class Event:
    def __init__(self, sender, timestamp, type_msg, id, msg=None, number_of_acks=0, num_one_queue=0):
        if msg is None:
            msg = {}
        self.id: str = id
        self.sender = sender
        self.timestamp = timestamp
        self.msg = msg
        self.type_msg = type_msg
        self.number_of_acks: int = number_of_acks
        self.num_one_queue: int = num_one_queue

        self.one_queue: bool = False  # é o primeiro da lista de todos os bancos
        self.fail: bool = False  # Não é o primeiro da lista de algum banco
        self.send: bool = False  # Controle de envio de mensagens para os peers
        self.loop_wait: bool = True  # Controle do loop de envio de novas mensagens
        self.exe: bool = False  # Já terminou de ser execultado pelo banco e sair do loop de espera de request
        self.can_be_executed: bool = True  # Pode ser execultado pelo banco
        self.mgs_executed: str = ""  # Mensagem que foi execultada ou nao

    def __lt__(self, other) -> bool:
        if self.timestamp == other.timestamp:
            return self.sender < other.sender
        return self.timestamp < other.timestamp

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def add_ack(self):
        self.number_of_acks += 1

    def add_num_one_queue(self, num_peers: int, mgs: str):
        if self.num_one_queue + 1 > num_peers:
            self.num_one_queue = 1
            if mgs == "ONE_QUEUE":
                self.fail = False
                self.can_be_executed = True
                self.mgs_executed = ""
        else:
            self.num_one_queue += 1

    def set_one(self):
        self.one_queue = True
