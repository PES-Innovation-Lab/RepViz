import math
import time

'''
Implementation of Replay Clock that uses dicts to store
offsets and counters between the current process and other
processes. As a result, the bitmap field is not required.
'''
class RepCl:
    def __init__(
        self,
        proc_id: int,
        interval: int,
        epsilon: int,
    ) -> None:
        self.proc_id = proc_id    # current process ID
        self.interval = interval  # duration of an epoch (TODO)
        self.epsilon = epsilon    # maximum acceptable clock skew in ms
        # epoch of the current process (current time in ms divided by the interval)
        self.epoch = self.get_current_epoch(interval)

        # offsets in a (key: val) format.
        # (proc_id: offset of process `proc_id` with respect to this process)
        self.offsets = {proc_id: 0}  # offset with respect to this process is always 0

        # counters in a (key: val) format.
        # (proc_id: counter of process `proc_id` with respect to this process)
        self.counters = {proc_id: 0}  # initialize counter of this process to 0

    def __repr__(self) -> str:
        return f'RepCl(proc_id={self.proc_id}, epoch={self.epoch}, offsets={self.offsets}, counters={self.counters})'

    @staticmethod
    def get_current_epoch(interval: int) -> int:
        return int(time.time() * 1000 / interval)
