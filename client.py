from socket import socket, AF_INET, SOCK_DGRAM
from sys import exit


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        try:
            self.socket = socket(AF_INET, SOCK_DGRAM)
        except socket.error:
            print 'ERR: Failed to create socket for client.'
            exit()
