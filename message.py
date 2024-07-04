from repcl import RepCl
from veccl import VecCl

class Message:
    def __init__(self, proc_id: int ,repcl: RepCl, veccl: VecCl, data: bytes) -> None:
        self.proc_id = proc_id
        self.repcl = repcl
        self.veccl = veccl
        self.data = data

    def __repr__(self) -> str:
        return f'Message(replay clock={self.clock}, data={self.data})'