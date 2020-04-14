

import sys
import tkinter as tk
from tkinter import Tk, Text , BOTH , W, N, E, S, messagebox as MB
from tkinter.ttk import Frame , Button , Label , Style
from GlobalErrorHandling import GlobalErrorHandler as ERHandler

BOUNDCOLOR = 'green'
UNBOUNDCOLOR = 'red'

class Example(Frame, ERHandler):
    def __init__(self , parent):
        Frame.__init__(self , parent)
        ERHandler(parent).__init__(masterWindow = parent)
        self.win = parent
        self.win.bind('<Escape>', self.onclose)
        self.initUI()


    def initUI(self):
        self.win.title("Windows")
        self.pack(fill=BOTH , expand=True)
        
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)
        
        lbl = Label(self , text="Windows")
        lbl.grid(row = 0, column = 1, columnspan = 4, sticky=W, pady=4, padx=5)
        
        area = Text(self)
        area.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky=E+W+S+N)

        abtn = Button(self , text="Activate")
        abtn.grid(row=1, column=3)
        
        cbtn = Button(self , text="Close", command = self.onclose)
        cbtn.grid(row=2, column=3, pady=4)
        
        hbtn = Button(self , text="Help")
        hbtn.grid(row=5, column=0, padx=5)
        
        obtn = Button(self , text="OK")
        obtn.grid(row=5, column=3)

        self.var = tk.BooleanVar()
        cb = tk.Checkbutton(self , text="Bind event", variable=self.var, command=lambda : self.onBind(self.testbtn))
        cb.config(state = 'active')
        cb.grid(row = 4, column = 3)
       
        self.testbtn = tk.Button(self, text = 'BOUND', padx = 16, pady = 10, command = self.testbtnonclick)
        self.testbtn['fg'] = BOUNDCOLOR
        self.testbtn.grid(row = 3, column = 3)
        self.bind_class("TButton", "<Button -1>", self.onButtonsClick)
        self.bind_class("Button", "<Button -1>", self.onButtonsClick)


    def onButtonsClick(self , e):
        print(e.widget._name, e.x, e.y)
        

    def onBind(self , w):
        if (self.var.get() == True):
            try:
                w.bind("<Button -1>", self.onClick)
                self.testbtn['fg'] = BOUNDCOLOR
                self.testbtn['text'] = 'BOUND'
            except Exception as e:
                MB.showinfo(e.message)
        else:   
            try:
                w.unbind("<Button -1>")
                self.testbtn['fg'] = UNBOUNDCOLOR
                self.testbtn['text'] = 'unBound'
            except Exception as e:
                MB.showinfo(e.message)

    def onClick(self , e):
        print("clicked")

    def testbtnonclick(self):
        if self.testbtn['fg'] == BOUNDCOLOR:
            MB.showinfo("I'm bound to the left mouse button")
        else:
            MB.showinfo("I AM NOT BOUND")

    def onclose(self, e = None):
        reply = MB.askquestion('closing', 'Do you wish to quit the app?')
        if reply == 'yes':
            sys.exit(0)


def main():
    win = Tk()
    win.geometry("350x300+300+300")
    app = Example(win)
    win.mainloop()


if __name__ == '__main__':
    main()

