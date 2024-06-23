class Event:
    def __init__(self, sender, timestamp, type_msg, id, msg='', number_of_acks=0, num_one_queue=0):
        self.id: str = id
        self.sender = sender
        self.timestamp = timestamp
        self.msg = msg
        self.type_msg = type_msg
        self.number_of_acks: int = number_of_acks
        self.num_one_queue: int = num_one_queue
        self.one_queue: bool = False
        self.fail: bool = False
        self.send: bool = False
        self.loop_wait: bool = True

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
        else:
            self.num_one_queue += 1

    def set_one(self):
        self.one_queue = True

