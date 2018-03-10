from tkinter import *
import tkinter.messagebox as messagebox
from rot13 import Rot13
import os
import base64

rot = Rot13()


def change_password():
    new = e1.get()
    if new == '':
        messagebox.showerror('Please input password.', 'Please input password.')
        return
    try:
        with open(os.getcwd() + '/password.pc', mode='w+') as f:
            f.write(base64.b64encode(bytes(rot.encodes(new).encode('utf8'))).decode('utf8'))
            f.close()
        messagebox.showinfo(title='Successful', message='Successfully saved password, your password is: ' + new)
    except Exception as e:
        messagebox.showerror(title='Error', message=e)
    return


root = Tk()
l1 = Label(root, text='Change Password Tool', font=('', 28))
l2 = Label(root, text='New password:')
e1 = Entry(root, show='*')
b1 = Button(root, text='Change password', command=change_password)
b2 = Button(root, text='exit', command=exit)
l1.pack()
l2.pack()
e1.pack()
b1.pack()
b2.pack()
try:
    root.title('Change Password Tool')
    root.resizable(width=False, height=False)
    root.mainloop()
except KeyboardInterrupt:
    exit(0)
