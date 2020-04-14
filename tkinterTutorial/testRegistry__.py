

import tkinter as tk
from tkinter.ttk import Treeview
import tkinter.ttk as ttk
from tkinter import PanedWindow, Frame, Label, BOTH, VERTICAL, HORIZONTAL, Entry, Scale, Button,\
        Menu, messagebox as MB, DoubleVar, IntVar, StringVar, LEFT, Canvas, OptionMenu, LabelFrame

import sys
import winreg as winreg
from winreg import *
from winregal import *
from winregal import RegKey, RegValue

from PyUtilities  import setColRowWeight
from PyUtilities  import get_widget_attributes
from MyLogging import MyLog
from MyLogging import LoggingHelpers
from GlobalErrorHandling import GlobalErrorHandler, DoDebugPrint

from collections.abc import Iterator, Generator
import os
from MyTkFontChooser import askfont
from tkinter.font import nametofont    

import inspect
from modalDialog import TreeviewUtilities
import re as re
import string
from inspect import currentframe, getframeinfo
from testRegistry_childDlg import RegistryMemoryUseChild

DEBUG = False
FORWARD_SLASH = '/'
ASTERISK = '*'
COLON = ':'
BADCHARS = set("/*:")



def GetScriptAndLine():
    frameinfo = getframeinfo(currentframe())
    return (frameinfo.filename, frameinfo.lineno)

TVUCOLUMNS = {
                0:"Value Name",
                1:"Value Type",
                2:"Value"
             }


roots_hives = {    
    "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
    "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
    "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
    "HKEY_USERS": winreg.HKEY_USERS,
    "HKEY_PERFORMANCE_DATA": winreg.HKEY_PERFORMANCE_DATA,
    "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
    "HKEY_DYN_DATA": winreg.HKEY_DYN_DATA
}



reg_list = (
REG_SZ,
REG_NONE,
REG_MULTI_SZ,
REG_QWORD,
REG_QWORD_LITTLE_ENDIAN,
REG_LINK,
REG_EXPAND_SZ,
REG_DWORD_BIG_ENDIAN,
REG_DWORD_LITTLE_ENDIAN,
REG_DWORD,
REG_BINARY
)


regDtypeDict = {
0:'REG_NONE',
1:'REG_SZ',
2:'REG_EXPAND_SZ',
3:'REG_BINARY',
4:'REG_DWORD',
5:'REG_DWORD_BIG_ENDIAN',
6:'REG_LINK',
7:'REG_MULTI_SZ',
11:'REG_QWORD'
}


REGHIVETXT = 'Registry Hive'
           
            
MYL = None
        
class InitUI(Frame):
 
    def __init__(self, win):
        Canvas.__init__(self, win)

        self.amBltFlag = False                  ## flag to prevent resizing during initialization
        self.filename = ''                      ## variable for filename of registry data
        # what is my (script) name
        scriptname = os.path.basename(__file__)
        
        self.lstUnknown = {}                    ## dictionary for registry "unknowns", usually unicode
                                                ## Created in RecursiveRegistry.recurse and used in bldRegTree
        self.bind("<Configure>", self.on_resize)
       
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

        self.win = win
        self['bg'] = 'blanched almond'

        self.style = ttk.Style()
            
        self.fontVar = tk.StringVar()
        self.fontVar.trace("w", self.check_fontVar)        
        
        self.rootsOfTree = []  # a list to contain the IID of each of the tree roots

        self.hiveSubMenuStringVar = StringVar()
        self.hiveSubMenuStringVar.trace('w', self.onSelectHive)

        self.srchTreeStringVar = StringVar()
        self.srchTreeStringVar.trace('w', self.onSrchTree)

        self.rootsHivesList = list(roots_hives)
            
        self.bldTabNotebook()
        self.bldPanedWindow(self.mainHiveFrame)

        self.memusedlg = None                   # testRegistry_childDlg
        self.bldMenu()
        self.bldStatusBar()
        self.amBltFlag = True
        #self.sashXWas = self.pnWin.sash_coord(0)[0]
        self.pack(fill = 'both', anchor = 'center', expand = True)
        self.origsashposition = self.sashXWas = 350

        return 



    def onSelectHive(self, *args):
        if self.hiveSubMenuStringVar.get() != '':
            #self.sbarBldBtn['state'] = 'normal'
            self.treebldbtn['state'] = 'normal'
        else:
            #self.sbarBldBtn['state'] = 'disable'
            self.treebldbtn['state'] = 'disable'
        

    def onSrchTree(self, *args):

        return


    def bldTabNotebook(self):
        nbFrame = tk.Frame(self)
        nbFrame.pack(fill = 'both', expand=True)

        self.notebook = ttk.Notebook(nbFrame)
        self.notebook.bind("<<NotebookTabChanged>>", self.notebookTabChanged)

        self.mainHiveFrame = tk.Frame()
        self.fileRepeaterFrame = tk.Frame(bg = 'light pink')
        testEnumKeysFrame = tk.Frame()

        self.notebook.add(self.mainHiveFrame, text="Registry Hives")
        self.notebook.add(self.fileRepeaterFrame, text="Hives as File")
        self.notebook.add(testEnumKeysFrame ,text = "Test RegKey.enum_keys")
        self.notebook.pack(pady=5, fill = 'both', expand=True)

        ##self.bldPanedWindow(frame1)

        self.lsBox = tk.Listbox(self.fileRepeaterFrame)
        
        ysb = ttk.Scrollbar(self.fileRepeaterFrame, orient = 'vertical', command = self.lsBox.yview)
        xsb = ttk.Scrollbar(self.fileRepeaterFrame, orient = 'horizontal', command = self.lsBox.xview)
        
        self.lsBox.configure(yscroll=ysb.set, xscroll=xsb.set)
        ysb.pack(side = 'right', fill = 'y', expand = False)
        xsb.pack(side = 'bottom', fill = 'x', expand = False)
        self.lsBox.pack(side = 'left', fill = 'both', expand = True, padx = 4, pady = 4)
        

        self.bldTestEnumKeysFrame(testEnumKeysFrame)
        get_widget_attributes(nbFrame)
        

    def bldTestEnumKeysFrame(self, frm):
        self.lsBoxEnumKeys = tk.Listbox(frm, bg = 'wheat2', fg = 'blue4')
        ysb = ttk.Scrollbar(frm, orient = 'vertical', command = self.lsBoxEnumKeys.yview)
        xsb = ttk.Scrollbar(frm, orient = 'horizontal', command = self.lsBoxEnumKeys.xview)
        self.lsBoxEnumKeys.configure(yscroll=ysb.set, xscroll=xsb.set)
        ysb.grid(row = 0, column = 2, rowspan = 3)
        ysb.columnconfigure(0, weight = 1)
        xsb.grid(row = 2, column = 0, columnspan = 2)
        xsb.rowconfigure(0, weight = 1)
        self.lsBoxEnumKeys.grid(row = 0, column = 0)
        
        
    def bldMenu(self):
        self.menubar = Menu(self.win)
        self.win.config(menu=self.menubar)
        fileMenu = Menu(self.menubar, tearoff=False)
        submenu = Menu(fileMenu , tearoff=False)
        submenu.add_command(label="New feed")
        submenu.add_command(label="Bookmarks")
        submenu.add_command(label="Mail")
        fileMenu.add_cascade(label='Import', menu=submenu , underline =0)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", underline=2, command = self.onExit_)
        self.menubar.add_cascade(label="File", underline=1, menu=fileMenu)

        
        editMenu = Menu(self.menubar, tearoff = False)
        srchTreeCmd = editMenu.add_command(label = 'Search Tree', command = self.searchTree)
        self.win.bind('<Control-F>', self.searchTree)
        self.menubar.add_cascade(label = 'Edit', underline = True, menu = editMenu)


        self.showStat = tk.BooleanVar()
        self.showStat.set(True)
        
        
        def vuMemory():
            RegistryMemoryUseChild(self, IAmAlive = dlgIsAlive)
            
        
        def dlgIsAlive(_dlg):
            """ dlgIsAlive: for threading, the RegistryMemoryUseChild must report 
                that it is initializing before the wait_window loop is begun.
            """
            if _dlg:
                self.memusedlg = _dlg
                _dlg.start()
            else:
                self.memusedlg = None
          

        vuMenu = Menu(self.menubar , tearoff=False)
        vuMenu.add_command(label = "Choose font", command = self.chooseFont)
        vuMenu.add_checkbutton(label="Show statusbar",
                command = self.toggleStatusBar , variable=self.showStat , onvalue=True , offvalue=False)
        vuMenu.add_separator()
        vuMenu.add_command(label = 'View memory used', command = vuMemory)
        self.menubar.add_cascade(label="View", menu=vuMenu)

        
        def bldChooseHiveMenu():
            self.bldMenu = tk.Menu(self.menubar, tearoff = False)
            
            self.hiveSubMenu = Menu(self.bldMenu, tearoff = True)
        
            i = 0
            for item in self.rootsHivesList:
                self.hiveSubMenu.add_radiobutton(label = item, variable = self.hiveSubMenuStringVar)  ##, value = roots_hives[item])
                i += 1
        
            #getHiveBtn = tk.Menubutton(self, text = "Choose registry hive", menu = self.hiveSubMenu, underline = True)
            self.bldMenu.add_cascade(label = "Choose registry hive", menu = self.hiveSubMenu, underline = True)
        
            self.bldMenu.add_cascade(label = 'Build Hive', underline = 1, command = self.bldHive)
            self.win.bind('c', lambda e: edit_btn.event_generate('<<Invoke>>'))

            self.bldMenu.add_separator()
            self.bldMenu.add_cascade(label = 'Clear Tree', underline = 3, command = self.clearTheTree)
            self.bldMenu.add_cascade(label = 'Test enum_keys generator', command = self.testEnumKeys)


        bldChooseHiveMenu()
        self.menubar.add_cascade(label = 'Build', underline = 1, menu = self.bldMenu)
        
        aboutMenu = Menu(self.menubar, tearoff = False)
        self.menubar.add_cascade(label = 'About', underline = 1, menu = aboutMenu)
        

    def onExit_(self):
        if MB.askokcancel("Question", "Are you sure you wish to quit?"):
            if self.memusedlg:
                self.memusedlg.cancel()
            self.destroy()
            self.win.destroy()            

 
        
    def returnFrame(self):
        return Frame(self)

    def testEnumKeys(self):
        if self.hiveSubMenuStringVar.get() == '':
            return
        # set the tabbed self.notebook to the third tab
        i = self.notebook.select(2)
        # delete the listbox contents
        self.lsBoxEnumKeys.delete(0, 'end')
        # get the generator
        # RegKey(
        with RegKey(self.hiveSubMenuStringVar.get()).enum_keys() as key:
            while next(key):
                self.lsBoxEnumKeys.insert('ene')
            return

        return


    def notebookTabChanged(self, event):
        return


    def setNotebookTab(self, *args):
        return


    def getNotebookTab(self, *args):
        return self.tabNdxIntVar.get()


    def onClick(self):
        pass

    def searchTree(self, *args):
        dlg = TreeviewUtilities(self.win)
        dlg.SearchTree(self.hiveTreeview)
     
        self.win.wait_window(dlg.top)
        return


    def bldStatusBar(self):
        self.sbarFrame = Frame(self)
        self.svarready = StringVar()
        self.svarready.set("Ready")
        lblsb = Label(self.sbarFrame , textvariable=self.svarready, relief = 'groove')
        lblsb.pack(side = LEFT, anchor = 'w')

        sep0 = ttk.Separator(self.sbarFrame, orient = 'vertical')
        sep0.pack(side = 'left', anchor = 'w', padx = 15, fill = 'x')


        #sbarBldBtn = Button(self.sbarFrame, text = 'Build', command = self.bldHive)
        #sbarBldBtn['state'] = 'disabled'
        #sbarBldBtn.pack(side = 'left', anchor = 'w')

        self.svarselection = StringVar()
        self.svarselection.set('Selection: ')
        lblselcap = Label(self.sbarFrame, text = 'Selection: ', relief = 'solid')
        lblselcap.pack(side = 'left')

        lblsel = tk.Label(self.sbarFrame, textvariable = self.svarselection, 
                          relief = 'sunken', width = 35)
        lblsel.pack(side = 'left', padx = 3)
        self.sbarFrame.pack(anchor = 'sw', side = 'bottom', fill = 'x', expand = False)
        setColRowWeight(self.sbarFrame)


    def toggleStatusBar(self):
        if (self.showStat.get() == True):
            self.sbarFrame.pack(anchor = 'w', side = 'bottom', fill = 'both', expand = True)
        else:
            self.sbarFrame.pack_forget()


    def on_resize(self,event):
        if not self.amBltFlag:
            return
        if self.width == event.width:
            return
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height

        #msg = "sash coord: [{0}] former Width: [{1}] present Width: [{2}]".format(self.pnWin.sash_coord(0)[0], self.width, event.width)
        #MYL.addlogentry(msg)
        
        self.width = event.width
        self.height = event.height
        
        ##self.scale()
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        #self.scale("all",0,0,wscale,hscale)
        
        
        def adjustSash():
            return
            sashXIs = self.pnWin.sash_coord(0)[0]
            self.sashXWas = self.sashXWas
            if wscale > 1:
                sashXIs += 8
            elif wscale < 1:
                sashXIs -= 8
                      
            self.pnWin.sash_place(0, sashXIs, self.pnWin.sash_coord(0)[1])

            
            self.sashXWas = sashXIs

        adjustSash()

    def LimitPWSize(self, *args):
        self.svarselection.set(self.pnWin.sash_coord(0))

        if self.pnWin.sash_coord(0)[0] >= self.origsashposition:
            return
        
        #self.pnWin.sash_place(0, self.origsashposition, self.pnWin.sash_coord(0)[1])
        #self.pnWin.sash_dragto(0, self.origsashposition, self.pnWin.sash_coord(0)[1])     
   

    def bldPanedWindow(self, parentFrame):
        self.pnWin = PanedWindow(parentFrame)
        self.pnWin.config(bg = 'CadetBlue1', orient = 'horizontal', 
                          sashwidth = 6, sashrelief = 'sunken',
                          relief = 'groove')
        #self.pnWin.paneconfigure('0', sticky = 'news')
        self.pnWin.bind("<B1-Motion>", self.LimitPWSize)
        
        pnTreeWin = LabelFrame(self.pnWin, bg = 'khaki1', text = '')  #'yellow: mainTreeFrame')
        self.bldHiveView(pnTreeWin)
        setColRowWeight(pnTreeWin) ##, colCount = 2, rowCount = 0)

        self.pnWin.paneconfig(pnTreeWin, minsize = 200)
        
        self.pnWin.add(pnTreeWin, stretch = 'always')
        
        valueFrame = Frame(self.pnWin, bd = 5, bg = 'purple1', width = 35)
        self.valueFrameLbl = Label(valueFrame, text = 'hello', relief = 'raised')
        self.valueFrameLbl.pack(side = 'top', fill = 'x', expand = 'false')
        self.pnWin.add(valueFrame, stretch = 'always')
        self.addValueTvu(valueFrame)

        
        self.pnWin.pack(fill = BOTH, anchor = 'center', padx = 4, pady = 4, expand = True)

    
    def addValueTvu(self, frm):
        self.valTvu = Treeview(frm)
        self.valTvu['columns'] = (TVUCOLUMNS[0], TVUCOLUMNS[1], TVUCOLUMNS[2])
        self.valTvu['show'] = ('headings')
        ## Column #0 always refers to the tree column, even 
        
        self.valTvu.column(TVUCOLUMNS[0], width = 100, anchor='center')
        self.valTvu.heading(TVUCOLUMNS[0], text = 'Value Name')
        
        self.valTvu.column(TVUCOLUMNS[1], width = 100, anchor='center')
        self.valTvu.heading(TVUCOLUMNS[1], text = 'Value Type')
        
        self.valTvu.column(TVUCOLUMNS[2], width = 100, anchor='center')
        self.valTvu.heading(TVUCOLUMNS[2], text = 'Value')
        
        self.valTvu.pack(anchor = 'center', fill = BOTH, expand = True)
        

        """
            The values to place in each column for each item can be specified either individually, 
            or by providing a list of values for the item. 
            In the latter case, this is done using the "values" item configuration option 
            (and so can be used either when first inserting the item or later) 
            which takes a list of the values; the order of the list must be the same as the order 
            in the "columns" widget configuration option.

            tree.set('widgets', 'size', '12KB')
            size = tree.set('widgets', 'size')
            tree.insert('', 'end', text='Listbox', values=('15KB Yesterday mark'))
        """


    def bldHiveView(self, pnTreeWin):
        chooseFrame = Frame(pnTreeWin)
        chooseFrame['bg'] = pnTreeWin['bg']
        cbOpt = ttk.Combobox(chooseFrame, textvariable = self.hiveSubMenuStringVar, 
                               justify = 'center', values = self.rootsHivesList)
        cbOpt.configure(state = 'readonly', width = 40)
        cbOpt.grid(row = 0, column = 0, sticky = 'ew', columnspan = 2)
        setColRowWeight(cbOpt, rowCount = 1, col_weight = 1, colCount = 3)
        
        self.treebldbtn = Button(chooseFrame, text = 'Build', command = self.bldHive)
        self.treebldbtn.grid(row = 0, column = 3, padx = 3, sticky = 'e')
        self.treebldbtn['state'] = 'disable'
        
        chooseFrame.grid(sticky = 'new', columnspan = 3)
        setColRowWeight(chooseFrame)

        def buildHiveTvu():
            hiveTreeFrame = LabelFrame(pnTreeWin, bg = 'light cyan')  #, text = 'turquoise')
            lbl = Label(hiveTreeFrame, text = 'hiveTreeFrame')
            lbl.grid(row = 0, column = 0, columnspan = 2, rowspan = 1, sticky = 'new')
            setColRowWeight(lbl,  colCount = 0, rowCount = 0)
      
            self.hiveTreeview = Treeview(hiveTreeFrame, padding = (2,2,2,2))
            self.hiveTreeview.bind('<Double-Button-3>', self.clearTheTree)
            self.hiveTreeview.heading('#0', text = REGHIVETXT, anchor = 'w')
            
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
        

    def bldBase(self):
        titleLbl = tk.Label(self.win, text = sys.argv[0], justify = 'center').pack(fill ='x', expand = True)
        tvu = self.bldTree(self)
        tvu.pack(side = 'left', fill = 'y', expand = True)
        sep = tk.Separator(self, width = 5, orient = 'vertical'). pack(anchor = 'w', expand = False)
        lbox = tk.Listbox(win, width = 50, height = 25)
        lbox.pack(fill = 'both', expand = True, padx = 4, pady = 4)
        return lbox, tvu


    
    def walkTheTree(self):
        self.lsBoxEnumKeys.delete(0, 'end')
        for child in self.hiveTreeview.get_children():
            S = "{0:>60} :: {1}".format(self.hiveTreeview.item(child)["text"], self.hiveTreeview.item(child)["values"])
            self.lsBoxEnumKeys.insert('end', S)
            info = getframeinfo(currentframe())
            DoDebugPrint(S, scriptname = info[0], lineno = info[1], fcnname= info[2])
            DoDebugPrint(child, scriptname = info[0], lineno = info[1], fcnname= info[2])
         
            
    def writeTvuToFile(self, lstOfTuples, testfile = False):
        
        with open(self.filename, 'w+') as tmp:
            for tpl in lstOfTuples:
                name = tpl[0]
                level = tpl[2]
                iter = tpl[1]
                
                try:
                    if name:
                        name = re.sub(f'[^{re.escape(string.printable)}]', '', re.escape(name))
                        if name == '':
                            name = 'strange patternS'
                except:
                    return
                    
                if testfile:    
                    tabString = ''
                    str_ = "{0},{1},{2}\n".format(level, iter, name)
                else:
                    tabString = MYTAB *level
                    str_ = "{0}{1:5}{2:10}{3:<65}\n".format(tabString, level, iter, name)
                try:
                    tmp.write(str_)
                except Exception as exc:
                    info = getframeinfo(currentframe())
                    DoDebugPrint('writeTvuToFile has failed:\niter: [{0}]\n[{1}]'.format(iter, exc.args), 
                                  scriptname = info[0], lineno = info[1], fcnname = info[2])
                    raise

                
            self.lsBox.delete(0, 'end')
            tmp.seek(0)
            lst = tmp.readlines()
            for line in lst:
                self.lsBox.insert('end', line)


    def check_fontVar(self, index, value, op):
        if self.fontVar.get():
            fontString = self.fontVar.get()
            ##self.text['font'] = fontString
            ##self.lblFont['font'] = fontString
            ##self.lblFont['text'] = fontString.replace('\ ', ' ')
            ##for child in self.children.values():
            ##    try:
            ##        child.haschildren()
            ##        child['text'] = fontString
            ##    except:
            ##        continue
            
            self.style.configure("Treeview.Heading", font= fontString)
            self.lsBox['font'] = fontString
            self.lsBoxEnumKeys['font'] = fontString

    def chooseFont(self):
        font_ = askfont(self.win)
        
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


    def clearTheTree(self, event = None):
        for row in self.hiveTreeview.get_children():
            self.hiveTreeview.delete(row)
        self.hiveTreeview.heading('#0', text = REGHIVETXT, anchor = 'w')


    def bldHive(self):
        """  def bldHive uses the RecursiveRegistry generator .send   """
        self.clearTheTree()
        self.filename = './{}.txt'.format(os.getpid())
        
        reg = RecursiveRegistry(self.win, hiveroot = self.hiveSubMenuStringVar.get())
        snd = reg.RecursiveRegistry_yield(0)
        try:
            for iid in self.rootsOfTree:
                self.hiveTreeview.delete(self.hiveTreeview.get_children(iid))
            self.rootsOfTree.clear()
            self.clearTheTree()
            self.hiveTreeview.heading('#0', text = self.hiveSubMenuStringVar.get())
        except:
            pass
        for tpl in snd:
            ##self.writeTvuToFile(tpl, testfile = True)
            self.bldRegTree(tpl)
            ##self.hiveTreeview.update()
            ##self.walkTheTree()
        ##self.hiveTreeview.
    

    def bldRegTree(self, lstOfTuples):
        _hdr = ''
        
        self.style.configure("mystyle.Treeview", highlightthickness=0, bd=0, 
                             bg = 'light pink',  font=('Calibri', 11)) # Modify the font of the body
        childParentId = ''
        lstNodePlacement = []                       # list of tuples. Root is reg root of current run. Nodes are one branch
        rootsOfTree = []
        
        for tpl in lstOfTuples:
            name = tpl[0]
            level = tpl[2]
            iter = tpl[1]
            tabString = MYTAB *level
            
            #info = getframeinfo(currentframe())
            #DoDebugPrint(tabString, name, scriptname = info[0], fcnname = info[2], lineno = info[1])
                    

            ###   what if there is already a -1 element already in the tree??
            if level == 0:
                iid = self.hiveTreeview.insert('', 'end', iter, text = name)
        
                self.hiveTreeview.item(iid, tags = ('bold', 'red'))
                self.rootsOfTree.append(iid)
                lstNodePlacement.append((level, iid))
            elif level > 0:
                """
                    if the current level is greater than the level from the last node of lstNodePlacement,
                    add the new level and the id of the child to the lstNodePlacement
                    A NEW BRANCH
                """
                if level > lstNodePlacement[-1][0]:
                    childId = self.hiveTreeview.insert(lstNodePlacement[-1][1], 'end', iter, text = name, values = tpl)
                    lstNodePlacement.append((level, childId))

                    """
                        BUT, if newitem.level is the <= level from the last node of 
                        lstNodePlacement, we want to add the new node to the parent of the 
                        last node in lstNodePlacement with the level the same as
                        newitem.level
                        SO, we pop() nodes from lstNodePlacement UNTIL level GT[>] the value of the
                        node at the end of lstNodePlacement.
                        ANOTHER BRANCH AT THE SAME LEVEL AS THE LAST.
                        
                    """
                elif level <= lstNodePlacement[-1][0]:              
                    while level <= lstNodePlacement[-1][0]:
                        lstNodePlacement.pop()
                        
                    try:
                        name = re.sub(f'[^{re.escape(string.printable)}]', '', re.escape(name))
                        if name == '':
                            name = 'Possible unicode chars'
                            tpl = (name, tpl[1], tpl[2])
                        childId = self.hiveTreeview.insert(lstNodePlacement[-1][1], 'end', iter, text = name, values = tpl)
                    except:
                        pass
                    lstNodePlacement.append((level, childId))
             
                ## otherwise, that is: the level of the new node is less than or equal to the level of 
                ## that node that was just previously added to the tree, there may be other PREVIOUS nodes 
                ## in the lstNodePlacement that have that same relationship to the new node.
                ## Therefore, remove those nodes.
                
                elif level <= lstNodePlacement[-1][0]:
                    while level <= lstNodePlacement[-1][0]:  ## remove those nodes
                        lstNodePlacement.pop()               ##
                    try:
                        childId = self.hiveTreeview.insert(lstNodePlacement[-1][1], 'end', iter, text = name, values = tpl)
                    except: 
                        name = re.sub(f'[^{re.escape(string.printable)}]', '', re.escape(name))
                        if name is '':
                            name = 'unicode chars: SAB'
                        tpl = (name, tpl[1], tpl[2])
                        childId = self.hiveTreeview.insert(lstNodePlacement[-1][1], 'end', iter, text = name, values = tpl)
                    
                    lstNodePlacement.append((level, childId))

                # at this point, lstNodePlacement has at least 2 nodes IF execution has pass through
                # one of the branches of the above conditional.
                if len(lstNodePlacement) == 1:
                    ##lstNodePlacement.pop()
                    break
                    
                    
                #  insert(parent, index, iid=None, **kw)
                #  Creates a new item and returns the item identifier of the newly created item.

                #  parent is the item ID of the parent item, or the empty string to create a new top-level item. 
                #  index is an integer, or the value �end�, specifying where in the list of parent�s children to insert the new item. 
                #  If index is less than or equal to zero, the new node is inserted at the beginning; 
                #  if index is greater than or equal to the current number of children, it is inserted at the end. 
                #  If iid is specified, it is used as the item identifier; iid must not already exist in the tree. 
                #  Otherwise, a new unique identifier is generated.

                #  See Item Options for the list of available points.
        

MYTAB = ' '*2

KEYLIST = 'klst'
VALLIST = 'vlst'

class getRegDict():
    def __init__(self, *args, **kwargs):
        WR = winregal()
        regdict = WR.to_dict()
        return


class RecursiveRegistry(GlobalErrorHandler):  ##Generator
    def __init__(self, win, **kwargs):
        GlobalErrorHandler(win).__init__(win)
        
        lstUnknown = {}
        self.indentcount = 0
        self._iter = 0
        self.kwargs = kwargs
      
        self.listOfHive = []
        

    @property
    def lstUnknown(self):
        return lstUnknown


    def RecursiveRegistry_yield(self, ignoredArg, filenameUnknown = ''):   ###
        _list = []
        self.getDirList = False
        yield_count = 0
        self.dictUnknowns = {}

        ## getHiveTopLevelsList is probably overkill. RegKey had enum_keys that should do it
        self.keyValLists = self.getHiveTopLevelsList(roots_hives[self.kwargs['hiveroot']])
        #klist = enum_keys()
        if self.keyValLists == {}:
            return
        self.re_ = re.compile(r'\\+')

        if KEYLIST in self.keyValLists:
            self.getDirList = True
            self.listOfHive = []
            negiter = 0  ## negiter is only for identifying the secondary roots of hives
            yield_count = 0
            for node in self.keyValLists[KEYLIST]:
                negiter -= 1
                self.dictUnknowns = {}          ## self.dictUnknowns must be clear on each iteration
                self.listOfHive = []            ## self.listOfHive must be clear on each iteration
                self.listOfHive.append((node, negiter, 0))
                
                # these should be the 0'th nodes
                
                self.dirpath = os.path.join(self.kwargs['hiveroot'], node)
                
                _list = self.recurse(self.dirpath, 0)
                if filenameUnknown > '':
                    self.writeFileOfUnknows(filenameUnknown)
                yield_count += 1
                yield self.listOfHive
        

    def writeFileOfUnknowns(self, filename):
        with open(filename, 'a+b') as file:
            for tpl in self.dictUnknowns:
                file.write(tpl)
                file.write(',')
        pass


    def recurse(self, key_root, ndntcnt):
        ## ndntcnt is the self.indentcount at the time of the call
        ## if ndntcnt == -1, initialize
        ###  RegKey wants a string for the path. NOT AN INTEGER ###
        
        try:
            with RegKey(key_root) as key:        ## key is an iterable of whatever key_root (like HKEY...\something)
                if not self.getDirList:
                    _str = "{0} {1} {2}".format('----', key_root, '-------------')
                    self.printValueOrKey(_str, self._iter)

                ndntcnt += 1
                ##   when should self.indentcount be decremented????
                ##   not to worry, the recursion handles it
            
                for item in key:                        ## then, we iterate over key, the iterable from above
                    '''
                    [RegKey(HKEY_CURRENT_USER\Software\JavaSoft\Prefs\software.aws.toolkits.jetbrains.settings./Default/Aws/Settings)]
                    There is an issue with keys of the above type. In this case 'item' is a RegKey (see below: isinstance(item, RegKey))
                    -and- it passes the other test: newItem = item.enum_values()
                    -BUT-, it pares off the last "Settings" as item.name rather than [software.aws.toolkits.jetbrains.settings./Default/Aws/Settings]
                    which is the true name. 
                    The result is that the recursion key_root is: []
                    SOLVED
                    TODO:
                    []
                    '''
                    self._iter += 1
                    
                    if not self.getDirList and self._iter % 50 == 0: ## DEBUG Item
                        input('any key to continue')                ##

                    if isinstance(item, RegValue): # we're not processing RegValue's NOW
                        if not self.getDirList:
                            self.printValueOrKey(item, self._iter)
                            ###  RegValue's have NO CHILDREN ###
                            ### and no need for recursion
                            ### TODO: decide if self._iter should be decremented
                        continue

                    
                    key_name = item.name
                    if isinstance(item, RegKey) and any((c in BADCHARS) for c in item.path):

                        lst = self.re_.split(item.path)
                        key_name = lst[-1]

                    
                    if isinstance(item, RegKey):
                        if self.getDirList:
                            ##self.listOfHive.append((item.name, self._iter, ndntcnt))
                            self.listOfHive.append((key_name, self._iter, ndntcnt))
                        else:
                            self.printValueOrKey(key_name, self._iter, ndntcnt)
                    
                        _dir = os.path.join(key_root, key_name)
                        '''
                        os.path.join messes up on joining "/×2ÕÉRBÉUÌØÅJÍGCÍJRÁXLÏYYG4"
                        to key_root. os.path.join returns the funny string.
                        '''
                        if len(_dir) < len(key_root):
                            continue
                            
                        ### SINCE THIS IS A RegKey it will, PROBABLY, have children.
                        ### this forces the recursion.
                        ### THEREFORE, this is the only time the recursion is necessary
                        ##if isinstance(_dir, RegKey):

                        self.recurse(_dir, ndntcnt)

                    

                ## after for item in key has exhausted key, quit the recursion
        except Exception as esc:
            _msg = 'the system cannot find the file specified'
            if esc.args[1].lower() == _msg:
                if DEBUG:
                    _msg = 'iter: {}, {}'.format(self._iter, _msg)
                    MYL.addlogentry() 
                pass
            else:
                _msg = '_iter {0}: exception [{1}]\nkey_root: [{2}]'.format(self._iter, esc.args, key_root)
                info = getframeinfo(currentframe())
                DoDebugPrint(_msg, scriptname = info[0], lineno = info[1], fcnname = info[2])
                if DEBUG:
                    MYL.addlogentry(_msg, scriptname = info[0], fcnname = info[2], lineno = info[1]) 
      
    
    def getHiveTopLevelsList(self, root):
        '''
            if the argument is an HKEY..., gathers top level keys into the dictionary, returndict
            Alternately, if a key below a hive root is passed, gathers the keys directly
            below the argument key and any values into the the dictionary, returndict
        '''
        keyList = []
        valList = []
        rrtnDict = {}
        try:
            self.regroot = ConnectRegistry(None, root)
            keycount, valcount, lastmod = QueryInfoKey(self.regroot)

            def buildkeylist():
                i = 0
                while i < keycount:
                    try:
                        sid = EnumKey(self.regroot, i)  ## TODO: EnumValue
                        keyList.append(sid)
                        i += 1
                    except:
                        raise

            if keycount > 0:
                buildkeylist()
            
            def buildvaluelist():
                i = 0
                while i < valcount:
                    try:
                        sid = EnumValue(self.regroot, i) 
                        valList.append(sid)
                        i += 1
                    except:
                        raise

            if valcount > 0:
                buildvaluelist()

            if len(keyList) > 0:
                rrtnDict.update(klst = keyList)
            if len(valList) > 0:
                rrtnDict.update(vlst = valList)

            return rrtnDict
        except Exception as e:
            errstring = "Error: {0}".format(e)
            MB.showinfo('unable to initialize hive root', errstring)
            return {}
        finally:
            CloseKey(self.regroot)
        return {}


    def printValueOrKey(self, toPrn, iter = None, indentCnt = None):
        _2prn = ""
        if iter:
            _2prn = "iter: {0:>3.3}".format(str(iter))
        else:
            _2prn = ' '*9

        if len(_2prn):
            _2prn += MYTAB 

        if  indentCnt:
            string = "ndnt: {0:>3.3}".format(str(indentCnt))
            _2prn += string
        else:
            _2prn += ' '*9
        
        if len(_2prn):
            _2prn += MYTAB

        if isinstance(toPrn, RegValue):
            _2prn += "RegValue: {0:18.18}\t{1:12.12}\t{2:45.45}".\
                format(toPrn.name, regDtypeDict[toPrn.type], str(toPrn.data))
        else:
            if indentCnt:
                _2prn = MYTAB *indentCnt +toPrn
            else:
                _2prn = toPrn
        ##print(MYTAB*indentCnt, _2prn)

        print(_2prn)

if __name__ == '__main__':
    win = tk.Tk()
    x = 1000
    y = 500
    win.geometry('+{0}+{1}'.format(x,y))
    win.attributes('-topmost', 1)
    win.config(bd = 4)
    ttl = os.path.basename(sys.argv[0])
    if DEBUG:
        MYL = MyLog()
    win.title(ttl)
    gui = InitUI(win)
    win.protocol("WM_DELETE_WINDOW", gui.onExit_)
    ##main()
    win.mainloop()

"""    
########### specialCaseTest() is for items that produce false keys #############
                    def isSpecialCaseTest():
                        tstItem = None
                        if  (FORWARD_SLASH in item.path
                                                         or ASTERISK in item.path):
                            # then item.name SHOULD BE everything after the last '\\'
                            lst = self.re_.split(item.path)
                            tstname = lst.pop(-1)  ## this is a string, should be the node name
                            key_name = tstname
                            return True

                            with RegKey(item) as subkey:
                                try:
                                    itemVals = subkey.enum_values()
                                    for val in itemVals:
                                        print(val)
                                    return True
                                except Exception as esc:
                                    try:
                                        itemKeys = subkey.enum_keys()
                                        for val in itemKeys:
                                            print(val)
                                        
                                    except Exception as esc:
                                        info = getframeinfo(currentframe())
                                        DoDebugPrint('_iter {0}: exception [{1}]'.format(_iter, esc.args), 
                                                     scriptname = info[0], lineno = info[1],
                                                     fcnname = info[2])
                        else:
                            return True
                            #-------------------------------------------------------------------------------
                    
                    #if isSpecialCaseTest(): 
"""