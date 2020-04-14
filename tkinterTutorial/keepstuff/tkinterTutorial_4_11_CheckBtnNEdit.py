
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
from GlobalErrorHandling import GlobalErrorHandler as GERR
import clipboard


NOWISTIME = "now is the time for all good men to come to the aid of their party"

class Example(Frame):
    def __init__(self , parent, **kwargs):
        GERR(self).__init__(parent, **kwargs)
        ##GERR(self).__init__(self, parent)  ''' this doesn't work '''
        Frame.__init__(self , parent)
        self.parent = parent
        self.initUI()
        self.entry.insert(0, NOWISTIME)


    def initUI(self):
        self.parent.title("Entry")
        self.pack(fill=BOTH , expand=True)
        self.entry = Entry(self)
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=15, sticky='we')

        self.entryvar = tk.StringVar()
        self.entry['textvariable'] = self.entryvar

        clearBtn = Button(self , text="Clear", command=self.onClear)
        clearBtn.grid(row=1, column=0, pady=15, padx=10, sticky=W)
        selBtn = Button(self , text="Select all", command=self.onSelectAll)
        selBtn.grid(row=1, column=1, sticky=W)

        deselBtn = Button(self , text="Deselect", command=self.onDeselect)
        deselBtn.grid(row=1, column=2, padx=10)

        sel2clipboard = Button(self, text = 'Selection >> clipboard', command = self.onsel2clipboard)
        sel2clipboard.grid(row = 1, column = 3, padx = 10)

        self.chvar = BooleanVar()
        self.chvar.set(False)
        
        checkBtn = Checkbutton(self , text="readonly", variable=self.chvar , command=self.onChangeReadability)
        checkBtn.grid(row=2, column=0)
        #self.entry.bind("<Control-Key-a>", onSelectAll)  ## this binding is done already

        resettextbtn = Button(self, text = 'reset text', command = self.resettext)
        resettextbtn.grid(row = 2, column = 3, padx = 5)

    def onClear(self):
        self.entry.delete(0, END)


    def resettext(self):
        self.entry.delete(0, END)
        self.entryvar.set(NOWISTIME)


    def onsel2clipboard(self):
        try:
            selection = self.entry.select_range('anchor', 'insert')
            if self.entry.selection():
                print(selection)
        except Exception as e:
            print(e.args)
            raise
        finally:
            return

        selection = self.entry.selection_to(tk.END)
        #selection = self.entry.select_range(ANCHOR, INSERT)
        print(selection)
        
        ##selection = self.entry.selection_to('end')         print(selection)
        if self.entry.selection_present():
            print('entry has a selection')
        return

        self.entry.insert(END, 'hello')
        # previous works fine
        #self.entry.insert('anchor', 'hello') ## ANCHOR fails, saying ANCHOR is not defined
        self.entry.insert('insert', 'GOODBYE')

        print("selected text: '%s'" % self.entry.get())
        selection = self.entryvar.get()
        print(selection)
        print(self.entry.bindtags())  
        print(" this is the order of binding events, left to right  ")
        '''
            The following would reorder the way the bindings are executed.
            To the second, first, third and fourth
            order = self.area.bindtags()
            self.area.bindtags((order[1], order[0], order[2], order[3]))
        '''
        '''
        startndx = self.entry.index(ANCHOR)
        endndx = self.entry.index(INSERT)
        print(startndx, endndx)
        '''

        
    def onSelectAll(self):
        self.selection = self.entry.select_range(0, END)
        clipboard.copy(self.entryvar.get())
        

    def onDeselect(self):
        self.entry.select_clear()


    def onChangeReadability(self):
        if self.chvar.get() == True:
            self.entry.config(state=DISABLED)
        else:
            self.entry.config(state=NORMAL)


def main():
    win = Tk()
    ex = Example(win)
    win.geometry("+800+500")
    win.attributes('-topmost', 1)
    win.mainloop()


if __name__ == '__main__':
    main()