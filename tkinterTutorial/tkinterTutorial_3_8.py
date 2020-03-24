
# -*- coding: utf -8 -*-
"""
ZetCode Tkinter e-book
This script creates a custom event.
Author: Jan Bodnar
Last modified: November 2015
Website: www.zetcode.com
"""
from tkinter import Tk, BOTH , StringVar, messagebox as MB
from tkinter.ttk import Frame , Button , Label
from random import randint
from GlobalErrorHandling import GlobalErrorHandler

class MyRandom(object):
    def __init__(self):
        self.r = 0

    def generate(self):
        self.r = randint(0, 900)
    
    def getRandom(self):
        return self.r

class Example(Frame, GlobalErrorHandler):
    def __init__(self , parent):
        Frame.__init__(self , parent , name="frame")
        GlobalErrorHandler(self).__init__(masterWindow = parent)

        self.parent = parent
        self.mr = MyRandom()
        self.initUI()
        '''-------------------------------protocol handling------------------------------'''
        self.parent.protocol("WM_DELETE_WINDOW", self.onDeleteWindow)


    def initUI(self):
        self.parent.title("Custom event")
        self.pack(fill=BOTH , expand=True)

        self.parent.bind("<<Random >>", self.updateLabel)
        '''               -----------         '''
        btn = Button(self , text="Random", command=self.onClick)
        btn.grid(row=0, column=0, padx=10, pady=10)
        self.lvar = StringVar()
        lbl = Label(self , textvariable=self.lvar)
        lbl.grid(row=0, column=1, padx=50)

    def onDeleteWindow(self):
        ret = MB.askquestion(title="Question", message="Are you sure to quit?", default = MB.NO)
        if (ret == "yes"):
            self.quit()
        else:
            return


    def onClick(self):
        self.mr.generate()
        self.event_generate('<<Random >>')
        '''                  -----------            '''

    def updateLabel(self , e):
        self.lvar.set(self.mr.getRandom ())


def main():
    root = Tk()
    root.geometry("300x200+300+300")
    app = Example(root)
    root.attributes('-topmost', 1)
    root.mainloop()
if __name__ == '__main__':
    main()