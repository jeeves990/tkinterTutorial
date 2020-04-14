
# -*- coding: utf -8 -*-
from tkinter import Tk, Toplevel , BitmapImage
from tkinter.ttk import Label
"""
ZetCode Tkinter e-book
This script creates a floating window.
The window has a grip by which we can
drag it and move it.
Author: Jan Bodnar
Last modified: November 2015
Website: www.zetcode.com
"""
BITMAP = """

#define grip_width 15
#define grip_height 29
static unsigned char grip_bits[] = {
    0x55 , 0x55 , 0x00 , 0x00 , 0x55 , 0x55 , 0x00 , 0x00 , 0x55 , 0x55 ,
    0x00 , 0x00 , 0x55 , 0x55 , 0x00 , 0x00 , 0x55 , 0x55 , 0x00 , 0x00 ,
    0x55 , 0x55 , 0x00 , 0x00 , 0x55 , 0x55 , 0x00 , 0x00 , 0x55 , 0x55 ,
    0x00 , 0x00 , 0x55 , 0x55 , 0x00 , 0x00 , 0x55 , 0x55 , 0x00 , 0x00 ,
    0x55 , 0x55 , 0x00 , 0x00 , 0x55 , 0x55 , 0x00 , 0x00 , 0x55 , 0x55 ,
    0x00 , 0x00 , 0x55 , 0x55 , 0x00 , 0x00 , 0x55 , 0x55 };
"""
class Example(Toplevel):
    def __init__(self , parent):
        Toplevel.__init__(self , parent)
        self.initUI()


    def initUI(self):
        self.overrideredirect(True)  ## removes the window decoration

        bitmap = BitmapImage(data=BITMAP)  ## a bitmap is created from the data provided

        msg = "Click on the grip to move\nRight click to terminate"
        self.label = Label(self , text=msg)
        self.grip = Label(self , image=bitmap)
        self.grip.image=bitmap
        self.grip.pack(side="left", fill="y")
        self.label.pack(side="right", fill="both", padx=3, expand=True)
        self.grip.bind("<ButtonPress -1>", self.startMove)
        self.grip.bind("<ButtonRelease -1>", self.stopMove)
        self.grip.bind("<B1-Motion >", self.onMotion)
        self.bind("<ButtonPress -3>", self.onRightClick)
        self.geometry("+300+300")


    def startMove(self , e):
        self.x = e.x
        self.y = e.y


    '''
        onMotion is called for every pixel moved, I bet.
        and gives a more or less smooth move.
    '''
    def onMotion(self , e):
        deltax = e.x - self.x
        deltay = e.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry("+%s+%s" % (x, y))
    
        
    def stopMove(self , e):
        e.x = None
        e.y = None


    def onRightClick(self , e):
        self.quit()


def main():
    root = Tk()
    app = Example(root)
    root.withdraw()
    root.mainloop()

if __name__ == '__main__':
    main()