import time
import numpy as np
import math

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

    @staticmethod
    def extract(number, k, p):
        return ((1 << k) - 1) & (number >> p)
    
    def remove_offset_at_index(self, index):
        # 010 011 101
        #   2   1   0

        # 010 101 111 010 011
        # 000 010 101 000 000 


        new_offset = self.offsets >> self.bits_per_offset
        new_offset = new_offset >> (index * self.bits_per_offset)
        new_offset = new_offset << (index * self.bits_per_offset)

        self.offsets = self.offsets << (64 - (index * self.bits_per_offset))
        self.offsets = self.offsets >> (64 - (index * self.bits_per_offset))

        self.offsets |= new_offset

    def shift(self, new_hlc):
        index = 0

        bitmap = self.offset_bmp
        while (bitmap > 0):
            process_id = np.uint64(math.log2((~(bitmap ^ (~(bitmap - 1))) + 1) >> 1))
            offset_at_index = self.get_offset_at_index(index)
            new_offset = math.min(new_hlc - (self.hlc - offset_at_index), self.epsilon)

            if (new_offset >= self.epsilon):
                self.remove_offset_at_index(index)
                self.offset_bmp = self.offset_bmp & ~(1 << process_id)
            else:
                self.set_offset_at_index(index, new_offset)
                self.offset_bmp = self.offset_bmp | (1 << process_id)
            
            bitmap = bitmap & (bitmap - 1)
            index += 1
        
        self.hlc = new_hlc

    def set_offset_at_index(self, index, new_offset):
        if new_offset > (1 << self.bits_per_offset) - 1:
            raise ValueError('Offset value too large')
        
        mask = np.uint64((1 << self.bits_per_offset) - 1) << (index * self.bits_per_offset)
        mask = ~mask

        self.offsets = self.offsets & mask
        self.offsets = self.offsets | (new_offset << (index * self.bits_per_offset))

    def get_offset_at_index(self, index):
        offset = self.extract(self.offsets, self.bits_per_offset, index * self.bits_per_offset)
        return offset

    def send_local(self) -> None:
        new_hlc = math.max(self.hlc, self.get_current_epoch())
        new_offset = new_hlc - self.node_hlc
        offset_at_pid = self.get_offset_at_index(self.proc_id)

        if (new_hlc == self.hlc and offset_at_pid <= new_offset):
            self.counters += 1
        elif (new_hlc == self.hlc):
            new_offset = math.min(new_offset, offset_at_pid)

            index = 0
            bitmap = self.offset_bmp    
            while (bitmap > 0):
                process_id = math.log2((~(bitmap ^ (~(bitmap - 1))) + 1) >> 1)
                if (process_id == self.proc_id):
                    self.set_offset_at_index(index, new_offset)
                    self.offset_bmp = self.offset_bmp | (1 << process_id)
                
                bitmap = bitmap & (bitmap - 1)
                index += 1
            
            self.counters = 0
            self.offset_bmp = self.offset_bmp | (1 << self.proc_id)
        else:
            self.counters = 0
            self.shift(new_hlc)

            index = 0
            bitmap = self.offset_bmp
            while (bitmap > 0):
                process_id = math.log2((~(bitmap ^ (~(bitmap - 1))) + 1) >> 1)
                if (process_id == self.proc_id):
                    self.set_offset_at_index(index, 0)
                    self.offset_bmp = self.offset_bmp | (1 << process_id)

                bitmap = bitmap & (bitmap - 1)
                index += 1

            self.offset_bmp = self.offset_bmp | (1 << self.proc_id)