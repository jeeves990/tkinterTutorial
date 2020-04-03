# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:04:27 2020

@author: FBA_S
"""

from tkinter import Tk, LEFT , BOTH , StringVar
from tkinter.ttk import Frame , Style , Label , Combobox


class Example(Frame):
    def __init__(self , parent):
        Frame.__init__(self , parent)
        self.parent = parent
        self.initUI()
    
    
    def initUI(self):
        self.parent.title("Combobox")
        self.pack(fill=BOTH , expand=1)
        self.cvar = StringVar()
        
        combo = Combobox(self , textvariable=self.cvar)
        combo.event_generate("<<ComboboxSelected>>", when = 'tail')
        ##combo.event_add("<<ComboboxSelected>>", "Button-1")
        combo.bind("<<ComboboxSelected>>", self.onComboSelect)
        combo['values'] = ('OpenBSD', 'NetBSD', 'FreeBSD')
        combo.current (0)
        combo.pack(side=LEFT , padx=15)
        
        self.lvar = StringVar()
        self.lvar.set("OpenBSD")
        lbl = Label(self , textvariable=self.lvar)
        lbl.pack(side=LEFT, anchor = 'e')


    def onComboSelect(self , e):
        w = e.widget
        self.lvar.set(w.get())
        
        
def main():
    root = Tk()
    ex = Example(root)
    root.geometry("+300+300")
    root.attributes('-topmost', 1)
    root.mainloop()
    
    
if __name__ == '__main__':
    main()