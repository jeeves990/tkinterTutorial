

import tkinter as tk
from tkinter import BOTH, RIDGE, RAISED, FLAT, Menu
import tkinter.ttk as ttk
from GlobalErrorHandling import GlobalErrorHandler
import sys

class TestNotebook(tk.Frame):
    def __init__(self, win):
        tk.Frame.__init__(self, win)
        self.win = win
        GlobalErrorHandler(win).__init__(masterWindow = win)
        lbl = tk.Label(self, text = 'hello there')
        lbl.pack(anchor = 'nw', side = 'top', fill = 'x', expand = 1)
        self.initUI()
        self.bldNotebook()
        self.pack(anchor = 'center', expand = True, fill = 'both', ipadx = 2, ipady = 2)



    def initUI(self):
        self.win.title("Submenu")
        self.pack(fill=BOTH , expand=True)

        s = ttk.Style()
        s.configure("Statusbar.TLabel", borderwidth=2, relief=RIDGE)
        s.configure("StatusbarSub.TLabel", borderwidth=2, relief=RIDGE, padx = 5)
        s.configure('TFrame', relief=RAISED)
        s.configure('TButton', relief=FLAT)

        self.menubar = Menu(self.win)
        self.win.config(menu=self.menubar)
        fileMenu = Menu(self.menubar, tearoff=False)
        submenu = Menu(fileMenu , tearoff=False)
        submenu.add_command(label="New feed")
        submenu.add_command(label="Bookmarks")
        submenu.add_command(label="Mail")
        fileMenu.add_cascade(label='Import', menu=submenu , underline =0)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", underline=0, command = self.onExit)
        self.menubar.add_cascade(label="File", underline=0, menu=fileMenu)

        self.showStat = tk.BooleanVar()
        self.showStat.set(True)

        viewMenu = Menu(self.menubar , tearoff=False)
        viewMenu.add_checkbutton(label="Show statusbar",
                command = self.onClick , variable=self.showStat , onvalue=True ,
        offvalue=False)
        self.menubar.add_cascade(label="View", menu=viewMenu)


    def onExit(self):
        sys.exit()

    def onClick(self, e = None):
        pass


    def bldNotebook(self):
        nbFrame = tk.Frame(self)
        nbFrame.pack(fill = 'both', expand=True)

        notebook = ttk.Notebook(nbFrame)
        self.frm1 = tk.Frame(width = 50, height = 100)
        self.frm2 = tk.Frame(width = 50, height = 100)
        self.frm3 = tk.Frame(width = 50, height = 100)
        notebook.add(self.frm1 ,text="Tab 1")
        notebook.add(self.frm2 ,text="Tab 2")
        notebook.add(self.frm3 ,text="Tab 3")
        notebook.pack(pady=5, fill = 'both', expand=True)

        ##self.bldPanedWindow(frame1)

        txt = tk.Text(self.frm1)
        for i in range(1, 99):
            txt.insert(tk.END, 'hello there, big boy\t')
        txt.pack()
        tk.Label(self.frm1, text = 'hello there [1]').pack(anchor = 'nw', side = 'top', fill = 'x', expand = 1)
        tk.Label(self.frm2, text = 'hello there [2]').pack(anchor = 'nw', side = 'top', fill = 'x', expand = 1)
        tk.Label(self.frm3, text = 'hello there [3]').pack(anchor = 'nw', side = 'top', fill = 'x', expand = 1)

if __name__ == '__main__':
    win = tk.Tk()
    win.geometry("+300+300")
    TestNotebook(win)
    win.mainloop()