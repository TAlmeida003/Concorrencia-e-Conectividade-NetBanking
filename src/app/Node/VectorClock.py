from threading import Lock


class VectorClock:
    def __init__(self, total_nodos: int, node_id):
        self.vector_clock: list[int] = [0] * total_nodos
        self.node_id = node_id
        self.lock = Lock()

    def incrementar(self) -> list[int]:
        with self.lock:
            self.vector_clock[self.node_id] += 1
            return self.vector_clock.copy()

    def atualizar(self, vetor_remetente: list[int]) -> list[int]:
        with self.lock:
            self.vector_clock = [max(self.vector_clock[i], vetor_remetente[i]) for i in range(len(self.vector_clock))]
            return self.vector_clock.copy()

    def obter(self) -> list[int]:
        return self.vector_clock.copy()

    def __repr__(self) -> str:
        return str(self.vector_clock)
