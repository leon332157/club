import socket
import tkinter.messagebox as messagebox
from tkinter import *
from functools import partial
from tkinter.scrolledtext import *
import time
import rot13
import base64
import json
import progressbar
import requests
import threading
import os


def init():
    global s
    global rot
    global utf8
    global port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(6666)
    rot = rot13.Rot13()
    utf8 = 'utf8'
    try:
        os.rmdir('cache/desc_running')
    except FileNotFoundError:
        pass


def pass_auth():
    password = e2.get()
    try:
        if password == '':
            messagebox.showinfo('Input password', 'Please input password.')
            return
        s.send(bytes(base64.b64encode(bytes(rot.encodes(password).encode('utf8')))))
    except Exception as e:
        messagebox.showwarning(title='Error', message=e)
        return
    auth = s.recv(1024)
    if auth != b'correct':
        messagebox.showwarning(title='incorrect password', message='Incorrect password!')
        return
    else:
        messagebox.showinfo(title='Successful', message='Successfully login')
        return


def connect():
    global s
    ip = e1.get()
    if not ip == '':
        pass
    else:
        messagebox.showwarning(title='Invalid input', message='Please input the right ip.')
        return
    try:
        s.settimeout(4)
        s.connect((str(ip), port))
        messagebox.showinfo(title='connected', message='Successfully connected!')
        return s
    except Exception as e:
        messagebox.showwarning(title='Error', message=e)
        s.close()
        del s
        init()


def execute():
    command = e3.get()
    if not command == '':
        pass
    else:
        messagebox.showinfo(title='input command', message='Please input command.')
        return
    try:
        s.send(bytes(('Y29tbWFuZA==.' + str(command)).encode('utf8')))
    except Exception as e:
        messagebox.showwarning(title='Error', message=e)
        return
    s.settimeout(20)
    raw_output = s.recv(65535).decode('utf8')
    if raw_output.startswith('b3V0cHV0Cg=='):
        t1.config(state=NORMAL)
        output = '{} command:{}\n{}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), command,
                                            raw_output.split('b3V0cHV0Cg==')[1])
        t1.insert(END, output)
        t1.config(state=DISABLED)


def cls():
    """:TODO:FIX CLEAR"""
    t1.config(state=NORMAL)
    t1.delete("1.0", END)
    t1.config(state=DISABLED)


def get_screenshot():
    try:
        s.send(b'aW1hZ2UgcXVlcnk=')
    except Exception as e:
        messagebox.showwarning(title='Error', message=e)
        return
    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
    s.settimeout(20)
    s.send(b'log check')
    if s.recv(1024) == b'not':
        messagebox.showinfo(title='login', message='Please login first')
        return
    if s.recv(1024) == b'l1':
        s.send(b'l1conf')
    time.sleep(1)
    raw_each_len = s.recv(65535)
    each_len = json.loads(raw_each_len)
    s.send(b'l1sconf')
    s.send(b'start')
    raw_list = list()
    for each in bar(each_len):
        raw_list.append(s.recv(each + 100))
        s.send(b'conf')
    print('\nrecived segments {}'.format(len(raw_list)))
    pic = b''.join(raw_list)
    f = open(os.getcwd() + '/sav.png', 'w+b')
    f.write(base64.b64decode(pic))
    f.close()
    messagebox.showinfo('saved', 'Saved in {}{}'.format(os.getcwd(), '/sav.png'))
    del bar


def show_password():
    if not e2.get() == '':
        messagebox.showinfo(title='password', message=e2.get())
    else:
        messagebox.showinfo(title='input password', message='Please input password.')


def quit_serv():
    try:
        s.send(b'ZXhpdCgp==')
    except Exception:
        pass
    time.sleep(1)
    s.close()
    print('Connection Closed')
    exit()


def desc_serv():
    t = threading.Thread(target=desc_serv_helper, daemon=True)
    if not os.path.isdir('cache/desc_running'):
        t.start()
    else:
        messagebox.showwarning('Already Running', 'Already Discovering Server')


def desc_serv_helper():
    os.mkdir('cache/desc_running', )
    serv_list = []
    raw_serv_dict = {}
    s1 = socket.socket()
    try:
        s1.connect(('baidu.com', 80))
        raw_ip = s1.getsockname()[0]
    except Exception:
        raw_ip = socket.gethostbyname(socket.gethostname())[0]
    s1.close()
    ip_list = raw_ip.split('.')
    ip_1 = int(ip_list[0])
    ip_2 = int(ip_list[1])
    ip_3 = int(ip_list[2])
    s1 = socket.socket()
    s1.settimeout(0.5)
    with progressbar.ProgressBar(max_value=255) as Bar:
        for i in range(0, 255):
            # if i == 1:
            #    ip = '127.0.0.1'
            # else:
            ip = '%d.%d.%d.%d' % (ip_1, ip_2, ip_3, i)
            # print(ip)
            try:
                name = requests.get('http://{}:5000'.format(ip), timeout=0.1)
                if name.status_code == 200:
                    raw_serv_dict[name.text] = ip
                del name
            except requests.exceptions.RequestException:
                pass
            Bar.update(i)
            del ip
        x = 0
        for k, v in raw_serv_dict.items():
            x += 1
            serv_list.append('{}) {} {}'.format(x, k, v))
    listbox.delete(0, END)
    if len(serv_list) == 0:
        listbox.insert(END, 'No server found.')
        return
    for each in serv_list:
        listbox.insert(END, each)
        try:
            os.rmdir('cache/desc_running')
        except FileNotFoundError:
            pass


def on_configure(event):
    # update scrollregion after starting 'mainloop'
    # when all widgets are in canvas
    canvas.configure(scrollregion=canvas.bbox('all'))


init()
root = Tk()
canvas = Canvas(root)
canvas.pack(side=LEFT)
scrollbar = Scrollbar(root, command=canvas.yview)
scrollbar.pack(side=LEFT, fill='y')
canvas.bind('<Configure>', on_configure)
root1 = Frame(canvas)
canvas.configure(width=550, height=600)
canvas.create_window((0, 0), width=0, window=root1, anchor=NW)
canvas.configure(yscrollcommand=scrollbar.set)
root.title('Server Login')
l1 = Label(root1, text='Server Login', font=('', 30))
l2 = Label(root1, text='Input server ip here:')
l3 = Label(root1, text='Input server password here:')
l4 = Label(root1, text='Command execute on server')
l5 = Label(root1, text='Execute log', font=('', 25))
l6 = Label(root1)
e1 = Entry(root1)
e2 = Entry(root1, show='*')
e3 = Entry(root1)
b1 = Button(root1, text='connect', command=connect)
b2 = Button(root1, text='login', command=partial(pass_auth))
b3 = Button(root1, text='exit', command=quit)
b4 = Button(root1, text='Execute', command=execute)
b5 = Button(root1, text='Show password', command=show_password)
b6 = Button(root1, text='Get Screen', command=get_screenshot)
b7 = Button(root1, text='Discover Server', command=desc_serv)
b8 = Button(root1, text='Clear log ', command=cls)
t1 = ScrolledText(root1, bg='black', fg='white', height=10, width=70, font=('', 11))
listbox = Listbox(root1, bg='black', fg='white', height=7, width=50)
listbox.insert(END, 'Discovered server will show in here')
l1.pack()
listbox.pack()
b7.pack()
l2.pack()
e1.pack()
b1.pack()
l3.pack()
e2.pack()
b2.pack()
b5.pack()
l4.pack()
e3.pack()
b4.pack()
l5.pack()
t1.pack()
b8.pack()
b6.pack()
l6.pack()
b3.pack()
try:
    t1.config(state=DISABLED)
    root.resizable(width=False, height=False)
    root.mainloop()
except KeyboardInterrupt:
    quit_serv()
