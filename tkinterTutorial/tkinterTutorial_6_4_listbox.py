# -*- coding: utf -8 -*-
"""
            ZetCode Tkinter e-book
            In this script , we dynamically add and remove Listbox
            items.
            Author: Jan Bodnar
            Last modified: November 2015
            Website: www.zetcode.com
"""


import tkinter as tk
from GlobalErrorHandling import GlobalErrorHandler
import sys
from tkinter import Tk, BOTH , Listbox , BooleanVar , END,\
        E, W, S, N, Frame
from tkinter.ttk import Button , Entry, Notebook
from tkinter.font import Font
import re
from MyTkFontChooser import askfont


TAB1 = 'Listbox Example'
TAB2 = 'Text Example'
TAB3 = 'tab 3'

##DEFAULTFONT = {'family': 'Times', 'size':10, 'weight':'normal', 'slant':'roman', 'underline':1}
##DEFAULTFONT = "{'family'='@Microsoft\\ JhengHei', 'size'= 20, 'weight'= 'bold', 'slant' =  'italic', 'underline'=1, 'overstrike'=1}"
DEFAULTFONT = '@Microsoft\\ JhengHei\\ UI\\ Light 18 normal italic overstrike'


class Example(Frame):
    def __init__(self, win):
        Frame.__init__(self , win)
        self.win = win
        GlobalErrorHandler(win).__init__(masterWindow = win)
        self.win.title("tkinterTutorial_6_4_listbox.py")
        self.config(bg = 'light pink')

        self.idxSelect = ()
        
        self.frm1 = None
        self.frm2 = None
        self.frm3 = None

        self.fontVar = tk.StringVar()
        self.fontVar.trace("w", self.check_fontVar)
        

        nbk = self.crtTabbedNotebook()
       
        self.entry.focus_set()
        self.nbk.pack(anchor = 'center', fill=BOTH , expand = True)
        self.pack(anchor = 'center', expand = True, fill = 'both', ipadx = 2, ipady = 2)
  

    def crtTabbedNotebook(self):
        self.nbk = Notebook(self)
        
        self.frm1 = tk.Frame(width = 50, height = 25, bg = 'ivory2')
        self.frm2 = tk.Frame(width = 50, height = 25, bg = 'sandy brown')
        self.frm3 = tk.Frame(width = 50, height = 5, bg = 'LemonChiffon2')
       
        self.nbk.add(self.frm1, text = TAB1)
        self.nbk.add(self.frm2, text = TAB2)
        self.nbk.add(self.frm3, text = TAB3)
        
        self.bldFrm4Listbox()
        self.bldFrm4Text()
        
    def bldFrm4Text(self):
        topfrm = tk.Frame(self.frm2)
        self.textFont = DEFAULTFONT
        self.lblFont = tk.Label(topfrm, text = DEFAULTFONT, font = DEFAULTFONT)
        self.lblFont.grid(row = 0, column = 5, padx = 5, columnspan = 4)
        btn = tk.Button(topfrm, text = 'Choose font', command = self.chooseFont)
        btn.grid(row = 0, column = 0, padx = 5)

        topfrm.pack(side = 'top', fill = 'x', expand = True)
        self.text = tk.Text(self.frm2, font = self.textFont)
        for i in range(1, 99):
            self.text.insert(tk.END, 'hello there, big boy\t')
        self.text['font'] = self.textFont
        self.text.pack(fill = 'both', ipadx = 3, ipady = 3, expand = True)

    
    def check_fontVar(self, index, value, op):
        if self.fontVar.get():
            fontString = self.fontVar.get()
            self.text['font'] = fontString
            self.lblFont['font'] = fontString
            self.lblFont['text'] = fontString.replace('\ ', ' ')


    def chooseFont(self):
        font_ = askfont(self.win)
        print(font_)
        ##self.lblFont.config(text = font_, font = font_)
       
        if font_:
            self.fontVar.set('')
            # spaces in the family name need to be escaped
            font_['family'] = font_['family'].replace(' ', '\ ')
            font_str = "%(family)s %(size)i %(weight)s %(slant)s" % font_
            if font_['underline']:
                font_str += ' underline'
            if font_['overstrike']:
                font_str += ' overstrike'
           
            self.fontVar.set(font_str)


    def bldFrm4Listbox(self):
        self.frm1.grid_columnconfigure(2, weight=1)
        self.frm1.grid_rowconfigure(1, weight=1)
        
        
        self.entryVar = tk.StringVar()
        self.entry = Entry(self.frm1, textvariable = self.entryVar)
        self.entry.grid(row=0, column=0, padx=10)

        self.lbox = Listbox(self.frm1, font = DEFAULTFONT)
        self.lbox.grid(row=1, column=0, rowspan=2, columnspan=4, pady = 10, padx=10, sticky='news')

        items = ['flower', 'pen', 'cup', 'chair', 'envelope', 'valet','coin', 'book', 'paper', 'bottle']
        for i in items:
            self.lbox.insert(END , i)

        self.entry.event_add("<<EntryBoxItem>>", "<KeyRelease-Return>")
        self.entry.bind("<<EntryBoxItem>>", self.addItem)
        
        self.lbox.event_add('<<ListBoxChoose>>', '<KeyRelease-Return>')
        self.lbox.bind('<<ListBoxChoose>>', self.editItem)
        self.lbox.bind('<Double-Button-1>', self.editItem)

        addBtn = Button(self.frm1 , text="Add", command=self.addItem)
        addBtn.grid(row=0, column=1, pady=10)
        
        remBtn = Button(self.frm1 , text="Remove", command=self.removeItem)
        remBtn.grid(row=3, column=0, padx=10, pady=10, sticky=W)

        sortBtn = Button(self.frm1, text = 'Sort items', command = self.sortItems)
        sortBtn.grid(row = 3, column = 2, padx = 10, sticky = 'we')


        self.lbox.bind('<Button -1>', self.setCurrent)
        self.lbox.bind('<B1-Motion >', self.moveSelection)
        
        
    

        def bldRadioButtonFrame():
            frm = tk.Frame(self.frm1, width = 25, height = 25, bg = self.frm1['bg'])
            print(self.frm1['bg'])
            self.rbvar = tk.IntVar()
            rbtnasc = tk.Radiobutton(frm, text = 'Ascending', variable = self.rbvar, value = True) 
            rbtndesc = tk.Radiobutton(frm, text = 'Descending', variable = self.rbvar, value = False)
            rbtnasc.config(bg = self.frm1['bg'], width = 16, padx = 4)
            rbtndesc.config(bg = self.frm1['bg'], width = 16, padx = 3)

            self.rbvar.set(True)
            rbtnasc.pack()
            rbtndesc.pack()
            frm.grid(row = 3, column = 3, sticky = W)

        bldRadioButtonFrame()

      
    def setCurrent(self, e):
        self.lbox.curIndex = self.lbox.nearest(e.y)
        
        
    def moveSelection(self, e):
        i = self.lbox.nearest(e.y)

        if i < self.lbox.curIndex:
            x = self.lbox.get(i)
            self.lbox.delete(i)
            self.lbox.insert(i+1, x)
            self.lbox.curIndex = i

        elif i > self.lbox.curIndex:
            x = self.lbox.get(i)
            self.lbox.delete(i)
            self.lbox.insert(i-1, x)
            self.lbox.curIndex = i

    def sortItems(self):
        temp_list = list(self.lbox.get(0, END))
        sorted_list = sorted(temp_list, reverse = not self.rbvar.get(),
                             key = lambda s : s.lower())
        self.lbox.delete(0, END)
        for item in sorted_list:
            self.lbox.insert(END , item)
   

    def addItem(self, e = None):
        if len(self.idxSelect) > 0:
            self.wasEdit()
            return
        if e:
            w = e.widget
            #print(str(type(w)))
            # split the widget type on all non-word (\W) characters
            s = re.split("\W", str(type(w)))
            
            # start from the last of the list returned by re.split
            i = len(s) -1
            while True:
                if i == -1:
                    break
                # if s[i] contains only alphanumeric characters, break
                # if s[i].isalnum():   not the test I need
                # what was really needed was to test for non-empty string
                if s[i] != '':
                    break
                print(s[i])
                i -= 1

            if i >= 0 and s[i].lower() != 'entry':
                return
        else:
            w = self.entry
        #val = w['textvariable'].value()
        val = self.entryVar.get()
        if (len(val.strip()) == 0):   return

        self.entryVar.set('')
        self.lbox.insert(END , val)
        self.entry.focus_set()

        self.lbox.see(END)


    def wasEdit(self):
        self.lbox.insert(self.idxSelect, self.entryVar.get())
        self.lbox.delete(self.idxSelect[0] +1)
        self.idxSelect = ()
        self.entryVar.set('')
        self.entry.focus_set()


    def editItem(self, e = None):
        self.idxSelect = self.lbox.curselection()
        if (len(self.idxSelect) == 0):      return
        
        s = self.lbox.get(self.idxSelect)
        
        self.entryVar.set(s)
        self.entry.focus_set()
        pass


    def removeItem(self):
        idx = self.lbox.curselection()
        if (len(idx) == 0):      return
        self.lbox.delete(idx , idx)


if __name__ == '__main__':
    win = tk.Tk()
    win.geometry("+900+300")
    win.attributes('-topmost', 1)
    Example(win)
    win.mainloop()



