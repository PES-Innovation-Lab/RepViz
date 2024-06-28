from repcl import RepCl

class Message:
    def __init__(self, clock: RepCl, data: bytes) -> None:
        self.clock = clock
        self.data = data

    def __repr__(self) -> str:
        return f'Message(clock={self.clock}, data={self.data})'
