from tkinter import *
from PIL import Image, ImageTk
import os

root = Tk()


def Click():
    image = Image.open(os.getcwd() + "/screenshot.png")
    photo = ImageTk.PhotoImage(image)

    label = Label(root, image=photo)
    label.image = photo  # keep a reference!
    label.pack()


image = Image.open(os.getcwd() + "/screenshot.png")
photo = ImageTk.PhotoImage(image)
label = Label(root, image=photo)

label.image = photo  # keep a reference!
label.pack()

labelframe = LabelFrame(root)
labelframe.pack(fill="both", expand="yes")

left = Label(labelframe)

button = Button(labelframe, padx=5, pady=5, text="Next", command=Click)
button.pack()

R1 = Radiobutton(labelframe, text="Choice 1", value=1)
R1.pack()

R2 = Radiobutton(labelframe, text="Choice 2", value=2)
R2.pack()

left.pack()
root.mainloop()
