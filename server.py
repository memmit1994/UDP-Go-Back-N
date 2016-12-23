from socket import socket, AF_INET, SOCK_DGRAM,error as socket_error
from threading import Thread
from random import randrange
from packet import Packet
from time import time
from ack import Ack


class Server:
    def __init__(self, host, port, window_size=10, timeout=1):
        self.host = host
        # try to create socket
        try:
            self.socket = socket(AF_INET, SOCK_DGRAM)
            self.socket.bind((host, port))
        except socket_error:
            print 'ERROR: Failed to create socket for server.'
            exit()
        # holds the number of packets to be resent after timeout
        self.window_size = window_size
        # this field holds the first packet's sequence number that hasn't been ACKed
        self.base = 1
        # holds the sequence number of the next packet
        self.next_seq_num = 1
        # will hold the starting time for the timer when server starts sending packets
        self.start_time = None
        self.timeout = timeout
        self.window = {}

    def start(self):

        while True:
            # receive file request
            msg = self.socket.recvfrom(1024)
            file_name, client_addr = msg

            # in case of corrupt request
            if not file_name:
                break

            reply = 'Received request for "' + file_name + '"'
            self.socket.sendto(reply, client_addr)

            print 'Request for "' + file_name.strip() + '" from [' + client_addr[0], ':', str(client_addr[1]) + ']'

            # create thread to handle request in
            Thread(target=self.__handle_request, args=[file_name, client_addr]).start()

    def __handle_request(self, file_name, client_addr):

        # generate another socket with another port number to handle request in
        sender = Server(self.host, randrange(5000, 9000), self.window_size, self.timeout)

        try:
            # open a file stream for the requested file
            f = open(file_name, 'r')
        except IOError:
            sender.socket.sendto('File not found.', client_addr)
            return

        # start timer
        sender.start_time = time()

        # set timeout for ACKs
        sender.socket.settimeout(0.001)

        while True:

            if sender.next_seq_num < sender.base + sender.window_size:

                packet = Packet.from_file(f, sender.next_seq_num)
                LOST = randrange(0, 100) < 50

                # check if all packets are sent
                if packet is None and sender.base + 1 == sender.next_seq_num:
                    print len(sender.window)
                    sender.socket.sendto('END', client_addr)
                    break

                elif packet is not None:
                    data = packet.to_data_string()
                    sender.window[sender.next_seq_num] = data
                    if not LOST:
                        sender.socket.sendto(data, client_addr)
                    else:
                        # uncomment this line to trace which packets were lost
                        # print 'Packet #', packet.seq_no, ' was lost.'
                        pass
                    sender.next_seq_num += 1

            try:
                # check for ACKs
                ack_string, addr = sender.socket.recvfrom(1024)
                ack = Ack.load_from_data_string(ack_string)

                if ack and ack.seq_no == sender.base:
                    # delete packet from window that was received by client
                    del sender.window[sender.base]
                    # increment base to allow for new packets to be sent in the next iteration
                    sender.base = ack.seq_no + 1
                    continue
            except:
                pass

            # check for timeout
            if time() - sender.start_time > sender.timeout:
                # resend lastly sent packets
                for i in range(sender.base, sender.next_seq_num):
                    sender.socket.sendto(sender.window[i], client_addr)
                # restart timer
                sender.start_time = time()


