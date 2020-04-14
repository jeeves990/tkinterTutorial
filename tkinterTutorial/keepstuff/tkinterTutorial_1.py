#!/usr/bin/env python3

"""
ZetCode Tkinter e-book
In this script , we change the default style
for the label widget class.
Author: Jan Bodnar
Last modified: January 2016
Website: www.zetcode.com
"""
from tkinter import Tk, BOTH
from tkinter.ttk import Frame , Label , Style, Entry

class Example(Frame):
    def __init__(self , parent):
        Frame.__init__(self , parent)
        self.parent = parent
        self.initUI()


    def initUI(self):
        self.pack(fill=BOTH , expand=True)
        s = Style()
        s.configure('TLabel', background='dark sea green',
        font=('Helvetica', '16'))
        lbl1 = Label(self , text="zetcode.com")
        lbl2 = Label(self , text="spoznaj.sk")
        lbl1.pack()
        lbl2.pack()
        self.moreStyles()

    def moreStyles(self):
        self.parent.title("Custom styles")
        self.pack(fill=BOTH , expand=True)

        from tkinter.ttk import Notebook
        notebook = Notebook(self)
        s = Style()
        s.configure('Tab1.TFrame', background='midnight blue')
        s.configure('Tab2.TFrame', background='lime green')
        s.configure('Tab3.TFrame', background='khaki')
        frame1 = Frame(width=400, height=300, style='Tab1.TFrame')
        frame2 = Frame(width=400, height=300, style='Tab2.TFrame')
        frame3 = Frame(width=400, height=300, style='Tab3.TFrame')
        notebook.add(frame1 , text="Tab 1")
        notebook.add(frame2 , text="Tab 2")
        notebook.add(frame3 , text="Tab 3")
        notebook.pack(pady=5)


def main():
    root = Tk()
    ex = Example(root)
    root.geometry("250x100+300+300")
    root.mainloop()
if __name__ == '__main__':
    main()