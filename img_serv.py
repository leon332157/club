import socket, base64, os, pyscreenshot, time, sys
from PIL import Image


class Server():
    def __init__(self):
        self.port = 6666
        self.address = '127.0.0.1'
        self.s1 = socket.socket()
        self.s1.bind((self.address, self.port))

    def main(self):
        self.s1.listen(10)
        conn, addr = self.s1.accept()
        print(addr)
        while True:
            time.sleep(0.25)
            pyscreenshot.grab_to_file(os.getcwd() + '/screenshot.png')
            raw_image = Image.open(os.getcwd() + '/screenshot.png')
            w, h = raw_image.size
            proc_img = raw_image.resize((int(w / 2), int(h / 2)))
            proc_img.save(os.getcwd() + '/screenshot.png')
            with open(os.getcwd() + '/screenshot.png', mode='rb') as f:
                bytes_img = f.read()
                if conn.recv(1024) == b'get_size':
                    conn.send(bytes(sys.getsizeof(bytes_img)))
                    print('sent size')
                    time.sleep(2)
                else:
                    conn.send(bytes_img)
                print('Sent')
