import asyncio
import heapq
import time
import socket
from threading import Lock, Thread

from src.app.Node.VectorClock import VectorClock
from src.app.Node.Event import Event
from src.app.utils import utils
from src.app.utils import request


class Node:
    def __init__(self, node_id: int, list_nodes: list[str]):
        self.id: int = node_id
        self.vector_clock: VectorClock = VectorClock(len(list_nodes), node_id)

        self.peers: list[str] = list_nodes
        self.FIFO_evento: list[Event] = []

        self.dict_ack: dict[str: int] = {}
        self.dict_one_queue: dict[str: int] = {}
        self.dict_peers_online: dict[str: bool] = {}

        self.msg_lock: Lock = Lock()
        self.ack_lock: Lock = Lock()

        utils.fail_dict_peers_online(self.dict_peers_online)

        Thread(target=self.init_check_queue).start()
        Thread(target=self.exe_one_queue).start()
        Thread(target=self.is_online).start()

    def propose_value(self, value: str) -> None:
        timestamp = self.vector_clock.incrementar()
        event = Event(self.id, timestamp, 'PROPOSE', utils.get_id_event(self.id, self.FIFO_evento), value)
        heapq.heappush(self.FIFO_evento, event)
        # Envia o evento para todos exceto ele msm
        for node in range(len(self.peers)):
            if node != self.id and self.dict_peers_online[self.peers[node]]:
                Thread(target=request.post_receiver_message, args=(event, node, self.peers, self.dict_peers_online)).start()

        if utils.len_nodes_online(self.dict_peers_online) == 1:
            self.dict_ack[event.id] = 0

    def receiver_message(self, event: Event) -> None:
        with self.msg_lock:
            self.vector_clock.atualizar(event.timestamp)
            send_ack: bool = self.add_event_in_FIFO_event(event)
        if send_ack:
            self.send_ack(event)

    def add_event_in_FIFO_event(self, event: Event) -> bool:
        if event not in self.FIFO_evento:
            heapq.heappush(self.FIFO_evento, event)
            self.add_ack(event.id)
            return True
        return False

    def send_ack(self, event: Event):
        for node in range(len(self.peers)):
            if node != self.id and self.dict_peers_online[self.peers[node]]:
                Thread(target=request.post_receiver_ack, args=(event.id, node, self.peers, self.dict_peers_online)).start()

    def receiver_ack(self, event_id: str):
        with self.ack_lock:
            self.add_ack(event_id)

    def add_ack(self, event_id):
        if event_id in self.dict_ack:
            self.dict_ack[event_id] += 1
        else:
            self.dict_ack[event_id] = 1

    def init_check_queue(self) -> None:
        while True:
            if self.FIFO_evento and self.FIFO_evento[0].sender == self.id and not self.FIFO_evento[0].one_queue:
                event = self.FIFO_evento[0]
                if event.id in self.dict_ack and self.dict_ack[event.id] == utils.len_nodes_online(self.dict_peers_online) - 1:
                    with self.msg_lock:
                        self.FIFO_evento[0].fail = False
                        if utils.len_nodes_online(self.dict_peers_online) > 1:
                            self.FIFO_evento[0].loop_wait = True
                        else:
                            self.FIFO_evento[0].loop_wait = False
                            event.set_one()
                        self.FIFO_evento[0].num_one_queue = 1
                    self.send_total_one_queue(event)

    def send_total_one_queue(self, event: Event):
        self.total_one_queue(event.id)
        while event.loop_wait:  # retirar
            time.sleep(0.1)

    def total_one_queue(self, event_id: str) -> None:
        self.FIFO_evento[0].send = False
        for node in range(len(self.peers)):
            if node != self.id and self.dict_peers_online[self.peers[node]]:
                Thread(target=request.post_init_check_queue, args=(event_id, node, self.peers, self.dict_peers_online)).start()
        self.FIFO_evento[0].send = True

    def exe_one_queue(self) -> None:
        while True:
            with self.msg_lock:
                if self.FIFO_evento and self.FIFO_evento[0].one_queue and self.FIFO_evento[0].send:
                    event = self.FIFO_evento[0]
                    print(f"DELIVER: {event}")
                    heapq.heappop(self.FIFO_evento)
                    self.dict_ack.pop(event.id)

            time.sleep(0.1)

    def send_one_queue(self, event_id: str) -> None:
        with self.msg_lock:
            # Definir a mensagem
            mgs: str = self.get_mgs_one_queue(event_id)
            index: int = utils.get_index_event(event_id, self.FIFO_evento)

            self.FIFO_evento[index].add_num_one_queue(utils.len_nodes_online(self.dict_peers_online), mgs)

            event = self.FIFO_evento[index]
            self.controller_num_queue(index, event_id, mgs)
        self.send_mgs_one_queue(event, mgs)

    def send_mgs_one_queue(self, event: Event, mgs: str) -> None:
        event.send = False

        for node in range(len(self.peers)):
            if node != self.id and self.dict_peers_online[self.peers[node]]:
                Thread(target=request.post_receiver_one_queue, args=(event.id, mgs, node, self.peers, self.dict_peers_online)).start()

        event.send = True

    def get_mgs_one_queue(self, event_id: str) -> str:
        if event_id == self.FIFO_evento[0].id:
            return "ONE_QUEUE"
        return "NOT_ONE_QUEUE"

    def controller_num_queue(self, index: int, event_id: str, mgs: str) -> None:

        self.FIFO_evento[index].add_num_one_queue(utils.len_nodes_online(self.dict_peers_online), mgs)
        if mgs == "NOT_ONE_QUEUE":
            self.FIFO_evento[index].fail = True

        if event_id == self.FIFO_evento[0].id and self.FIFO_evento[0].num_one_queue == utils.len_nodes_online(self.dict_peers_online) and \
                not self.FIFO_evento[0].fail and mgs == "ONE_QUEUE":
            self.FIFO_evento[0].set_one()
            self.FIFO_evento[index].loop_wait = False
        elif self.FIFO_evento[index].num_one_queue == utils.len_nodes_online(self.dict_peers_online) and not self.FIFO_evento[index].one_queue:
            self.FIFO_evento[index].fail = False
            self.FIFO_evento[index].loop_wait = False
            self.FIFO_evento[index].num_one_queue = 0

    def receiver_one_queue(self, event_id: str, mgs: str) -> None:
        with self.msg_lock:
            index: int = utils.get_index_event(event_id, self.FIFO_evento)
            self.controller_num_queue(index, event_id, mgs)

    def is_online(self) -> None:
        while True:
            try:
                time_init = time.time()
                socket.create_connection(("8.8.8.8", 53), timeout=5)
                if not self.dict_peers_online[self.peers[self.id]]:
                    self.dict_peers_online[self.peers[self.id]] = True
                    self.FIFO_evento.clear()
                    self.dict_ack.clear()
                    Thread(target=self.check_nodes_online).start()
                utils.delay_time(time_init)
            except OSError:
                self.FIFO_evento.clear()
                self.dict_ack.clear()
                utils.fail_dict_peers_online(self.dict_peers_online)

    def check_nodes_online(self):
        while self.dict_peers_online[self.peers[self.id]]:
            asyncio.run(request.main_check(self.id, self.dict_peers_online))
