import pickle as pickle
import socket
import subprocess
from rot13 import Rot13
import base64
import os
import pyscreenshot
import threading
rot = Rot13()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # initiallize socket
s.bind(('127.0.0.1', 6666))
s.listen(100)
print('Server listening on {}:{}'.format('127.0.0.1', 6666))
try:
    conn, addr = s.accept()
except KeyboardInterrupt:
    s.close()
    print('Connection Closed')
    exit(0)
print('connection from: ' + str(addr))

global password
try:
    with open(os.getcwd() + '/password.pc', 'r+') as f:
        raw_password = f.read()
        password = rot.decodes(pickle.loads(base64.b64decode(raw_password)))
except Exception as e:
    print(e)
    print("Please set password use 'change password.py'")
    exit(1)


def main():
    try:
        data = conn.recv(1024).decode('utf8')
        if str(data).startswith('ZXhpdCgp=='):
            s.close()
            print('Connection Closed')
            exit()
        if str(data).startswith('Y29tbWFuZA=='):
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
        if rot.decodes(pickle.loads(base64.b64decode(data))) == password:
            conn.send(bytes('correct'.encode('utf8')))
            print('correct password')
            return True
        if data == b'aW1hZ2UgcXVlcnk=':
            img = pyscreenshot.grab()
            img.save(os.getcwd() + '/scessnshot.png')
            del img
            img = open(os.getcwd() + '/screenshot.png')
            raw_img = base64.encode(img)
            conn.send(raw_img)
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
