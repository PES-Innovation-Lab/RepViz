from repcl import RepCl
from veccl import VecCl

class RepClMessage:
    def __init__(self, clock: RepCl, data: bytes) -> None:
        self.clock = clock
        self.data = data

    def __repr__(self) -> str:
        return f'Message(replay clock={self.clock}, data={self.data})'

class VecClMessage:
    def __init__(self, clock: VecCl, data: bytes) -> None:
        self.clock = clock
        self.data = data

    def __repr__(self) -> str:
        return f'Message(vector clock={self.clock}, data={self.data})'