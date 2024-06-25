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
        self.counters = {}

    def __repr__(self) -> str:
        return f'RepCl(proc_id={self.proc_id}, epoch={self.epoch}, offsets={self.offsets}, counters={self.counters})'

    '''
    Use system time and calculate the current epoch as
    (unix timestamp in ms) / interval
    '''
    @staticmethod
    def get_current_epoch(interval: int) -> int:
        return int(time.time() * 1000 / interval)

    '''
    Advance the clock by one timestep
    '''
    def advance(self) -> None:
        # calculate the current epoch
        new_epoch = max(self.get_current_epoch(self.interval), self.epoch)

        # if the event occured in the same epoch as the last event
        if self.epoch == new_epoch:
            if self.proc_id in self.counters:
                # increment this process's counter if it already exists
                self.counters[self.proc_id] += 1
            else:
                # or create a counter for this process and start it off with 0
                self.counters[self.proc_id] = 0

        # if the event occurred in a different epoch as the last event
        else:
            # delete all counters because a new epoch was entered
            self.counters.clear()

            # loop through all the offsets
            for p in list(self.offsets.keys()):
                # re-compute the offset with the new epoch
                new_offset = self.offsets[p] + new_epoch - self.epoch  # calculate the new offset
                if new_offset >= self.epsilon:
                    # remove the offset if it is greater than epsilon
                    del self.offsets[p]
                else:
                    # store the re-computed offset if it is still under epsilon
                    self.offsets[p] = new_offset

        self.epoch = new_epoch  # update the epoch
        self.offsets[self.proc_id] = 0  # must always remain 0
