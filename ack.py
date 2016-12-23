from sys import getsizeof
from pickle import loads, dumps


class Ack:
    def __init__(self, seq_no):
        self.seq_no = seq_no
        self.length = getsizeof(self)

    def to_data_string(self):
        return dumps(self)

    @staticmethod
    def load_from_data_string(data_sring):
        return loads(data_sring)
