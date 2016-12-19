

class Packet:
    def __init__(self, length, seq_no, data):
        self.length = length
        self.seqNo = seq_no
        self.data = data
