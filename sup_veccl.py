import time
import numpy as np

'''
Implementation of Replay Clock that uses dicts to store
offsets and counters between the current process and other
processes. As a result, the bitmap field is not required.
'''
class VecCl:
    def __init__(self, proc_id: int, proc_count: int, counter_bit_width: int) -> None:
        self.proc_id = proc_id
        self.proc_count = proc_count
        self.counter_bit_width = counter_bit_width
        self.counter_array = [np.uint64(0) for _ in np.arange(proc_count)]

    def __repr__(self) -> str:
        return f'VectorCl(proc_id={self.proc_id}, counters={self.counter_array})'
    
    def to_dict(self) :
        return {'proc_id' : str(self.proc_id), 
                'counters' : str(self.counter_array)}

    def advance(self) -> float:
        starttime = time.time()

        if (self.counter_array[self.proc_id] + 1) < (1 << self.counter_bit_width):
            self.counter_array[self.proc_id] += 1
        endtime = time.time()

        return endtime - starttime

    def merge(self, other_counter) -> float:
        starttime = time.time()

        for i in range(self.proc_count):
            self.counter_array[i] = max(self.counter_array[i], other_counter.counter_array[i])
        self.advance()

        endtime = time.time()
        return endtime - starttime