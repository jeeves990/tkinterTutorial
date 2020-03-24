
# -*- coding: utf -8 -*-
"""
ZetCode Tkinter e-book
This script creates a simple animation.
Author: Jan Bodnar
Last modified: November 2015
Website: www.zetcode.com
"""
from PIL import Image , ImageTk
from tkinter import Tk, BOTH , CENTER
from tkinter.ttk import Frame , Label

DELAY = 850

class Example(Frame):
    def __init__(self , parent):
        Frame.__init__(self , parent , name="frame")
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Animation")
        self.pack(fill=BOTH , expand=True)
        self.i = 0
        self.img_names = ("one.png", "two.png", "three.png",
                            "four.png", "five.png", "six.png", "seven.png",
                            "eight.png", "nine.png")
        img = Image.open(self.img_names[self.i])
        num = ImageTk.PhotoImage(img)
        self.label = Label(self , image=num)
        self.label.pack(pady=30)
        # reference must be stored
        self.label.image = num
        self.after(DELAY , self.doCycle)


    def doCycle(self):
        self.i += 1
        if (self.i >= 9):
            return
        img = ImageTk.PhotoImage(Image.open(self.img_names[self.i]))
        self.label.configure(image=img)
        self.label.image = img
        self.after(DELAY , self.doCycle)


def main():
    root = Tk()
    root.geometry("300x200 +300+300")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()