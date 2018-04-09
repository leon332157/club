import subprocess
import socket
import base64
import os
import textwrap
import pyscreenshot
import time
import json
from rot13 import Rot13
from PIL import Image
import multiprocessing as mp
import name_server
import progressbar

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
name = input('Set name for server:')
if not name:
    name = 'Test'
print('name: {}'.format(name))
NameServer = name_server.NameServer(name)
mp.Process(target=NameServer.start).start()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # initiallize socket
s.bind(('0.0.0.0', 6666))
s.listen(100)
print('\nServer listening on {0}:{1} and {0}:{2}'.format('0.0.0.0', 6666, 5000))
try:
    conn, addr = s.accept()
except KeyboardInterrupt:
    s.close()
    print('Connection Closed')
    exit(0)
print('connection from: {}'.format(addr))


def main():
    try:
        data = str(conn.recv(1024).decode('utf8'))
        if data == 'ZXhpdCgp==':
            s.close()
            print('Connection Closed')
            exit()
        if data.startswith('Y29tbWFuZA=='):
            if not log:
                conn.send(('b3V0cHV0Cg==' + 'You are not logged in, please login first.').encode('utf8'))
                print('Not logged in')
                return False
            raw_command = data.split('Y29tbWFuZA==.')[1]
            command = raw_command.split(' ')
            print('executing: ' + raw_command)
            try:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output = process.stdout.read()
                if output == b'':
                    output = process.stderr.read()
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                output = str(e).encode('utf8')
            conn.send((b'b3V0cHV0Cg==' + output))
            return True
        if rot.decodes(base64.b64decode(data).decode('utf8')) == password:
            conn.send(bytes('correct'.encode('utf8')))
            print('correct password')
            return True
        if data == 'aW1hZ2UgcXVlcnk=':
            if conn.recv(1024) == b'log check':
                if not log:
                    conn.send(b'not')
                    print('Not logged in')
                    return False
                else:
                    conn.send(b'pass')
            bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
            pyscreenshot.grab_to_file(os.getcwd() + '/screenshot.png')
            raw_image = Image.open(os.getcwd() + '/screenshot.png')
            w, h = raw_image.size
            proc_img = raw_image.resize((int(w / 1), int(h / 1)))
            proc_img.save(os.getcwd() + '/screenshot.png')
            with open(os.getcwd() + '/screenshot.png', mode='rb') as bytes_img_file:
                img = base64.b64encode(bytes_img_file.read())
                base64_list = textwrap.wrap(img.decode('utf8'), 300)
                each_len = []
                for each in base64_list:
                    each_len.append(len(each))
                print('data ready')
            conn.send(b'l1')
            print('sent hello')
            while not conn.recv(1024) == b'l1conf':
                time.sleep(0.1)
            print('recvd hello')
            while not conn.recv(1024) == b'start':
                time.sleep(0.5)
            conn.send(json.dumps(len(each_len)).encode('utf8'))
            while not conn.recv(1024) == b'l1sconf':
                time.sleep(0.1)
            print('client size confirmed')
            while not conn.recv(1024) == b'start':
                time.sleep(0.1)
            print('Start sending')
            for each in bar(base64_list):
                conn.send(each.encode('utf8'))
                if not conn.recv(1024) == b'conf':
                    time.sleep(0.1)
            print('\nsent segments: {}'.format(len(base64_list)))
            return True
        else:
            conn.send('incorrect'.encode('utf8'))
            print('incorrect password')
            return False
    except (KeyboardInterrupt, ConnectionResetError):
        s.close()
        print('Connection Closed')
        exit()


log = False
while True:
    log = main()  # Continuously get return value True or False to verify login.
    continue
