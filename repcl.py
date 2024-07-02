import time

'''
Implementation of Replay Clock that uses dicts to store
offsets and counters between the current process and other
processes. As a result, the bitmap field is not required.
'''
class RepCl:
    def __init__(self, proc_id: int, proc_count: int, field_width: int, interval: int, epsilon: float) -> None:
        self.proc_id = proc_id        # current process ID
        self.proc_count = proc_count  # total number of processes
        self.field_width = field_width    # width of each field in the clock
        self.interval = interval      # duration of an epoch (TODO)
        self.epsilon = epsilon        # maximum acceptable clock skew in ms
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
    Increment the counter corresponding to this process
    '''
    def inc_counter(self) -> None:
        if self.proc_id in self.counters:
            # increment this process's counter if it already exists
            if (self.counters[self.proc_id] + 1) < 2 ** self.field_width:
                self.counters[self.proc_id] += 1
        else:
            # or create a counter for this process and set it to 1
            self.counters[self.proc_id] = 1

    '''
    Set a particular offset to a given value, with bounds checking
    '''
    def set_offset(self, proc_id: int, value: int) -> None:
        if (value + 1) < 2 ** self.field_width:
            self.offsets[proc_id] = value
        else:
            self.offsets[proc_id] = (2 ** self.field_width) - 1

    '''
    Set a particular counter to a given value, with bounds checking
    '''
    def set_counter(self, proc_id: int, value: int) -> None:
        if (value + 1) < 2 ** self.field_width:
            self.counters[proc_id] = value
        else:
            self.counters[proc_id] = (2 ** self.field_width) - 1

    '''
    Advance the clock by one timestep
    '''
    def advance(self) -> None:
        # calculate the current epoch
        new_epoch = max(self.get_current_epoch(self.interval), self.epoch)

        # if the event occured in the same epoch as the last event
        if self.epoch == new_epoch:
            self.inc_counter()  # update counter

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
                    # self.offsets[p] = new_offset
                    self.set_offset(p, new_offset)

        self.epoch = new_epoch  # update the epoch
        # self.offsets[self.proc_id] = 0  # must always remain 0
        self.set_offset(self.proc_id, 0)  # must always remain 0

    '''
    Merge an incoming message's timestamp into self.
    TODO: implement cases where the incoming message
          is not of the same epoch as the latest event
          in the current process.
    '''
    def merge(self, other) -> None:
        # calculate the current epoch
        new_epoch = max(self.get_current_epoch(self.interval), self.epoch, other.epoch)

        # if the message was sent in the same epoch as the latest event in the current process
        if other.epoch == new_epoch == self.epoch:
            # loop through all the counters present in both this timestamp and the other timestamp
            for p in self.counters.keys() & other.counters.keys():
                # update them to the max value
                # self.counters[p] = max(self.counters[p], other.counters[p])
                self.set_counter(p, max(self.counters[p], other.counters[p]))

            # loop through all the new counters that the other timestamp maintains
            for p in other.counters.keys() - self.counters.keys():
                # copy them into our `counters`
                # self.counters[p] = other.counters[p]
                self.set_counter(p, other.counters[p])

            # loop through all the offsets present in both this timestamp and the other timestamp
            for p in self.offsets.keys() & other.offsets.keys():
                # update them to the max value
                # self.offsets[p] = max(self.offsets[p], other.offsets[p])
                self.set_offset(p, max(self.offsets[p], other.offsets[p]))
            # self.offsets[self.proc_id] = 0  # must always remain 0
            self.set_offset(self.proc_id, 0)  # must always remain 0

            # loop through all the new offsets that the other timestamp maintains
            for p in other.offsets.keys() - self.offsets.keys():
                # copy them into our `offsets`
                # self.offsets[p] = other.offsets[p]
                self.set_offset(p, other.offsets[p])

            self.inc_counter()  # update counter

        # if the message is lagging behind
        elif new_epoch == self.epoch:
            self.inc_counter()  # update counter

            # offset of the timestamp of the incoming message
            msg_offset = self.epoch - other.epoch

            # loop through all the new offsets that the other timestamp maintains
            for p in other.offsets.keys() - self.offsets.keys():
                # TODO: finish commenting the code
                if (new_offset := other.offsets[p] + msg_offset) < self.epsilon:
                    # self.offsets[p] = new_offset
                    self.set_offset(p, new_offset)

            if msg_offset < self.epsilon:
                for p in other.counters.keys() - self.counters.keys():
                    # self.counters[p] = other.counters[p]
                    self.set_counter(p, other.counters[p])

            if msg_offset < self.epsilon:
                # self.offsets[other.proc_id] = msg_offset
                self.set_offset(other.proc_id, msg_offset)
            else:
                if other.proc_id in self.offsets:
                    del self.offsets[other.proc_id]

        # if the message is leading
        elif new_epoch == other.epoch:
            # offset of the timestamp of the incoming message
            msg_offset = other.epoch - self.epoch

            # update our counters to the ones in the timestamp of the incoming message
            for p in other.counters.keys():
                # self.counters[p] = other.counters[p]
                self.set_counter(p, other.counters[p])

            for p in self.offsets.keys():
                if self.offsets[p] + msg_offset < self.epsilon:
                    # self.offsets[p] += msg_offset
                    self.set_offset(p, self.offsets[p] + msg_offset)

            for p in other.offsets.keys():
                # self.offsets[p] = other.offsets[p]
                self.set_offset(p, other.offsets[p])

            self.epoch = other.epoch

        else:
            # in all other cases, simply advance the clock
            self.advance()

        # self.offsets[self.proc_id] = 0  # must always remain 0
        self.set_offset(self.proc_id, 0)  # must always remain 0
