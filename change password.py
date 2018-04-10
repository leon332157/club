#! /usr/bin/env python3
from tkinter import *
import tkinter.messagebox as messagebox
from rot13 import Rot13
import os
import base64


class ChangePasswordTool:
    def __init__(self):

        self.rot = Rot13()
        root = Tk()
        self.l1 = Label(root, text='Change Password Tool', font=('', 28))
        self.l2 = Label(root, text='New password:')
        self.e1 = Entry(root, show='*')
        self.b1 = Button(root, text='Change password', command=self.change_password)
        self.b2 = Button(root, text='exit', command=exit)
        self.l1.pack()
        self.l2.pack()
        self.e1.pack()
        self.b1.pack()
        self.b2.pack()
        try:
            root.title('Change Password Tool')
            root.resizable(width=False, height=False)
            root.mainloop()
        except KeyboardInterrupt:
            exit(0)

    def change_password(self):
        new = self.e1.get()
        if new == '':
            messagebox.showerror('Please input password.', 'Please input password.')
            return
        try:
            with open(os.getcwd() + '/password.pc', mode='w+') as f:
                f.write(base64.b64encode(bytes(self.rot.encodes(new).encode('utf8'))).decode('utf8'))
                f.close()
            messagebox.showinfo(title='Successful', message='Successfully saved password, your password is: ' + new)
        except Exception as e:
            messagebox.showerror(title='Error', message=e)
        return


if __name__ == '__main__':
    ChangePasswordTool()
