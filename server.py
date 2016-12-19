from socket import socket
from threading import Thread


class Server:
    def __init__(self, host, port, timeout=1, window_size=10):
        self.host = host
        self.port = port
        self.socket = socket(host, port)
        self.socket.settimeout(timeout)
        self.window_size = window_size

    def start(self):
        while True:
            msg = None
            # keep receiving and ignore timeout by waiting
            while not msg:
                try:
                    msg = self.socket.recvfrom(1024)
                except:
                    pass

            file_name, addr = msg
            if not file_name:
                break

            reply = 'Received request for "' + file_name + '"'
            self.socket.sendto(reply, addr)

            print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + file_name.strip()
            Thread(target=self.__handle_request, args=[file_name, addr]).start()

    def __handle_request(self):
        pass
