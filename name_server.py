import socket


class Name_Server():
    def __init__(self, name):
        self.s = socket.socket()
        self.s.bind(('0.0.0.0', 6668))
        self.s.listen(10)
        self.name = name

    def start(self):
        print('name serv start')
        conn, addr = self.s.accept()
        print(addr)
        while True:
            data = conn.recv(1024).decode('utf8')
            if data == 'name query':
                conn.send('response.{}'.format(self.name).encode('utf8'))
            if data == 'name change':
                conn.send('response_name_change')
                self.name = conn.recv(1024).decode('utf8')
            if data == 'stop':
                break
