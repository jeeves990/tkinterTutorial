# -*- coding: utf -8 -*-
"""
    ZetCode Tkinter e-book
    This script creates nofitication windows
    from mouse press and mouse release events.
    Author: Jan Bodnar
    Last modified: November 2015
    Website: www.zetcode.com
"""
from tkinter import Tk, BOTH , Toplevel
from tkinter.ttk import Frame , Label , Style
from tkinter import messagebox
import time


class NotifyWindow(Toplevel):
    def __init__(self , parent , elapsed , screen_x , screen_y):
        Toplevel.__init__(self , parent , background="sky blue")
        self.overrideredirect(True)
        self.el = elapsed
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.initUI()


    def initUI(self):
        s = Style()
        s.configure('TLabel', background='sky blue')
        lbl = Label(self , text=str(self.el) + " ms")
        lbl.pack(padx=5, pady=5)
        self.update()
        h = self.winfo_height()
        self.geometry('+{0}+{1}'.format(self.screen_x , self.screen_y -h))
        self.after(self.el, self.destroyWin)


    def destroyWin(self):
        self.destroy()


class Example(Frame):
    def __init__(self , parent):
        Frame.__init__(self , parent , name="frame")
        self.parent = parent
        self.initUI()


    def initUI(self):
        self.parent.title("Notify")
        self.pack(fill=BOTH , expand=True)
        self.bind("<Button -1>", self.onPress)
        self.bind("<ButtonRelease -1>", self.onRelease)


    def onPress(self , e):
        self.start = time.time()


    def onRelease(self , e):
        screen_x = e.x_root
        screen_y = e.y_root
        self.stop = time.time()
        el = self.stop - self.start
        el_ms = el * 1000
        el_r = round(el_ms)
        self.createNotificationWindow(el_r , screen_x , screen_y)


    def createNotificationWindow(self , elapsed , screen_x , screen_y):
        nwin = NotifyWindow(self , elapsed , screen_x , screen_y)


def main():
    root = Tk()
    root.geometry("350x250+300+300")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()
