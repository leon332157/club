#! /usr/bin/env python3
import tkinter.messagebox as messagebox
from tkinter import *
from tkinter.scrolledtext import *
import time
import rot13
import base64
import json
import progressbar
import requests
import threading
import os
import socket


class Client:

    def __init__(self):
        self.s = socket.socket()
        self.port = int(6666)
        self.rot = rot13.Rot13()
        self.utf8 = 'utf8'
        try:
            os.mkdir('cache')
        except FileExistsError:
            pass
        try:
            os.rmdir('cache/desc_running')
        except FileNotFoundError:
            pass
        try:
            os.rmdir('cache/get_sc')
        except FileNotFoundError:
            pass
        root = Tk()
        self.canvas = Canvas(root)
        self.canvas.pack(side=LEFT)
        scrollbar = Scrollbar(root, command=self.canvas.yview)
        scrollbar.pack(side=LEFT, fill='y')
        self.canvas.bind('<Configure>', self.on_configure)
        root1 = Frame(self.canvas)
        self.canvas.configure(width=550, height=600)
        self.canvas.create_window((0, 0), width=0, window=root1, anchor=NW)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        root.title('Server Login')
        self.l1 = Label(root1, text='Server Login', font=('', 30))
        self.l2 = Label(root1, text='Input server ip here:')
        self.l3 = Label(root1, text='Input server password here:')
        self.l4 = Label(root1, text='Command execute on server')
        self.l5 = Label(root1, text='Execute log', font=('', 25))
        self.l6 = Label(root1)
        self.e1 = Entry(root1)
        self.e2 = Entry(root1, show='*')
        self.e3 = Entry(root1)
        self.b1 = Button(root1, text='connect', command=self.connect)
        self.b2 = Button(root1, text='login', command=self.pass_auth)
        self.b3 = Button(root1, text='exit', command=quit)
        self.b4 = Button(root1, text='Execute', command=self.execute)
        self.b5 = Button(root1, text='Show password', command=self.show_password)
        self.b6 = Button(root1, text='Get Screen', command=self.get_screenshot)
        self.b7 = Button(root1, text='Discover Server', command=self.desc_serv)
        self.b8 = Button(root1, text='Clear log ', command=self.cls)
        self.t1 = ScrolledText(root1, bg='black', fg='white', height=10, width=70, font=('', 11))
        self.listbox = Listbox(root1, bg='black', fg='white', height=7, width=50)
        self.listbox.insert(END, 'Discovered server will show in here')
        self.tk_comp_list = [self.l1, self.listbox, self.b7, self.l2, self.e1, self.b1, self.l3, self.e2, self.b2,
                             self.b5, self.l4, self.e3, self.b4, self.l5, self.t1, self.b8, self.b6, self.l6, self.b3]
        for each in self.tk_comp_list:
            each.pack()
        try:
            self.t1.config(state=DISABLED)
            root.resizable(width=False, height=False)
            root.mainloop()
        except KeyboardInterrupt:
            self.quit_serv()

    def pass_auth(self):
        password = self.e2.get()
        try:
            if password == '':
                messagebox.showinfo('Input password', 'Please input password.')
                return
            self.s.send(bytes(base64.b64encode(bytes(self.rot.encodes(password).encode('utf8')))))
        except Exception as e:
            messagebox.showwarning(title='Error', message=e)
            return
        auth = self.s.recv(1024)
        if auth != b'correct':
            messagebox.showwarning(title='incorrect password', message='Incorrect password!')
            return
        else:
            messagebox.showinfo(title='Successful', message='Successfully login')
            return

    def connect(self):
        ip = self.e1.get()
        if not ip == '':
            pass
        else:
            messagebox.showwarning(title='Invalid input', message='Please input the right ip.')
            return
        try:
            self.s.settimeout(4)
            self.s.connect((str(ip), self.port))
            messagebox.showinfo(title='connected', message='Successfully connected!')
            return self.s
        except Exception as e:
            messagebox.showwarning(title='Error', message=e)
            self.s.close()
            del self.s
            self.__init__()

    def execute(self):
        command = self.e3.get()
        if not command == '':
            pass
        else:
            messagebox.showinfo(title='input command', message='Please input command.')
            return
        try:
            self.s.send(bytes(('Y29tbWFuZA==.' + str(command)).encode('utf8')))
        except Exception as e:
            messagebox.showwarning(title='Error', message=e)
            return
        self.s.settimeout(20)
        raw_output = self.s.recv(65535).decode('utf8')
        if raw_output.startswith('b3V0cHV0Cg=='):
            self.t1.config(state=NORMAL)
            output = '{} command:{}\n{}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), command,
                                                raw_output.split('b3V0cHV0Cg==')[1])
            self.t1.insert(END, output)
            self.t1.config(state=DISABLED)

    def cls(self):
        self.t1.config(state=NORMAL)
        self.t1.delete("1.0", END)
        self.t1.config(state=DISABLED)

    def get_screenshot(self):
        th = threading.Thread(target=self.get_screenshot_helper, daemon=True)
        if not os.path.isdir('cache/get_sc'):
            th.start()
        else:
            messagebox.showwarning('Already Running', 'Already Receiving Screenshot')

    def get_screenshot_helper(self):
        try:
            self.s.send(b'aW1hZ2UgcXVlcnk=')
        except Exception as e:
            messagebox.showwarning(title='Error', message=e)
            return
        os.mkdir('cache/get_sc')
        self.s.settimeout(20)
        self.s.send(b'log check')
        if self.s.recv(1024) == b'not':
            messagebox.showinfo(title='login', message='Please login first')
            return
        if self.s.recv(1024) == b'l1':
            self.s.send(b'l1conf')
        self.s.send(b'start')
        raw_each_len = self.s.recv(9000)
        each_len = json.loads(raw_each_len)
        self.s.send(b'l1sconf')
        self.s.send(b'start')
        raw_list = list()
        with progressbar.ProgressBar(max_value=each_len) as bar:
            for i in range(0, each_len):
                raw_list.append(self.s.recv(400))
                self.s.send(b'conf')
                bar.update(i)
        print('\nrecived segments {}'.format(len(raw_list)))
        pic = b''.join(raw_list)
        f = open(os.getcwd() + '/sav.png', 'w+b')
        f.write(base64.b64decode(pic))
        f.close()
        messagebox.showinfo('saved', 'Saved in {}{}'.format(os.getcwd(), '/sav.png'))
        del bar
        os.rmdir('cache/get_sc')

    def show_password(self):
        if not self.e2.get() == '':
            messagebox.showinfo(title='password', message=self.e2.get())
        else:
            messagebox.showinfo(title='input password', message='Please input password.')

    def quit_serv(self):
        try:
            self.s.send(b'ZXhpdCgp==')
        except socket.error:
            pass
        time.sleep(1)
        self.s.close()
        print('Connection Closed')
        exit()

    def desc_serv(self):
        t = threading.Thread(target=self.desc_serv_helper, daemon=True)
        if not os.path.isdir('cache/desc_running'):
            t.start()
        else:
            messagebox.showwarning('Already Running', 'Already Discovering Server')

    def desc_serv_helper(self):
        os.mkdir('cache/desc_running', )
        serv_list = []
        raw_serv_dict = {}
        s1 = socket.socket()
        try:
            s1.connect(('baidu.com', 80))
            raw_ip = s1.getsockname()[0]
        except socket.error:
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
        self.listbox.delete(0, END)
        if len(serv_list) == 0:
            self.listbox.insert(END, 'No server found.')
            return
        for each in serv_list:
            self.listbox.insert(END, each)
            try:
                os.rmdir('cache/desc_running')
            except FileNotFoundError:
                pass

    def on_configure(self, event):
        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))


if __name__ == '__main__':
    Client()
