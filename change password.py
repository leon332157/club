import pickle
from Tkinter import *
import tkMessageBox as Messagebox
from rot13 import Rot13
import os
import base64

rot = Rot13()


def change_password():
    new = e1.get()
    try:
        f = open(os.getcwd() + 'password.pc', mode='w+')
        obj = pickle.dumps(rot.encodes(new))
        encode = base64.b64encode(obj)
        f.write(encode)
        f.close()
        Messagebox.showinfo(title='Successful', message='Successfully saved password, your password is: ' + new)
    except Exception as e:
            Messagebox.showerror(title='Error', message=e)
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
