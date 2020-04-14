

import tkinter as tk
from tkinter.ttk import Treeview
import tkinter.ttk as ttk
from tkinter import PanedWindow, Frame, Label, BOTH, VERTICAL, HORIZONTAL, Entry, Scale, Button,\
        Menu, messagebox as MSGBOX, DoubleVar, IntVar, StringVar, LEFT, Canvas, OptionMenu, LabelFrame

import sys

import os
import winreg as winreg
import inspect
from modalDialog import TreeviewUtilities


TVUCOLUMNS = {
                0:"Value Name",
                1:"Value Type",
                2:"Value"
             }


def setColRowWeight(obj, row_weight = 1, col_weight = 1, **kwargs):
    try:
        colCount, rowCount = obj.grid_size()
        if 'colCount' in kwargs:
            colCount = kwargs['colCount']
        if 'rowCount' in kwargs:
            rowCount = kwargs['rowCount']
        if not colCount:
            colCount = 1
        if not rowCount:
            rowCount = 1


        
        for i in range(0, rowCount):
            obj.grid_rowconfigure(i, weight = row_weight)

        for i in range(0, colCount):
            obj.grid_columnconfigure(i, weight = col_weight)
    except Exception as e:
        msg = 'setColRowWeight: has failed with [{}]'.format(e.args)
        MSGBOX.showinfo('Exception: non fatal', msg)


class InitUI(Frame):
 
    def __init__(self, win):
        Canvas.__init__(self, win)

        self.win = win
        self['bg'] = 'blanched almond'

        self.style = ttk.Style()
        self.bldTabNotebook()
        self.bldPanedWindow(self.mainHiveFrame)

        #self.bldStatusBar()
        self.pack(fill = 'both', anchor = 'center', expand = True)

        
    def bldTabNotebook(self):
        nbFrame = tk.Frame(self)
        nbFrame.pack(fill = 'both', expand=True)

        notebook = ttk.Notebook(nbFrame)
        self.mainHiveFrame = tk.Frame()
        self.fileRepeaterFrame = tk.Frame(bg = 'light pink')
        writebackframe = tk.Frame()
        notebook.add(self.mainHiveFrame, text="Registry Hives")
        notebook.add(self.fileRepeaterFrame, text="Hives as File")
        notebook.add(writebackframe ,text="Treeview write back")
        notebook.pack(pady=5, fill = 'both', expand=True)

        
    def bldPanedWindow(self, parentFrame):
        self.pnWin = PanedWindow(parentFrame)
        self.pnWin.config(bg = 'CadetBlue1', orient = 'horizontal', 
                          sashwidth = 6, sashrelief = 'sunken',
                          relief = 'groove')
        
        #maintreeFrame = 
        pnTreeWin = LabelFrame(self.pnWin, bg = 'yellow', text = 'yellow: mainTreeFrame')
        self.bldHiveView(pnTreeWin)
        setColRowWeight(pnTreeWin) ##, colCount = 2, rowCount = 0)

        self.pnWin.paneconfig(pnTreeWin, minsize = 250)
        
        self.pnWin.add(pnTreeWin, stretch = 'never')

        valueFrame = Frame(self.pnWin, bd = 5, bg = 'purple1', width = 35)
        self.valueFrameLbl = Label(valueFrame, text = 'hello', relief = 'raised')
        self.valueFrameLbl.pack(side = 'top', fill = 'x', expand = 'false')
        self.pnWin.add(valueFrame, stretch = 'always')
        self.addValueTvu(valueFrame)
        
        self.pnWin.pack(fill = BOTH, anchor = 'center', padx = 4, pady = 4, expand = True)
        
    
    def addValueTvu(self, frm):
        self.valTvu = Treeview(frm)
        self.valTvu['columns'] = (TVUCOLUMNS[0], TVUCOLUMNS[1], TVUCOLUMNS[2])
        self.valTvu['show'] = 'headings'
        
        self.valTvu.column(TVUCOLUMNS[0], width = 100, anchor='center')
        self.valTvu.heading(TVUCOLUMNS[0], text = 'Value Name')
        
        self.valTvu.column(TVUCOLUMNS[1], width = 100, anchor='center')
        self.valTvu.heading(TVUCOLUMNS[1], text = 'Value Type')
        
        self.valTvu.column(TVUCOLUMNS[2], width = 100, anchor='center')
        self.valTvu.heading(TVUCOLUMNS[2], text = 'Value')
        
        self.valTvu.pack(anchor = 'center', fill = BOTH, expand = True)
        

    def bldHiveView(self, pnTreeWin):
        chooseFrame = Frame(pnTreeWin)
        chooseFrame['bg'] = pnTreeWin['bg']
        cbOpt = ttk.Combobox(chooseFrame, justify = 'center')
        
        setColRowWeight(cbOpt)
        cbOpt.grid(row = 0, column = 0, sticky = 'ew', columnspan = 3)
        setColRowWeight(cbOpt, rowCount = 1, col_weight = 1, colCount = 3)

        self.treebldbtn = Button(chooseFrame, text = 'Build')
        self.treebldbtn.grid(row = 0, column = 3, padx = 3, sticky = 'e')

        chooseFrame.grid(sticky = 'new', columnspan = 3)
        setColRowWeight(chooseFrame)

        def buildHiveTvu():
            hiveTreeFrame = LabelFrame(pnTreeWin, text = 'turquoise', bg = 'turquoise')
            lbl = Label(hiveTreeFrame, text = 'hiveTreeFrame')
            lbl.grid(row = 0, column = 0, columnspan = 2, rowspan = 1, sticky = 'new')
            setColRowWeight(lbl,  colCount = 0, rowCount = 0)

            self.hiveTreeview = Treeview(hiveTreeFrame, padding = (2,2,2,2))
            self.hiveTreeview.heading('#0', text = 'Registry Hive', anchor = 'w')
            
            
            ysb = ttk.Scrollbar(hiveTreeFrame, orient='vertical', command=self.hiveTreeview.yview)
            xsb = ttk.Scrollbar(hiveTreeFrame, orient='horizontal', command=self.hiveTreeview.xview)
            self.hiveTreeview.configure(yscroll=ysb.set, xscroll=xsb.set)
            
            self.hiveTreeview.grid(row = 0, column = 0, sticky = 'news', rowspan = 3, columnspan = 2)

            # ---- if hiveTreeFrame row == 0 it is sticky just right 
            # -------- but it covers the Combobox.
            # --BUT-- set it to row == 1, where it should be AND it is sticky 'ews' 
            # -----------but only a ratio of north
            hiveTreeFrame.grid(row = 1, column = 0, sticky = 'news', rowspan = 6, columnspan = 3)
            setColRowWeight(hiveTreeFrame, row_weight = 1, rowCount = 2)

            colCount, rowCount = hiveTreeFrame.grid_size()
            ysb.grid(row = 0, column = colCount, sticky = 'ns', rowspan = rowCount)
            xsb.grid(row = rowCount +1, column = 0, sticky = 'we', columnspan = colCount)
          
        buildHiveTvu()
        

if __name__ == '__main__':
    win = tk.Tk()
    x = 1000
    y = 500
    win.geometry('+{0}+{1}'.format(x,y))
    win.attributes('-topmost', 1)
    win.config(bd = 4)
    ttl = os.path.basename(sys.argv[0])
    win.title(ttl)
    InitUI(win)
    win.mainloop()

    
