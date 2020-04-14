
# -*- coding: utf -8 -*-
"""
ZetCode Tkinter e-book
This script creates a simple animation.
Author: Jan Bodnar
Last modified: November 2015
Website: www.zetcode.com
"""

import tkinter as tk
from PIL import Image , ImageTk
from tkinter import Tk, BOTH , CENTER
from tkinter.ttk import Frame , Label
from GlobalErrorHandling import GlobalErrorHandler as ER
 
DELAY = 850

class Example(Frame, ER):
    def __init__(self , parent):
        Frame.__init__(self , parent , name="frame")
        ER(parent).__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Animation")
        self.pack(fill=BOTH , expand=True)
        self.topframe = Frame(self)
        self.topframe.pack(side = tk.TOP, anchor = 'nw', fill = BOTH)
        self.lblCount = Label(self.topframe, text = 'lblcount')
        self.lblCount.pack(side = tk.LEFT, padx = 16, pady = 16)
        self.btnRestart = tk.Button(self.topframe, text = 'Restart animation', command = self.onrestart)
        self.btnRestart.pack(side = tk.RIGHT, padx = 16, pady = 16)


        self.img_names = ("1.png", "2.png", "3.png",
                            "4.png", "5.png", "6.png", "7.png",
                            "8.png", "9.png")
        self.label = Label(self)
        self.label.pack(pady=30)
        self.onrestart()


    def onrestart(self):
        self.i = 0
        self.doCycle()
        return
        img = Image.open(self.img_names[self.i])
        self.num = ImageTk.PhotoImage(img)
        ##self.label['image'] = self.num
        
        # reference must be stored
        self.label['image'] = self.num
        self.after(DELAY , self.doCycle)


    def doCycle(self):
        while True:
            if (self.i >= 9):
                break
            self.lblCount['text'] = str(self.i +1)
            img = ImageTk.PhotoImage(Image.open(self.img_names[self.i]))
            self.label.configure(image=img)
            self.label['image'] = img
            self.i += 1

            '''
                to make the iterative display of the images work, 
                I had to do the following self.update()
            '''
            self.update()

            '''
                Is this is a recursive call. If so, why?
                It probably is not since it actually will execute 
                commands below it.
            '''
            ##self.after(DELAY , self.doCycle)   
            ## self.i += i
                                    
            self.after(DELAY)
        self.lblCount['text'] = 'unloaded'
            
"""
this works
    def doCycle(self):
        ##while True:
            if (self.i >= 9):
                return
            self.lblCount['text'] = str(self.i +1)
            img = ImageTk.PhotoImage(Image.open(self.img_names[self.i]))
            self.label.configure(image=img)
            self.label.image = img
            self.after(DELAY , self.doCycle)   ## this is a recursive call. why?????
            ##self.after(DELAY)
            self.i += 1

"""
def main():
    root = Tk()
    root.geometry("800x800+300+300")
    root.attributes('-topmost', 1)
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()