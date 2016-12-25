from socket import socket, AF_INET, SOCK_DGRAM, error as socket_error
from sys import exit
from packet import Packet
from ack import Ack
from time import time
from random import random


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        try:
            self.socket = socket(AF_INET, SOCK_DGRAM)
            self.socket.bind((host, port))
        except socket_error:
            print 'ERROR: Failed to create socket for client.'
            exit()
        self.expected_seq_no = 1

    def get_file(self, file_name, server_addr):
        try:
            # send request for file
            self.socket.sendto(file_name, server_addr)

            addr = None
            while not addr:
                # receive server's reply
                reply, addr = self.socket.recvfrom(1024)

                # check if it's really the server that's sending the message
                if addr != server_addr:
                    addr = None
                    continue

                print 'Server reply : ' + reply

                self.receive_file()

        except socket_error, msg:
            print 'Error Code : ' + str(msg[0]) + '\nMessage :  ' + msg[1]
            exit()

    def receive_file(self):
        received_file = open("response.png", "w+")
        start_time = time()
        count = -1
        while True:
            count += 1
            data_string, addr = self.socket.recvfrom(1024)

            if data_string != 'END' and data_string != 'File not found.':
                packet = Packet.from_string(data_string)

                if packet.seq_no <= self.expected_seq_no:
                    ack = Ack(packet.seq_no)
                    LOST = random() < 0.05
                    if not LOST:
                        self.socket.sendto(ack.to_data_string(), addr)
                    else:
                        # uncomment this line to trace which packets were lost
                        print 'Ack #', packet.seq_no, ' was lost.'
                    if packet.seq_no == self.expected_seq_no:
                        self.expected_seq_no += 1
                        received_file.write(packet.data)
            else:
                print 'Request ended in ' + str(time() - start_time)
                received_file.close()
                break
