from sys import getsizeof
from pickle import dumps,loads


class Packet:
    def __init__(self, length, seq_no, data):
        self.length = length
        self.seq_no = seq_no
        self.data = data

    def to_data_string(self):
        return dumps(self, -1)

    @staticmethod
    def from_file(f, seq_no):
        data = f.readline(512)
        if len(data) > 0:
            size = getsizeof(data) + getsizeof(seq_no)
            packet = Packet(size, seq_no, data)
            return packet
        else:
            return None

    @staticmethod
    def from_string(data_string):
        return loads(data_string)