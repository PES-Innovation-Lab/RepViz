import time
import numpy as np

class RepCl:
    def __init__(self, proc_id: int, interval: int, epsilon: float, bits_per_offset: int) -> None:
        self.proc_id = proc_id
        self.interval = interval
        self.epsilon = epsilon
        self.bits_per_offset = bits_per_offset

        self.hlc: np.uint64 = self.get_current_epoch()
        self.offset_bmp = np.uint64(0)
        self.offsets = np.uint64(0)
        self.counters = np.uint64(0)

    def __repr__(self) -> str:
        offset_bmp = bin(self.offset_bmp)[2:].zfill(64)
        offsets = bin(self.offsets)[2:].zfill(64)
        counters = bin(self.counters)[2:].zfill(64)
        return f'RepCl(\n\tproc_id:\t{self.proc_id},\n\thlc:\t\t{self.hlc},\n\toffset_bmp:\t{offset_bmp},\n\toffsets:\t{offsets},\n\tcounters:\t{counters}\n)'

    def get_current_epoch(self) -> np.uint64:
        return np.uint64(time.time() * 1000 / self.interval)
