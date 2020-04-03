# -*- coding: utf -8 -*-
"""
    ZetCode Tkinter e-book
    In this script , the text entered
    in the Entry widget is shown in
    the Label.
    Author: Jan Bodnar
    Last modified: November 2015
    Website: www.zetcode.com
"""

import tkinter as tk
from tkinter import Tk, BOTH , W, END , NORMAL , DISABLED , BooleanVar
from tkinter.ttk import Entry , Frame , Button , Checkbutton


class Example(Frame):
    def __init__(self , parent):
        Frame.__init__(self , parent)
        self.parent = parent
        self['relief'] = 'groove'
        self.initUI()
        self.bldRBtnFrame()

    def initUI(self):
        self.parent.title("Entry")
        self.pack(anchor = 'nw', fill = BOTH, expand=True)

        self.entryvar = tk.StringVar()
        self.entry = Entry(self)
        self.entry['textvariable'] = self.entryvar
        self.entry.grid(row=0, column=0, columnspan=2, padx=10, pady=15, sticky=W)

        clearBtn = Button(self , text="Clear", command=self.onClear)
        clearBtn.grid(row=1, column=0, pady=15, padx=10, sticky=W)

        selBtn = Button(self , text="Select all",  command=self.onSelectAll)
        selBtn.grid(row=1, column=1, sticky=W)

        deselBtn = Button(self , text="Deselect", command=self.onDeselect)
        deselBtn.grid(row=1, column=2, padx=10)

        self.chvar = BooleanVar()
        self.chvar.set(False)
        checkBtn = Checkbutton(self , text="readonly", variable=self.chvar, command=self.onChangeReadability)
        checkBtn.grid(row=2, column=0)



    def bldRBtnFrame(self):
        self.btnframe = Frame(self)
        self.btnframe.grid(row = 1, column = 5)
        self.btnframe['relief'] = 'sunken'

        self.rbvar = tk.IntVar()
        rb1 = tk.Radiobutton(self.btnframe, text = 'RB 1', variable = self.rbvar, value = 1, command = self.rbSelect)
        rb2 = tk.Radiobutton(self.btnframe, text = 'RB 2', variable = self.rbvar, value = 2, command = self.rbSelect)
        rb3 = tk.Radiobutton(self.btnframe, text = 'RB 3', variable = self.rbvar, value = 3, command = self.rbSelect)
        rb4 = tk.Radiobutton(self.btnframe, text = 'RB 4', variable = self.rbvar, value = 4, command = self.rbSelect)
        rb1.grid(row = 0, column = 0, padx = 10)
        rb2.grid(row = 1, column = 0, padx = 10)
        rb3.grid(row = 2, column = 0, padx = 10)
        rb4.grid(row = 3, column = 0, padx = 10)
        
    def rbSelect(self):
        sel = self.rbvar.get()
        if sel == 1:
            txt ='rb 1'
        elif sel == 2:
            txt = 'rb 2'
        elif sel == 3:
            txt = 'rb 3'
        elif sel == 4:
            txt ='rb 4'
        else:
            txt = 'tilt'
            return
        print(txt)
        txt = 'RadioButton {0} has been pushed'.format(txt)
        print(txt)
        self.entryvar = txt
        


    def onClear(self):
        self.entry.delete(0, END)


    def onSelectAll(self):
        self.entry.select_range(0, END)


    def onDeselect(self):
        self.entry.select_clear()


    def onChangeReadability(self):
        if self.chvar.get() == True:
            self.entry.config(state=DISABLED)
        else:
            self.entry.config(state=NORMAL)


def main():
    root = Tk()
    ex = Example(root)
    root.geometry("+300+300")
    root.mainloop()
if __name__ == '__main__':
    main()
