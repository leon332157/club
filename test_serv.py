import socket


class Server():
    def __init__(self):
        self.port = 6667
        self.address = '127.0.0.1'
        self.s1 = socket.socket()
        self.s1.bind((self.address, self.port))
        self.s1.listen(10)

    def start(self):
        print('start')
        while True:
            conn, addr = self.s1.accept()
            if conn.recv(1024) == b'stop':
                break
        self.s1.close()
