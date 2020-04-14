"""
ZetCode Tkinter e-book
This program presents the command
parameter.
Author: Jan Bodnar
Last modified: November 2015
Website: www.zetcode.com
"""

import tkinter as tk
from tkinter import Tk, BOTH , LEFT, BooleanVar, IntVar
from tkinter.ttk import Frame , Button , Checkbutton, Radiobutton, Style
from tkinter import messagebox as MB

class Example(Frame):
    def __init__(self , parent):
        Frame.__init__(self , parent , name="frame")
        self.parent = parent
        self.initUI()

    def initUI(self):
        gui_style = Style()
        gui_style.configure('My.TRadioButton', foreground='#334353')
        gui_style.configure('My.TFrame', columnspan = 4)

        self.parent.title("Commands")
        self.pack(fill=BOTH , expand=True)

        self.btn = tk.Button(self , text="Button", command=self.onButton1Click)
        self.btn.grid(row = 0, column = 0, padx=15)
        ##self.btn.config(foreground = 'green')
        self.btn['fg'] = 'dark green'

        ##cb = Checkbutton(self , text="Checkbutton", command=self.onButton2Click)
        ##cb.pack(side=LEFT)
        self.parent.bind("<Escape>", self.quitApp)

        self.var = BooleanVar()
        cb = Checkbutton(self , text="Bind event", variable=self.var, command=lambda : self.onBind(self.btn))
        cb.grid(row=0, column=1)

        self.rbvar = IntVar()
        self.rbvar.set(1)
        self._1 = 5
        self._2 = 10 
        self._3 = 15
        btnFrame = tk.Frame(self)
        self.rb0 = tk.Radiobutton(btnFrame, text = "On", variable = self.rbvar, value = self._1, foreground = 'red', background = 'light gray', command = self.rbSelected)
        self.rb1 = tk.Radiobutton(btnFrame, text = "Off", variable = self.rbvar, value = self._2, background = 'light gray', command = self.rbSelected)
        self.rb2 = tk.Radiobutton(btnFrame, text = "Limbo", variable = self.rbvar, value = self._3, background = 'light gray', command = self.rbSelected)
        self.rb0.grid(row = 0, column = 0)
        self.rb1.grid(row = 0, column = 1)
        self.rb2.grid(row = 0, column = 2)
        btnFrame.grid(row = 1, column = 0, sticky = 'news', padx = 6, pady = 12)



    def rbSelected(self):
        self.btn['fg'] = self.rb0['fg'] = self.rb1['fg'] = self.rb2['fg'] = 'black'
        if self.rbvar.get() == self._1:
            print('Radio button 1')
            self.btn['fg'] = self.rb0['fg'] = 'green'
        elif self.rbvar.get() == self._2:
            print('Radio button 2')
            self.btn['fg'] = self.rb1['fg'] = 'red'
        elif self.rbvar.get() == self._3:
            print('Radio button 3')
            self.btn['fg'] = self.rb2['fg'] = 'cyan'
        else:
            MB.showinfo(title = 'Tilt!!', message = 'Something went wrong. rbvar is: ' +str(self.rbvar))
                        
    def onBind(self , w):
        if (self.var.get() == True):
            w.bind("<Button-1>", self.onButton1Click)
            print('the BIND')
        else:
            print('the unbind')
            w.unbind("<Button-1>")

    def quitApp(self, e):
        if MB.askokcancel("Question", "Are you sure you wish to quit?"):
            self.quit()
        

    def onButton1Click(self):
        print("Push Button clicked")

    def onButton2Click(self):
        print("Checkbutton clicked")


def main():
    win = Tk()
    win.geometry("250x150+300+300")
    win.wm_attributes("-topmost", 1)    
    app = Example(win)
    win.mainloop()

if __name__ == '__main__':
    main()