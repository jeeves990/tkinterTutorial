# -*- coding: utf -8 -*-
"""
        ZetCode Tkinter e-book
        In this script , attach a vertical Scrollbar
        to the Canvas widget.
        Author: Jan Bodnar
        Last modified: November 2015
        Website: www.zetcode.com
"""

import tkinter as tk

from tkinter import Tk, BOTH , RIGHT , LEFT , Y, ALL , Canvas , VERTICAL
import tkinter.ttk as ttk
from tkinter.ttk import Frame , Scrollbar , Label, Notebook, PanedWindow


FONT_SIZE = 12
YOFFSET = 10
XOFFSET = 20

DELAY1 = 30
DELAY2 = 20

class Example(Frame):
    def __init__(self , parent):
        Frame.__init__(self , parent)
        self.parent = parent
        self.pw = tk.PanedWindow(orient = "vertical", sashwidth = 3)
        self.pw.pack(fill=BOTH, expand=True)

        self.pw.add(self.bldSideBarLeft())
        self.pw.add(self.bldRightSide())
        self.pw.add(self.bldProgBarFrame())
        
        
    def bldProgBarFrame(self):
        frm = tk.Frame(width = 200, height = 200, background = 'cyan')
        self.pb1 = ttk.Progressbar(frm , mode='determinate', name='pb1')
        self.pb2 = ttk.Progressbar(frm , mode='indeterminate', name = 'pb2')

        startBtn =ttk.Button(frm , text='Start', command=lambda: self.updateBars('start'))
        stopBtn = ttk.Button(frm , text='Stop', command=lambda: self.updateBars('stop'))

        self.pb1.grid(row=0, column=0, columnspan=2, pady=15, padx=10, sticky = 'we')
        self.pb2.grid(row=1, column=0, columnspan=2, padx=10, sticky = 'we')
        startBtn.grid(row=2, column=0, pady=15, padx=10, sticky = 'e')
        stopBtn.grid(row=2, column=1, padx=10, sticky = 'w')
        return frm

    
    def updateBars(self , op):
        #self.pb1 = self.nametowidget('pb1')
        #self.pb2 = self.nametowidget('pb2')
        if op == 'start':
            self.pb1.start(DELAY1)
            self.pb2.start(DELAY2)
        else:
            self.pb1.stop()
            self.pb2.stop()


    def bldRightSide(self):
        sidebar = tk.PanedWindow(orient="horizontal", sashwidth = 3)
        main = tk.Frame(width=200, height= 200, background="dark gray")
        _lbl_ = tk.Label(main, text = 'Main Frame', fg = 'white', bg = "dark gray")
        _lbl_.pack(anchor = 'center')

        sidebar_top = tk.Frame(sidebar, width=200, height = 200, background = "gray")
        
        lbl = Label(sidebar_top, text = 'sidebar_top')
        lbl.pack()
        sidebar_bottom = tk.Frame(sidebar, width=200, height=200, background="white")
        _lbl = Label(sidebar_bottom, text = 'sidebar_bottom')
        _lbl.pack()

            # add the top and bottom to the sidebar
        sidebar.add(sidebar_top)
        sidebar.add(sidebar_bottom)
        self.pw.add(main)
        return sidebar


    def bldSideBarLeft(self):
        frm = tk.Frame(height = 400, width = 400, background = 'cyan')
        lbl = Label(frm, text = 'hello there, big boy')
        lbl.pack()
        
        sbCanvas = Canvas(frm)
        sbar = Scrollbar(frm, orient=VERTICAL, command = sbCanvas.yview)
        sbCanvas.configure(yscrollcommand = sbar.set)
        sbar.pack(side=RIGHT , fill=Y)
        sbCanvas.pack(side=LEFT, fill=BOTH , expand=True)

        
        for i in range (100):
            x = XOFFSET
            y = i*(YOFFSET + FONT_SIZE) + YOFFSET
            sbCanvas.create_text(x, y, font=("times", FONT_SIZE), text="Item " + str(i))

        self.bind("<Configure>", self.onConfigure)
        return frm
            

    def onConfigure(self , event):
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))


    def bldNotebook(self):
        nbFrame = Frame(self)
        nbFrame.pack(fill=BOTH, expand=True)

        notebook = Notebook(nbFrame)
        frame1 = Frame()
        frame2 = Frame()
        frame3 = Frame()
        lbl1 = Label(frame1 , text="Pane 1")
        lbl1.place(x=30, y=40)
        lbl2 = Label(frame2 , text="Pane 2")
        lbl2.place(x=30, y=40)
        lbl3 = Label(frame3 , text="Pane 3")
        lbl3.place(x=30, y=40)
        notebook.add(frame1 ,text="Tab 1")
        notebook.add(frame2 ,text="Tab 2")
        notebook.add(frame3 ,text="Tab 3")
        notebook.pack(pady=5, fill=BOTH , expand=True)
        return nbFrame

    
def main():
    root = Tk()
    ex = Example(root)
    root.geometry("+850+550")
    root.attributes('-topmost', 1)
    root.mainloop()


if __name__ == '__main__':
    main()
