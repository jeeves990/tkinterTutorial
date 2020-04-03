
"""
In this script , we create a New folder
example with the grid manager.
Author: Jan Bodnar
Last modified: December 2015
Website: www.zetcode.com
page 32 of tutorial
"""
from tkinter import Tk, Text , BOTH , E, W, S, N
from tkinter.ttk import Frame , Button , Label , Entry

class Example(Frame):
    def __init__(self , parent):
        Frame.__init__(self , parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("New folder")

        self.pack(fill=BOTH , expand=True)
        
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(0, pad=10)
        
        lbl = Label(self , text="Name:")
        lbl.grid(row=0, column=0, padx=5)
        entry = Entry(self)
        entry.grid(row=0, column=1, columnspan=4, padx=5, sticky=W+E)
        txt = Text(self , width=20, height =10)
        txt.grid(row=1, column=0, columnspan=5, padx=5, pady=5,
        sticky=E+W+N+S)
        okBtn = Button(self , text="OK")
        okBtn.grid(row=3, column=3, sticky=E)
        closeBtn = Button(self , text="Close")
        closeBtn.grid(row=3, column=4, padx=5, sticky=E)

def main():
    win = Tk()
    win.geometry("330x300+300+300")
    app = Example(win)
    win.mainloop()

if __name__ == '__main__':
    main()
