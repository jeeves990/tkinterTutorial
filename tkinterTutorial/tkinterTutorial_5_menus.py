# -*- coding: utf -8 -*-
"""
    ZetCode Tkinter e-book
    In this script we create a submenu
    a separator and keyboard shortcuts to menus.
    Author: Jan Bodnar
    Last modified: November 2015
    Website: www.zetcode.com
"""

''' this is all incomplete and buggy  '''
    
from PIL import Image , ImageTk
import tkinter as tk
from tkinter import (Tk, Menu , BooleanVar , StringVar , BOTTOM , X, BOTH , RIDGE,
                        LEFT , TOP , BOTH , FLAT , RAISED)
from  tkinter import messagebox as MB
import tkinter.ttk as ttk
from tkinter.ttk import Frame , Label , Style, Button
from GlobalErrorHandling import GlobalErrorHandler

class Example(tk.Frame):
    def __init__(self , parent):
        tk.Frame.__init__(self , parent)
        GlobalErrorHandler(parent).__init__(masterWindow = parent)
        self.parent = parent
        
        self.configure(background = 'cyan')
        parent.protocol("WM_DELETE_WINDOW", self.onExit)
        self.initUI()
        #self.bldToolBar()
        #self.bldPopupMenu()
        #self.bldNotebook()
       
        self.bldStatusBar()
        self.pack(anchor = 'center', expand = True, fill = BOTH, ipadx = 2, ipady = 2)

    def bldNotebook(self):
        nbFrame = Frame(self)
        nbFrame.pack(fill=BOTH, expand=True)

        notebook = ttk.Notebook(nbFrame)
        frame1 = Frame(width = 50, height = 100)
        frame2 = Frame(width = 50, height = 100)
        frame3 = Frame(width = 50, height = 100)
        notebook.add(frame1 ,text="Tab 1")
        notebook.add(frame2 ,text="Tab 2")
        notebook.add(frame3 ,text="Tab 3")
        notebook.pack(pady=5, fill=BOTH , expand=True)

        self.bldPanedWindow(frame1)

        txt = tk.Text(frame2)
        for i in range(1, 99):
            txt.insert(tk.END, 'hello there, big boy\t')
        txt.pack()
        
        return nbFrame

    
    def bldPanedWindow(self, frm):
        WORDS = "Farewell to our fine feathered friends. For that duck may be somebody's mother"
        pw = tk.PanedWindow(frm, orient = "horizontal", sashwidth = 3)
        frm1 = Frame(width = 50, height = 100)
        lbl1 = tk.Label(frm1 , text="Pane 1")
        lbl1.config(justify = 'center', bg = 'light gray', fg = 'black')
        lbl1.pack(fill = X, expand = True, anchor = 'nw', padx = 16)
     
        
        def bldListBox(self):
            ## INFO: example of correct way to connect scrollbars
            vsbar = tk.Scrollbar(frm1, orient = 'vertical')
            hsbar = tk.Scrollbar(frm1, orient = 'horizontal')
            
            self.lbox = tk.Listbox(frm1, bg = 'light pink', width = 50, height = 30)
            self.lbox.configure(exportselection = 0, yscrollcommand = vsbar.set, xscrollcomman = hsbar.set)
            
            vsbar.configure(command = self.lbox.yview)
            hsbar.configure(command = self.lbox.xview)

            acts = ['Scarlett Johansson', 'Rachel Weiss','Natalie Portman', 'Jessica Alba']
            for i in acts:
                self.lbox.insert('end', i)
        
            self.lbox.event_generate("<<ListboxSelect>>", when = 'tail')
            self.lbox.event_add("<<ListboxSelect>>", "Double-Button-1")
            """      ------------------------------------------------     """
            self.lbox.bind("<<ListboxSelect>>", self.onListboxSelect)
            self.lbox.bind('<Return>', self.onListboxReturn)

            for i in range(1, 50):
                self.lbox.insert(tk.END, str(i) * 25)
            self.lbox.config(selectmode = 'single', highlightbackground='linen', highlightcolor = 'linen')
            vsbar.pack(side = 'right', fill = 'y', expand = True)
            hsbar.pack(side = 'bottom', fill = 'x', expand = True)
            self.lbox.pack(side = 'left', fill = 'y', expand = True, anchor = 'center', padx = 3, pady = 3)

            btnFrm4ListBox = tk.Frame(frm1, bg = 'light pink', height = 3)


        def bldListboxToolbar(self):
            toolbar = Frame(frm1)
            selectionbtn = Button(toolbar, text = 'Get Selection', command = self.btnClick4Selection)
            selectionbtn.pack(side=LEFT , padx=2, pady=2)
            
            selectionCaption = Label(toolbar, text = 'Selection type:')
            selectionCaption.pack(side = 'left', padx = 4)


            def bldSelectionCombobox():
                self.typeStringVar = tk.StringVar()
                self.selTypecbox = ttk.Combobox(toolbar, textvariable = self.typeStringVar) 
            
                ##self.selTypecbox.event_generate("<<ComboboxSelected>>", when = 'tail')
                self.selTypecbox.event_add("<<ComboboxChosen>>", "Double-Button-1")
                self.selTypecbox.bind('<<ComboboxChosen>>', self.setListBoxSelectionType)

                self.selTypecbox['state'] = 'readonly'
                self.selTypecbox['width'] = 10
                self.selTypecbox['justify'] = 'right'
                self.selTypecbox['values'] = ('Single', 'Extended')
                self.selTypecbox.current(0)
            
                self.selTypecbox.pack(side = 'left')

            bldSelectionCombobox()
            toolbar.pack(side = 'bottom' , fill = X)
            

        bldListboxToolbar(self)
        bldListBox(self)

        self.lblselectvar = tk.StringVar() 
        ##self.lblselectvar.set('')
        ##self.lblselectvar.trace_add("write", self.onListboxSelect)

        self.lblselect = tk.Label(frm1, text = '', textvariable = self.lblselectvar)
        self.lblselect.config(justify = 'center', bg = 'linen', fg = 'royal blue', height = 1)
        self.lblselect.pack(fill = X, expand = 0, anchor = 'sw', padx = 16, pady = 3)

        frm2 = Frame(width = 50, height = 100)
        lbl2 = tk.Label(frm2 , text="Pane 2")
        lbl2.config(justify = 'center', bg = 'light gray', fg = 'black')
        lbl2.pack(fill = X, expand = True, anchor = 'nw', padx = 16)
        

        def bldTextBox(frm2):
            txt = tk.Text()

        txt = tk.Text(frm2, width = 50, height = 100, bg = 'cyan')
        for i in range(1, 100):
            txt.insert(tk.END, WORDS)
        
        frm3 = Frame(width = 50, height = 100)
        lbl3 = tk.Label(frm3 , text="Pane 3")
        lbl3.config(justify = 'center', bg = 'light gray', fg = 'black')
        lbl3.pack(fill = X, expand = True, anchor = 'nw', padx = 16)
        
        pw.add(frm1)
        pw.add(frm2)
        pw.add(frm3)
        pw.pack(fill=BOTH, expand=True)


    def setListBoxSelectionType(self, e):
        print('hello from setListBoxSelectionType. THE ACTIVE INDEX IS %d' % e.widget['active'])
        w = e.widget
        self.typeStringVar.set = w.get()
        #s = self.selTypecbox.get()
        #self.lbox['selectionmode'] = 'single'
        pass

    def btnClick4Selection(self,event):

        pass


    def onListboxReturn(self, e = None):
        # get the item selected by the arrow key

        pass

    def onListboxSelect(self, e = None):
        items = self.lbox.curselection()
        s = self.lbox.get(items)
        print(s)
        w = e.widget
        print(type(w))
        print('onListboxSelect: THE ACTIVE INDEX IS %s' % w['active'])
        print('get(ACTIVE) is ', w.get('active'))
        self.lblselectvar.set(s)
        self.svarselection.set(s)
    

    def initUI(self):
        self.parent.title("Submenu")
        self.pack(fill=BOTH , expand=True)

        s = Style()
        s.configure("Statusbar.TLabel", borderwidth=2, relief=RIDGE)
        s.configure("StatusbarSub.TLabel", borderwidth=2, relief=RIDGE, padx = 5)
        s.configure('TFrame', relief=RAISED)
        s.configure('TButton', relief=FLAT)

        self.menubar = Menu(self.parent)
        self.parent.config(menu=self.menubar)
        fileMenu = Menu(self.menubar , tearoff=False)
        submenu = Menu(fileMenu , tearoff=False)
        submenu.add_command(label="New feed")
        submenu.add_command(label="Bookmarks")
        submenu.add_command(label="Mail")
        fileMenu.add_cascade(label='Import', menu=submenu , underline =0)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", underline=0,
        command=self.onExit)
        self.menubar.add_cascade(label="File", underline=0, menu=fileMenu)

        self.showStat = BooleanVar()
        self.showStat.set(True)

        viewMenu = Menu(self.menubar , tearoff=False)
        viewMenu.add_checkbutton(label="Show statusbar",
        command=self.onClick , variable=self.showStat , onvalue=True ,
        offvalue=False)
        self.menubar.add_cascade(label="View", menu=viewMenu)


    def bldToolBar(self):
        toolbar = Frame(self)

        self.img = Image.open("exit.png")
        eimg = ImageTk.PhotoImage(self.img)
        exitButton = Button(toolbar , image=eimg, command=self.onExit)
        exitButton.image = eimg
        exitButton.pack(side=LEFT , padx=2, pady=2)
        toolbar.pack(side=TOP , fill=X)
        self.parent.config(menu=self.menubar)
        self.pack(side = 'top', anchor = 'nw', fill = 'x')


    def bldStatusBar(self):
        self.sbarFrame = Frame(self)
        self.svarready = StringVar()
        self.svarready.set("Ready")
        self.sb = Label(self.sbarFrame , textvariable=self.svarready, style="Statusbar.TLabel")
        self.sb.pack(side = LEFT, anchor = 'w', expand = 0)

        ttk.Separator(self.sbarFrame, orient = 'vertical').pack(side = 'left', anchor = 'w', 
                                                     padx = 15, fill = 'x', expand = 0)


        self.svarselection = StringVar()
        self.svarselection.set('Selection: ')
        lblselcap = Label(self.sbarFrame, text = 'Selection: ', style = "StatusbarSub.TLabel")
        lblselcap.pack(side = 'left')

        lblsel = tk.Label(self.sbarFrame, textvariable = self.svarselection, relief = 'sunken', width = 35)
        lblsel.pack(side = 'left', padx = 3, expand = 1)
        self.sbarFrame.pack(anchor = 'w', side = 'bottom', fill = 'both', expand = 0)


    def onClick(self):
        if (self.showStat.get() == True):
            self.sbarFrame.pack(anchor = 'w', side = 'bottom', fill = 'both', expand = 0)
        else:
            self.sbarFrame.pack_forget()


    def onExit(self):
        self.quit()


    def bldPopupMenu(self):
        self.menu = Menu(self.parent , tearoff=False)
        self.menu.add_command(label="Minimize",
        command=self.doMinimize)
        self.menu.add_command(label="Exit", command=self.onExit)
        self.parent.bind("<Button -3>", self.showMenu)
        self.pack()


    def showMenu(self , e):
        self.menu.post(e.x_root , e.y_root)


    def doMinimize(self):
        self.parent.iconify()

    
    def onExit(self):
        query = MB.askquestion('Quitting?', 'Are you sure you wish to exit the application?', icon = 'warning') == 'yes'
        if  query:
            self.quit()
        else:
            pass


def main():
    root = Tk()
    root.geometry("+300+300")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()


