import socket
import subprocess
from rot13 import Rot13
import base64
import os
import pyscreenshot
from PIL import Image
import time

rot = Rot13()
global password
try:
    with open(os.getcwd() + '/password.pc', 'r+') as f:
        raw_password = f.read().encode('utf8')
        password = rot.decodes(base64.b64decode(raw_password).decode('utf8'))
except Exception as e:
    print(e)
    print("Please set password use 'change password.py'")
    exit(1)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # initiallize socket
s.bind(('127.0.0.1', 6666))
s.listen(100)
img_serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # initiallize socket
img_serv.bind(('127.0.0.1', 6667))
print('\nServer listening on {0}:{1} and {0}:{2}'.format('127.0.0.1', 6666, 6667))
try:
    conn, addr = s.accept()
except KeyboardInterrupt:
    s.close()
    print('Connection Closed')
    exit(0)
print('connection from: ' + str(addr))


def main():
    try:
        data = conn.recv(1024).decode('utf8')
        if data == 'ZXhpdCgp==':
            s.close()
            print('Connection Closed')
            exit()
        if data == 'Y29tbWFuZA==':
            if not log:
                conn.send(bytes(('b3V0cHV0Cg==' + 'You are not logged in, please login first.').encode('utf8')))
                print('Not logged in')
                return False
            raw_command = str(data).split('Y29tbWFuZA==')[1]
            command = raw_command.split(' ')
            print('executing: ' + raw_command)
            try:
                output = str(subprocess.check_output(command, stderr=subprocess.STDOUT))
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                output = str(e)
            conn.send(bytes(('b3V0cHV0Cg==' + output).encode('utf8')))
            return True
        if rot.decodes(base64.b64decode(data).decode('utf8')) == password:
            conn.send(bytes('correct'.encode('utf8')))
            print('correct password')
            return True
        if data == 'aW1hZ2UgcXVlcnk=':
            while True:
                time.sleep(0.25)
                pyscreenshot.grab_to_file(os.getcwd() + '/screenshot.png')
                raw_image = Image.open(os.getcwd() + '/screenshot.png')
                w, h = raw_image.size
                proc_img = raw_image.resize((int(w / 4), int(h / 4)))
                proc_img.save(os.getcwd() + '/screenshot.png')
                with open(os.getcwd() + '/screenshot.png', mode='rb') as bytes_img_file:
                    bytes_img = bytes_img_file.read()
                    conn.send(base64.b64encode(bytes_img))
                    print('Sent')
        else:
            conn.send(bytes('incorrect'.encode('utf8')))
            print('incorrect password')
            return False
    except KeyboardInterrupt:
        s.close()
        print('Connection Closed')
        exit()


log = False
while True:
    # try:
    log = main()  # Continuously get return value True or False to verify login.
    continue
# except Exception as e:
# print(e)
#   s.close()
#   print('Connection Closed')
#   exit(0)
