#!/usr/bin/env python3

"""
        ZetCode Tkinter e-book
        This script shows a simple window
        on the screen.
        Author: Jan Bodnar
        Last modified: January 2016
            Website: www.zetcode.com
"""
from tkinter import Tk, BOTH, Scrollbar, Canvas
from tkinter.ttk import Frame, Label, Button



''' COLORS = [ "#f45", "#ee5", "#aa4", "#a1e433", "#e34412", "#116611", "#111eeefff", "#3aa922191", "#abbabbaaa" ]   '''
import PyColorNList

class Example(Canvas):
    def __init__(self , parent):
        Canvas.__init__(self , parent)
        self.parent = parent
        self.configure(cursor = 'based_arrow_up')  ##'circle')
        self.initUI()
        frame = Frame(self)
        self.create_window((0,0), window=frame, anchor='nw')
        

    def initUI(self):
        self.parent.title("Simple")
        ##self.pack(fill=BOTH , expand=True)
        self.grid(row = 0, column = 0)
        self.centerWindow()
        self.addScrollbar()
        self.addColors()

    def addScrollbar(self):
        sbar = Scrollbar(self.parent, orient = 'vertical', command = self.yview, width = 16)
        self.configure(yscrollcommand = sbar.set)
        sbar.grid(row = 0, column = 1)


    def addColors(self):
        colors = PyColorNList.COLORS
       
        _row = 0
        color = 0
        column = 0
        while True:  ## this will be the row loop

            while True:    ## this will be the color loop
                thiscolor = colors[color]
                lbl = Label(self , text=thiscolor , background=thiscolor)
                lbl.grid(row = _row, column = column)

                column += 1   ## move to the next column
                btn = Button(self, text = thiscolor)
                btn.grid(row = _row, column = column)
                column += 1
                
                color += 1
                if color == len(colors):  ## don't overrun the colors list
                    break   ## the inner <color> loop
                if column == 16:
                    column = 0
                    break

            if color == len(colors):
                break  ## the outer <row> loop
            _row += 1

    def centerWindow(self):
        w = 290
        h = 150
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('+%d+%d' % (x, y))


def main():
    root = Tk()
    ##root.geometry("%dx%d+%d+%d" % (250, 150, 300, 300))
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()