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
from tkinter import Tk, LEFT , BOTH , StringVar
from tkinter.ttk import Entry , Frame , Label
from GlobalErrorHandling import GlobalErrorHandler as GERR

def callback(*args):
    print("variable changed!")


#%%
class Example(Frame):
    def __init__(self, parent, **kwargs):
        win = parent
        GERR(self).__init__(win, **kwargs)
        Frame.__init__(self, win, **kwargs)  
        
        self.parent = parent
        self.parent.title("Entry")
        self.initUI()
        self.pack(fill=BOTH , expand=1)
        self.entry.focus_set()


    def initUI(self):
        self.entry = Entry(self)
        self.lbl = Label(self)
        
        
        self.evar = StringVar()
        ##evar.trace("write", self.onChanged)
        self.evar.trace_add("write", callback)
        self.evar.trace_add('write', self.onChanged)
        self.entry['textvariable'] = self.evar
                
        self.lvar = StringVar()
        self.lvar.set("...")
        self.lbl['textvariable'] = self.lvar
        
        self.entry.pack(side=LEFT , padx=15)
        self.lbl.pack(side=LEFT)
        self.entry.focus_set()
       
    

    def onChanged(self, *args):
        self.lvar.set(self.evar.get())

#%%
def main():
    win = Tk()
    win.geometry("250x100+800+500")
    win.attributes('-topmost', 1)
    ex = Example(win)
    win.mainloop()

if __name__ == '__main__':
    main()