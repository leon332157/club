from tkinter import filedialog
from tkinter import *
import os

root = Tk()
filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file")
print(filename)
# open
