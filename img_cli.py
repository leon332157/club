import socket, base64, os


class Cilent():
    def __init__(self):
        self.server = socket.socket()
        self.server.bind(('127.0.0.1', 6668))
        self.server.listen(10)

    def __str__(self):
        return 'Image cilent'

    def __repr__(self):
        return self.__str__()

    def connect(self, ipaddr='127.0.0.1', port=6666):
        self.s1 = socket.socket()
        try:
            self.s1.connect((ipaddr, port))
            return [True]
        except Exception as e:
            return [False, e]

    def get(self):

        self.s1.send(b'get_size')
        self.pic_size = self.s1.recv(1024)
        self.s1.send(b'get_one')
        self.raw_cont = self.s1.recv(int(self.pic_size) + 10)
        self.cont = self.raw_cont.decode('utf8')
        self.s1.send(b'conf')
        with open(os.getcwd() + 'save.png', 'wb') as f:
            f.write(self.cont)
            f.close()
            print('saved')


s = Cilent()
print(s.connect())
s.get()
