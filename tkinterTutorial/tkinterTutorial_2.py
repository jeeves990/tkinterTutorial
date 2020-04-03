#!/usr/bin/env python3

"""
    ZetCode Tkinter e-book
    In this script , we lay out images
    using absolute positioning.
    Author: Jan Bodnar
    Last modified: December 2015
    Website: www.zetcode.com
"""
from __future__ import print_function
##from Pillow import PIL.Image, PIL.ImageTk

from PIL import Image , ImageTk
from tkinter import Tk, BOTH, Canvas
from tkinter.ttk import Frame , Label , Style, Entry, Button
from PyUtilities import setColRowWeight


class Example(Frame):
    def __init__(self , parent):
        Frame.__init__(self , parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Absolute positioning")
        self.pack(fill=BOTH , expand=True)
        style = Style()
        style.configure("TFrame", background="#333")
        size = 128,128
        '''
        bard = Image.open("bardejov.jpg")
        bardThumbNail = bard.thumbnail(size, Image.BICUBIC)
        bardejov = ImageTk.PhotoImage(bard)

        label1 = Label(self , image=bardejov)
        label1.image = bardejov
        label1.place(x=20, y=20)
        '''
        rot = Image.open("rotunda.jpg")
        rotunda = ImageTk.PhotoImage(rot)
        rot.thumbnail(size, Image.BICUBIC)
        label2 = Label(self , image=rotunda)
        label2.image = rotunda
        label2.place(x=40, y=160)
        
        minc = Image.open("mincol.jpg")
        mincol = ImageTk.PhotoImage(minc)
        minc.thumbnail(size, Image.BICUBIC)
        label3 = Label(self , image=mincol)
        label3.image = mincol
        label3.place(x=170, y=50)

class Calculator(Canvas):
    def __init__(self , parent):
        Canvas.__init__(self , parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Calculator")
        
        Style(). configure("TButton", padding=(0, 5, 0, 5),
        font='serif 10')

        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)
        self.columnconfigure(2, pad=3)
        self.columnconfigure(3, pad=3)
        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)
        entry = Entry(self)
        entry.grid(row=0, column=0, columnspan=4, sticky= 'ew')
        cls = Button(self , text="Cls")
        cls.grid(row=1, column=0)
        bck = Button(self , text="Back")
        bck.grid(row=1, column=1)
        lbl = Button(self)
        lbl.grid(row=1, column=2)
        clo = Button(self , text="Close")
        clo.grid(row=1, column=3)
        sev = Button(self , text="7")
        sev.grid(row=2, column=0)
        eig = Button(self , text="8")
        eig.grid(row=2, column=1)
        nin = Button(self , text="9")
        nin.grid(row=2, column=2)
        div = Button(self , text="/")
        div.grid(row=2, column=3)
        fou = Button(self , text="4")
        fou.grid(row=3, column=0)
        fiv = Button(self , text="5")
        fiv.grid(row=3, column=1)
        six = Button(self , text="6")
        six.grid(row=3, column=2)
        mul = Button(self , text="*")
        mul.grid(row=3, column=3)
        one = Button(self , text="1")
        one.grid(row=4, column=0)
        two = Button(self , text="2")
        two.grid(row=4, column=1)
        thr = Button(self , text="3")
        thr.grid(row=4, column=2)
        mns = Button(self , text="-")
        mns.grid(row=4, column=3)
        zer = Button(self , text="0")
        zer.grid(row=5, column=0)
        dot = Button(self , text=".")
        dot.grid(row=5, column=1)
        equ = Button(self , text="=")
        equ.grid(row=5, column=2)
        pls = Button(self , text="+")
        pls.grid(row=5, column=3)
        ##self.grid(row = 0, column = 0)
        self.pack()


def main():
    win = Tk()
    win.resizable(width = None, height = None)
    x = win.winfo_screenwidth() /2
    y = win.winfo_screenheight() /2
    win.geometry("+%d+%d" % (x, y))
    ##app = Example(win)
    app = Calculator(win)
    win.wm_attributes("-topmost", 1)
    
    win.mainloop()

if __name__ == '__main__':
    main()
