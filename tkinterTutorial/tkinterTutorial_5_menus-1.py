


# -*- coding: utf -8 -*-
"""
            ZetCode Tkinter e-book
            In this script , we dynamically add and remove Listbox
            items.
            Author: Jan Bodnar
            Last modified: November 2015
            Website: www.zetcode.com
"""


import tkinter as tk
from tkinter import Tk, BOTH , Listbox , BooleanVar , END , E, W, S, N
from tkinter.ttk import Frame , Button , Entry


class Example(Frame):
    def __init__(self , parent):
        Frame.__init__(self , parent)
        self.parent = parent
        self.initUI()
    
        
    def initUI(self):
        self.parent.title("Adding , removing items")
        self.pack(fill=BOTH , expand=True)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.entry = Entry(self)
        self.entry.grid(row=0, column=0, padx=10)
        addBtn = Button(self , text="Add", command=self.addItem)
        addBtn.grid(row=0, column=1, pady=10)
        self.lbox = Listbox(self)
        self.lbox.grid(row=1, column=0, rowspan=2, columnspan=3,
        padx=10, sticky=E+W+N+S)
        remBtn = Button(self , text="Remove", command=self.removeItem)
        remBtn.grid(row=3, column=0, padx=10, pady=10, sticky=W)
   
   
    def addItem(self):
        val = self.entry.get()
        if (len(val.strip()) == 0):   return

        self.entry.delete(0, END)
        self.lbox.insert(END , val)


    def removeItem(self):
        idx = self.lbox.curselection()
        if (len(idx) == 0):      return
        self.lbox.delete(idx , idx)


def main():
    root = Tk()
    ex = Example(root)
    root.geometry("+300+300")
    root.mainloop()


if __name__ == '__main__':
    main()


