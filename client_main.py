from client import Client

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 4444

client = Client('127.0.0.1', 8787)
client.get_file('image.png', (SERVER_HOST, SERVER_PORT))
client.socket.close()



