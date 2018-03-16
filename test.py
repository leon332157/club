# !/usr/bin/python

from tkinter import tix
from tkinter import *

app = tix.Tk()
app.title('exploring tix')

# scr_win = tix.ScrolledWindow(app, width=200, height=300,scrollbar='y')
scr_win = tix.ScrolledWindow(app, width=500, height=600)
scr_win.pack(fill='both', expand=1)

sframe = scr_win.window
# sframe.config(bg='brown')
s1 = '''Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
Welcome to tkinter.tix, tkinter on steroids!
'''
s2 = '... Now included with Python31 ...'
# for x in range(20):
# tix.Label(sframe, text=s1, bg='yellow').pack()
# tix.Label(sframe, text=s2, bg='white', fg='red').pack()

tix.Label(sframe, text=s1, bg='yellow').pack()
tix.Label(sframe, text=s2, bg='white', fg='red').pack()

Checkbutton(sframe, text='I have HotFix/OINT rollback labels').pack()
Button(sframe, text='Exit').pack(side=LEFT)
Button(sframe, text='Next', width=20).pack(side=RIGHT)

app.mainloop()
