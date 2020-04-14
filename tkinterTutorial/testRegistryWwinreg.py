# -*- coding: utf-8 -*-
"""
    converting this rendition from using winregal to winreg
"""

import tkinter as tk
from tkinter.ttk import Treeview, Progressbar
import tkinter.ttk as ttk
from tkinter import PanedWindow, Frame, Label, BOTH, VERTICAL, HORIZONTAL, Entry, Scale, Button,\
        Menu, messagebox as MB, DoubleVar, IntVar, StringVar, LEFT, Canvas, OptionMenu, LabelFrame, Text

import sys
from winreg import *

from PyUtilities  import setColRowWeight, get_widget_attributes
from PyUtilities import *
from MyLogging import MyLog
from MyLogging import LoggingHelpers
from GlobalErrorHandling import GlobalErrorHandler, DoDebugPrint
from Exceptions import NoCountError, NoListError

from collections.abc import Iterator, Generator
import os
from MyTkFontChooser import askfont
from tkinter.font import nametofont    

import inspect
from modalDialog import TreeviewSearchUtility
import re as re
import string
from inspect import currentframe, getframeinfo
from ResourceUseProcess_childDlg import RegistryMemoryUseChild
from multiprocessing import Pool, Process, Queue, Pipe
from time import sleep


DEBUG = True
RE_RAISE = False

FORWARD_SLASH = '/'
ASTERISK = '*'
COLON = ':'
BADCHARS = set("/*:")
BACKSLASH = '\\'
REG_KEY_NOTFOUND = 'the system cannot find the file specified'
              
#info = getframeinfo(currentframe()) 
SRC = 0             # fully qualified source filename
LNO = 1             # line number in source file
FCN = 2             # function name in source file

def prn_exception_info(e, errtype, debug_msg):
    try:    print('{}: [{}]\n'.format(errtype, e.errno))
    except:  print('{}: unable to print errno.\n'.format(errtype))
    for s in e.args:
        print(s, '\n')
    print(debug_msg, '\n\n\n')
                

TVUCOLUMNS = {
                0:"Value Name",
                1:"Value Type",
                2:"Value"
             }

REGHIVETXT = 'Registry Hive'
           
            
MYL = None
parent_conn, child_conn = Pipe()
YouMayResize = False
TK_ALIAS = None                 # an alias for the Tk object
DEBUGFILENAME = './{}.txt'.format(os.getpid())
TVU4REGKEYS = None
CHOOSE_REG_KEY_VAR = None
STATUS_BAR_FRAME = None


##############################################################
# following are aliases of StringVar's for status bar updating
#
ITERANNUNVAR = None
READY_VAR = None
ITEM_PATH = None
ITEM_CAP = None
##############################################################


def callMemUseChild(conn):
    self.reg = RegistryMemoryUseChild(self, IAmAlive = dlgIsAlive, conn = conn, parent_pid = os.getpid() )

class MemoryUsageChild(RegistryMemoryUseChild):
    def __init__(self, parent):
        RegistryMemoryUseChild.__init__(self, parent)
        self._p = Process(target = callMemUseChild(child_conn))
        #self.p.start()
        # Some time later ...
        print('PID is ' + str(self.p.pid))
        print(parent_conn.recv())
        #reg = RegistryMemoryUseChild(self, IAmAlive = dlgIsAlive)
            
        @property
        def memoryUsageDlg(self):
            return self

        @memoryUsageDlg.deleter
        def memoryUsageDlg(self):
            del self


class InitUI(Canvas):
 
    def __init__(self, tKparent):
        Canvas.__init__(self, tKparent)

        YouMayResize = False                  ## flag to prevent resizing during initialization
        # what is my (script) name
        scriptname = os.path.basename(__file__)
        
        self.lstUnknown = {}                    ## dictionary for registry "unknowns", usually unicode
                                                ## Created in RecursiveRegistry.recurse and used in bldRegTree
        self.tKparent = tKparent
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

        self['bg'] = 'blanched almond'
        
        self.style = ttk.Style()
        self.bind('<Configure>', self.ctrlSize)
        self.rootsOfTree = []   # a list to contain the IID of each of the tree roots
                                # list is built as the Treeview is built

        self.srchTreeStringVar = StringVar()
        ##self.srchTreeStringVar.trace('w', self.onSrchTree)

        bldNBKFrame = BldTabNotebookFrame(self)
        bldNBKFrame.pack(fill = 'both', expand = 'yes')

        self.pnWin = BldPanedWindow(bldNBKFrame.mainHiveFrame)
        self.pnWin.pack(fill = 'both', expand = True)
        #self.win.bind("<Button-1>", self.on_button_1_down)

        ui = self
        self.menu = Main_menu(self, self.tKparent)
        self.tKparent.configure(menu = self.menu)

        self.frm_sbar = Frame_StatusBar(self)
        self.frm_sbar.pack(anchor = 'sw', side = 'bottom', fill = 'x', expand = False)
        
        self.pack(fill = 'both', anchor = 'center', expand = True)
        self.tKparent.originalHeight = int(tKparent['height'])
        self.tKparent.originalWidth = int(tKparent['width'])

        sbarStr = 'Original::Width [{}], Height [{}]'.format(tKparent['width'], tKparent['height'])
        self.frm_sbar.sel1_StrVar.set(sbarStr)
        self.frm_sbar.establishOriginalDimensions()
        YouMayResize = True

        return 


    @staticmethod
    def _cancel():
        if MB.askokcancel("Question", "Are you sure you wish to quit?"):
            try:
                if MemoryUsageChild.memoryUsageDlg:
                    del MemoryUsageChild.memoryUsageDlg    ###
            except:
                pass
            sys.exit(0)

    def ctrlSize(self, *args):
        if int(self.tKparent['height']) <= self.tKparent.originalHeight:
           self.tKparent['height'] =  self.tKparent.originalHeight
        if int(self.tKparent['width']) <=  self.tKparent.originalWidth:
            self.tKparent['width'] =  self.tKparent.originalWidth

        sbarStr = 'Width [{}]. Height [{}]'.format(self.tKparent['width'], self.tKparent['height'])
        self.frm_sbar.selection_StrVar.set(sbarStr)

   
class FontUtility:
    def __init__(self, **kwargs):    # master, master_parent):
        self._fontVar = StringVar()
        self._fontVar.trace("w", self.fontvar)                

        pass
    
    def fontvar(self, *args):
        if _fontVar.get():
            fontString = _fontVar.get()
            self.style.configure("Treeview.Heading", font = fontString)
            self.lsBox['font'] = fontString
            EnumKeysFrame3.lsBoxEnumKeys['font'] = fontString
            Frame_4_RegKeys["font"] = fontString


    def change_fontvar(self):
        _font = askfont()
        if _font:
            self._fontVar.set('')
            # spaces in the family name need to be escaped
            _font['family'] = _font['family'].replace(' ', '\ ')
            font_str = "%(family)s %(size)i %(weight)s %(slant)s" % _font
            if _font['underline']:
                font_str += ' underline'
            if _font['overstrike']:
                font_str += ' overstrike'
           
            self._fontVar.set(font_str)

    
class Main_menu(Menu):
    """ main menu and sundry 
        uiParent is the Frame which contains the Main_menu
        tKparent is the tkinter tk object which owns the Main_menu
    """
    def __init__(self, uiParent, tKparent = None):
        Menu.__init__(self, uiParent)
        self.ui_parent = uiParent
        self.tk_parent = tKparent

        self.add_cascade(label = 'File', underline = 1, menu = self.TheFileMenu(self.tk_parent))

        editMenu = Menu(self, tearoff = False)
        editMenu.add_command(label = 'Search Tree', command =  self.srchRegKeyTree)
        editMenu.add_separator()
        editMenu.add_command(label = "Choose font", command = FontUtility().change_fontvar)

        self.add_cascade(label = 'Edit', underline = True, menu = editMenu)
        
        self.showStat = tk.BooleanVar()
        self.showStat.trace('w', self.toggleShowStatusBar)

        self.add_cascade(label = 'View', underline = 1, menu = self.TheViewMenu(tKparent, self))

        self.add_cascade(label = 'Build', underline = 1, menu = self.TheBuildMenu(tKparent))
        
        aboutMenu = Menu(self, tearoff = False)
        aboutMenu.add_cascade(label="Process Id: [{}]".format(os.getpid()) )
        self.add_cascade(label = 'About', underline = 1, menu = aboutMenu)
            

    class TheFileMenu(Menu):
        def __init__(self, tKparent):
            Menu.__init__(self, tKparent)
            self.configure(tearoff=False)

            submenu = Menu(self , tearoff=False)
            submenu.add_command(label="New feed")
            submenu.add_command(label="Bookmarks")
            submenu.add_command(label="Mail")
            self.add_cascade(label='Import', menu=submenu , underline =0)
            self.add_separator()
            self.add_cascade(label="Exit", underline=2, command = InitUI._cancel)

    class TheViewMenu(Menu):
        def __init__(self, tKparent, parent):
            Menu.__init__(self, tKparent)
            self.configure(tearoff=False)
            
            
            self.add_checkbutton(label="Show statusbar", variable = parent.showStat , onvalue=True , offvalue=False)
            self.add_separator()
            self.add_cascade(label = 'View memory used')

    class TheBuildMenu(Menu):
        def __init__(self, tKparent):
            Menu.__init__(self, tKparent)
            self.configure(tearoff = False)
            
            chooseRegKeyMenu = Menu(self, tearoff = True)
            i = 0
            for item in HivesList:
                chooseRegKeyMenu.add_radiobutton(label = item, variable = CHOOSE_REG_KEY_VAR)
                i += 1

            self.add_cascade(label = "Choose RegKey", menu = chooseRegKeyMenu, underline = 1)
            self.add_cascade(label = 'Build Registry Tree', underline = 1, command = Frame_4_RegKeysContainer.bldRegKeyTree)
            tKparent.bind('c', lambda e : edit_btn.event_generate('<<Invoke>>', when = 'tail'))
            self.add_separator()
            self.add_cascade(label = 'Clear RegKey Tree', underline = 3, command = Treeview_4_RegKeys.clearRegKeys)
            self.add_cascade(label = 'Test enum_keys generator', command = NoteBookUtilities.testEnumKeys())

       
    def toggleShowStatusBar(self, *args):
        self.ui_parent.frm_sbar.toggleStatusBar()
         
    def returnFrame(self):
        return Frame(self)

    def srchRegKeyTree(self):
        if not self.tKparent:
            raise ValueError("Main_menu.srchRegKeyTree (@staticmethod): self.tKparent is not instantiated.")
        dlg = TreeviewUtilities(self.tKparent)
        dlg.SearchTree(Treeview_4_RegKeys.tvu_4_roots)
        self.win.wait_window(dlg.top)
        return


    def setNotebookTab(self, *args):
        return


    def getNotebookTab(self, *args):
        return self.tabNdxIntVar.get()


    def onClick(self):
        pass

    
    def bldBase(self):
        titleLbl = tk.Label(self.win, text = sys.argv[0], justify = 'center').pack(fill ='x', expand = True)
        tvu = self.bldTree(self)
        tvu.pack(side = 'left', fill = 'y', expand = True)
        sep = tk.Separator(self, width = 5, orient = 'vertical'). pack(anchor = 'w', expand = False)
        lbox = tk.Listbox(win, width = 50, height = 25)
        lbox.pack(fill = 'both', expand = True, padx = 4, pady = 4)
        return lbox, tvu


    
    def writeTvuToFile(self, lstOfTuples, testfile = False):
        filename = DEBUGFILENAME + 'tuples'
        with open(filename, 'w+') as tmp:
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


class NoteBookUtilities():
    def __init__(self, master):
        pass

    @staticmethod                
    def testEnumKeys():
        """
            # set the tabbed self.notebook to the THIRD tab
            # delete the listbox contents
            # build a representation of the keys
        """
        if CHOOSE_REG_KEY_VAR.get() == '':
            return
        i = self.notebook.select(2)
        EnumKeysFrame3.lsBoxEnumKeys.delete(0, 'end')
        with RegKey(self.hiveSubMenuStringVar.get()).enum_keys() as key:
            while next(key):
                EnumKeysFrame3.lsBoxEnumKeys.insert('ene')
        return


class BldTabNotebookFrame(Frame):
    """ contains three pages: self._mainHiveFrame, fileRepeaterFrame & EnumKeysFrame """
    def __init__(self, parent):
        Frame.__init__(self, parent)
        

        ##lbl = Label(self).pack()

        self.nbk = ttk.Notebook(self)
        self.nbk.bind("<<NotebookTabChanged>>", self.notebookTabChanged)

        self._mainHiveFrame = tk.Frame(bg = 'spring green')
        fileRepeaterFrame = tk.Frame(bg = 'light pink')
        enumKeysFrame = EnumKeysFrame3(self)

        self.nbk.add(self._mainHiveFrame, text = "Registry Hives")
        self.nbk.add(fileRepeaterFrame, text = "Hives as File")
        self.nbk.add(enumKeysFrame, text = "Test RegKey.enum_keys", sticky = 'news')
        self.nbk.pack(pady=5, fill = 'both', expand=True)

        self.lsBox = tk.Listbox(fileRepeaterFrame)
        
        ysb = ttk.Scrollbar(fileRepeaterFrame, orient = 'vertical', command = self.lsBox.yview)
        xsb = ttk.Scrollbar(fileRepeaterFrame, orient = 'horizontal', command = self.lsBox.xview)
        
        self.lsBox.configure(yscroll=ysb.set, xscroll=xsb.set)
        ysb.pack(side = 'right', fill = 'y', expand = False)
        xsb.pack(side = 'bottom', fill = 'x', expand = False)
        self.lsBox.pack(side = 'left', fill = 'both', expand = True, padx = 4, pady = 4)
        
        get_widget_attributes(self)
        
    @property
    def notebook(self):
        return self.nbk
    
    @property
    def mainHiveFrame(self):
        return self._mainHiveFrame


    def notebookTabChanged(self, event):
        return

class EnumKeysFrame3(Frame):
    ''' populates EnumKeysFrame the third child of TabbedNotebook '''
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self._lsBoxEnumKeys = tk.Listbox(self, bg = 'black', fg = 'blue4')

        ysb = ttk.Scrollbar(self, orient = 'vertical', command = self._lsBoxEnumKeys.yview)
        xsb = ttk.Scrollbar(self, orient = 'horizontal', command = self._lsBoxEnumKeys.xview)
        self._lsBoxEnumKeys.configure(yscroll=ysb.set, xscroll=xsb.set)
        
        ysb.grid(row = 0, column = 2, rowspan = 3)
        ysb.columnconfigure(0, weight = 1)
        xsb.grid(row = 2, column = 0, columnspan = 2)
        
        xsb.rowconfigure(0, weight = 1)
        self._lsBoxEnumKeys.grid(row = 0, column = 0)

    @staticmethod
    @property
    def lsBoxEnumKeys(self):
        return self._lsBoxEnumKeys
    

class BldPanedWindow(PanedWindow):
    """ has two panes oriented horizontally: frm_4_RegKeys and frm_4_RegValues   """
    def __init__(self, parent):
        PanedWindow.__init__(self, parent)
        self.configure(bg = 'CadetBlue1', orient = 'horizontal', 
                          sashwidth = 6, sashrelief = 'sunken',
                          relief = 'groove')
        #self.bind("<B1-Motion>", self.LimitPWSize)
        
        frm_4_RegValues = self.Frame_4_RegValues(None)
        frm_4_RegKeyContainer = Frame_4_RegKeysContainer(self)
        setColRowWeight(frm_4_RegKeyContainer)

        self.paneconfigure(frm_4_RegKeyContainer, sticky = 'news', minsize = 300)  
        self.paneconfigure(frm_4_RegValues, sticky = 'news', after = frm_4_RegKeyContainer, minsize = 300)  
      

    #property
    #def hiveSubMenuStrVar(self):
    #    return  self.StrVar_4_Reg_Roots

    #@staticmethod
    
    #def hive_submenu_strvar_value():
    #    return self.StrVar_4_Reg_Roots.get()

    
    class Frame_4_RegValues(Frame):
        """   contains the columnar Treeview for RegValue's   """
        def __init__(self, parent):
            Frame.__init__(self, parent)
            self.configure(bd = 5, bg = 'purple1', width = 303)
            lbl = Label(self, text = "hello, I'm the values frame", relief = 'raised')
            lbl.pack(side = 'top', fill = 'x', expand = 'false')
            self.addValueTvu = self.AdValTvu(self)
    

        class AdValTvu(Treeview):
            def __init__(self, parent):
                Treeview.__init__(self, parent)
                        # The values to place in each column for each item can be specified either individually, 
                        # or by providing a list of values for the item. 
                        # In the latter case, this is done using the "values" item configuration option 
                        # (and so can be used either when first inserting the item or later) 
                        # which takes a list of the values; the order of the list must be the same as the order 
                        # in the "columns" widget configuration option.

                        # tree.set('widgets', 'size', '12KB')
                        # size = tree.set('widgets', 'size')
                        # tree.insert('', 'end', text='Listbox', values=('15KB Yesterday mark'))
                self['columns'] = (TVUCOLUMNS[0], TVUCOLUMNS[1], TVUCOLUMNS[2])
                self['show'] = ('headings')
                ## Column #0 always refers to the tree column, even 
        
                self.column(TVUCOLUMNS[0], width = 100, anchor='center')
                self.heading(TVUCOLUMNS[0], text = 'Value Name')
        
                self.column(TVUCOLUMNS[1], width = 100, anchor='center')
                self.heading(TVUCOLUMNS[1], text = 'Value Type')
        
                self.column(TVUCOLUMNS[2], width = 100, anchor='center')
                self.heading(TVUCOLUMNS[2], text = 'Value')
        
                self.pack(anchor = 'center', fill = BOTH, expand = True)
            
   
    @property  
    def hiveSubMenuStrVar(self):
        return self.StrVar_4_Reg_Roots
    
    
class Frame_4_RegKeysContainer(LabelFrame):
    """  contains two elements: Frame_4_RegKey_choice <above>::has  Combobox and Build button
                        -and-   Frame_4_RegKeys <below>
    """
    def __init__(self, parent):
        LabelFrame.__init__(self, parent)
        self.configure(bg = 'light cyan', text = '')

        frm_4_RegKey_choice = Frame_4_RegKey_choice(self)
        frm_4_RegKeys = Frame_4_RegKeys(self)
        setColRowWeight(frm_4_RegKey_choice)
        setColRowWeight(self)

        frm_4_RegKey_choice.pack(side = 'top', fill = 'x', expand = False, anchor = 'w')
        frm_4_RegKeys.pack(side = 'top', fill = 'both', expand = True, anchor = 'w')


    @staticmethod
    def bldRegKeyTree():
        if not CHOOSE_REG_KEY_VAR.get():
            MB.showinfo('No Registry Key chosen', 'Please choose a registry key from the list')
            return
        BuildRegKeyTree().buildRegKeyTree(CHOOSE_REG_KEY_VAR.get())
        return
    

class Frame_4_RegKey_choice(LabelFrame):
    def __init__(self, parent):
        LabelFrame.__init__(self, parent)
        self['text'] = ''
        self['bg'] = parent['bg']

        self.parent = parent
        cbOpt = ttk.Combobox(self, textvariable = CHOOSE_REG_KEY_VAR,  justify = 'center', values = HivesList)
        cbOpt.configure(state = 'readonly', width = 40)
        cbOpt.grid(row = 0, column = 0, sticky = 'ew', columnspan = 2)
        setColRowWeight(cbOpt, rowCount = 1, col_weight = 1, colCount = 3)
            
        self.treebldbtn = Button(self, text = 'Build', command = Frame_4_RegKeysContainer.bldRegKeyTree)
        setColRowWeight(cbOpt)
        self.treebldbtn.grid(row = 0, column = 3, padx = 3, sticky = 'e')
        self.treebldbtn['state'] = 'disable'
        
        CHOOSE_REG_KEY_VAR.trace('w', self.onChooseRegKey)
        
    
    def onChooseRegKey(self, *args):
        if CHOOSE_REG_KEY_VAR.get() != '':            
            self.treebldbtn['state'] = 'normal'
        else:            
            self.treebldbtn['state'] = 'disable'


class Frame_4_RegKeys(LabelFrame):
    """
        contains tvu_4_RegKeyHive and two Scrollbars
    """
    def __init__(self, parent):
        LabelFrame.__init__(self, parent)
        self.config(bd = 2, bg = 'light pink', text = '')
        self.tvu_4_RegKeys = tvu_4_RegKeys = Treeview_4_RegKeys(self)
        
        minwd = 300
        tvu_4_RegKeys.column("#0", width = minwd, stretch=True, minwidth = minwd)

        ysb = tk.Scrollbar(self, orient='vertical', command= tvu_4_RegKeys.yview)
        ysb.config(activebackground = 'firebrick1', width = 12)
        xsb = tk.Scrollbar(self, orient='horizontal', command = tvu_4_RegKeys.xview)
        xsb.config(activebackground = 'firebrick1')
        tvu_4_RegKeys.configure(yscroll=ysb.set, xscroll=xsb.set)

        self.grid_columnconfigure(0, minsize = minwd, weight = 1)
        self.grid_columnconfigure(1, minsize = int(ysb['width']), weight = 1)
        
        ysb.grid(row = 0, column = 1, sticky = 'nse')
        xsb.grid(row = 1, column = 0, sticky = 'swe')
        setColRowWeight(tvu_4_RegKeys)
        tvu_4_RegKeys.grid(row = 0, column = 0, sticky = 'news', columnspan = 1, rowspan = 1)
        
        setColRowWeight(ysb)
        setColRowWeight(xsb)
        colcount, rowcount = self.grid_size()
        #setColRowWeight(self, rowCount = rowcount, colCount = colcount)
        self.grid_rowconfigure(0, minsize = 100, weight = 1)
        self.grid_rowconfigure(1, minsize = int(xsb['width']), weight = 1)
        
        self.grid_columnconfigure(0, minsize = 100, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        #for i in range(colcount):
        #    lbl = Label(self, text = 'Col: [{}]'. format(i))
        #    lbl.grid(row = rowcount, column = i, columnspan = 1, sticky = 'swe')


class Frame_StatusBar(LabelFrame):
    def __init__(self, parent):
        LabelFrame.__init__(self, parent)
        
        self.parent = parent
        TK_ALIAS.bind('<Configure>', self.resizeStatusBar)
        global READY_VAR
        READY_VAR = ready_StrVar = StringVar()
        ready_StrVar.set("Ready")
        lblops = Label(self , textvariable = ready_StrVar, relief = 'groove')
        lblops.pack(side = LEFT, anchor = 'w')

        #sep0 = ttk.Separator(self, orient = 'vertical')
        #sep0.pack(side = 'left', anchor = 'w', padx = 2, fill = 'x')

        global ITEM_CAP
        ITEM_CAP = self.selection_StrVar = StringVar()
        self.selection_StrVar.set('Selection:')
        lblselcaption = Label(self, text = '', relief = 'solid')
        lblselcaption.pack(side = 'left')

        global ITEM_PATH
        ITEM_PATH = StringVar()
        self.lbl_item_path = tk.Label(self, textvariable = ITEM_PATH, width = 85)
        self.lbl_item_path.pack(side = 'left', padx = 3, expand = True)

        global ITERANNUNVAR
        ITERANNUNVAR = self.sel1_StrVar = StringVar()
        lblsel1 = Label(self, textvariable = self.sel1_StrVar, relief = 'groove', width = 12)
        lblsel1.pack(side = 'left', padx = 5)
        setColRowWeight(self)
        self.progBar = Progressbar(self, mode = "indeterminate", length = self['width'] - 10)
        GLOBAL_update_idletasks()

        global STATUS_BAR_FRAME
        STATUS_BAR_FRAME = self
       

    def show_progressbar(self):
        self.progBar.pack(anchor = 'w', side = 'bottom', fill = 'both', expand = True)


    def hide_progressbar(self):
        self.progBar.pack_forget()

    
    def establishOriginalDimensions(self):
        self.original_size = self.winfo_reqwidth()
        self.item_path_original_size = self.lbl_item_path.winfo_reqwidth()
        pass

    def resizeStatusBar(self, *args):
        if not YouMayResize:
            return
        proportion = self['width'] / self.original_size
        self.lbl_item_path['width'] = int(self.original_size * proportion)
    
    
    def toggleStatusBar(self):
        if self.parent.menu.showStat.get():
            self.pack(anchor = 'w', side = 'bottom', fill = 'both', expand = True)
        else:
            self.pack_forget()


class BuildRegKeyTree():
    """  class BuildRegKeyTree uses the RecursiveRegistry generator .send   """
    def __init__(self, *args, **kwargs):
        pass
        

    def buildRegKeyTree(self, regkey = None):
        
        Treeview_4_RegKeys.clearRegKeys()
        if not regkey:
            regkey = CHOOSE_REG_KEY_VAR.get()
            if regkey == '':
                return
            
        reg = RecursiveRegistry(hiveroot = regkey)
        
        global TK_ALIAS
        global TVU4REGKEYS
        global GLOBAL_update_idletasks
        snd = reg.RecursiveRegistry_yield(0)
        try:
            #self.rootsOfTree.clear()
            TVU4REGKEYS.clearRegKeys
            GLOBAL_update_idletasks
            
            
        except Exception as e:
            for x in e.args:
                print(x)
            pass
        for tpl in snd:
            ##self.writeTvuToFile(tpl, testfile = True)
            self.bldRegTree(tpl)
            ##self.hiveTreeview.update()
            ##self.walkTheTree()
            GLOBAL_update_idletasks(10)
            

    def bldRegTree(self, lstOfTuples):
        _hdr = ''
        global TVU4REGKEYS

        if not TVU4REGKEYS:
            raise ValueError('Treeview not set')
            
        #TVU4REGKEYS.style.configure("mystyle.Treeview", highlightthickness=0, bd=0, 
        #                     bg = 'light pink',  font=('Calibri', 11)) # Modify the font of the body
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
                iid = TVU4REGKEYS.insert('', 'end', iter, text = name)
        
                TVU4REGKEYS.item(iid, tags = ('bold', 'red'))
                rootsOfTree.append(iid)
                lstNodePlacement.append((level, iid))
            elif level > 0:
                """
                    if the current level is greater than the level from the last node of lstNodePlacement,
                    add the new level and the id of the child to the lstNodePlacement
                    A NEW BRANCH
                """
                if level > lstNodePlacement[-1][0]:
                    childId = TVU4REGKEYS.insert(lstNodePlacement[-1][1], 'end', iter, text = name, values = tpl)
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
                        childId = TVU4REGKEYS.insert(lstNodePlacement[-1][1], 'end', iter, text = name, values = tpl)
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
                        childId = TVU4REGKEYS.insert(lstNodePlacement[-1][1], 'end', iter, text = name, values = tpl)
                    except: 
                        name = re.sub(f'[^{re.escape(string.printable)}]', '', re.escape(name))
                        if name is '':
                            name = 'unicode chars: SAB'
                        tpl = (name, tpl[1], tpl[2])
                        childId = TVU4REGKEYS.insert(lstNodePlacement[-1][1], 'end', iter, text = name, values = tpl)
                    
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
 
                
class Treeview_4_RegKeys(Treeview):
    def __init__(self, parent):
        Treeview.__init__(self, parent)
        self.configure(padding = (2,2,2,2))
        self.bind('<Double-Button-3>', self.clearRegKeys)
        self.heading('#0', text = REGHIVETXT, anchor = 'w')
        global TVU4REGKEYS
        TVU4REGKEYS = self

    def tvu4RegKeys(self):
        return self
    
    def clearRegKeys(self = 0):
        if not TVU4REGKEYS:
            if YouMayResize: 
                MB.showinfo('Nothing to do', 'TVU4REGKEYS is unbuilt')
            return
        clear_iter = 0
        global READY_VAR
        READY_VAR.set('Clearing Treeview')
        try:
            def clearTheChildren(itemNo = 0):
                for i in TVU4REGKEYS.get_children(itemNo):
                    try:
                        clearTheChildren(i)
                        #if TVU4REGKEYS(i).exists:
                        #print(TVU4REGKEYS.item(i)['text'])
                        TVU4REGKEYS.delete(i)
                        clear_iter += 1
                        if clear_iter % 100:
                            global ITERANNUNVAR
                            ITERANNUNVAR.set(str(clear_iter))
                            global GLOBAL_update_idletasks
                            GLOBAL_update_idletasks(2)                 
                    except:
                        continue
            clearTheChildren(0)
        finally:
            TVU4REGKEYS.heading('#0', text = REGHIVETXT, anchor = 'w')
            READY_VAR.set('Ready')


    def populateTreeview_with_RegKeys(self):



        pass


MYTAB = ' '*2

KEYLIST = 'klst'
VALLIST = 'vlst'

class getRegDict():
    def __init__(self, *args, **kwargs):
        WR = winregal()
        regdict = WR.to_dict()
        return

class RecursiveRegistry(GlobalErrorHandler):  ##Generator
    def __init__(self, **kwargs):
        GlobalErrorHandler(TK_ALIAS).__init__(TK_ALIAS)
        
        lstUnknown = {}
        self.indentcount = 0
        self.output_iter = 0
        self.kwargs = kwargs
        self.listOfHive = []
        
        global CHOOSE_REG_KEY_VAR
        self.regRootName = CHOOSE_REG_KEY_VAR.get()
        TVU4REGKEYS.heading('#0', text = CHOOSE_REG_KEY_VAR.get(), anchor = 'w')
        if MYL:
            MYL.addRegistryLogentry(CHOOSE_REG_KEY_VAR.get() + '\n')
        global GLOBAL_update_idletasks
        GLOBAL_update_idletasks(WAITFOR = 15)
        self.rootOfHiveIntAlias = roots_of_hives[self.regRootName]

        """ ConnectRegistry: Establishes connection to a predefined registry handle on 
            ANOTHER COMPUTER, and returns a handle object.
            The first argument is the name of the remote computer, of the form r"\\computername". 
            If None, the local computer is used.
            The second argument is the predefined handle to connect to.
        """
        self.HKEYRootHandle = ConnectRegistry(None, self.rootOfHiveIntAlias)
        """ I puzzled with where to close this handle but, since it will be needed throughout the use
            of the RecursiveRegistry class, I have decided to let the garbage collector take care of it.
        """

        self.regRootNameLen = len(self.regRootName)
    
        
    def lstUnknown(self):
        return lstUnknown


    def RecursiveRegistry_yield(self, ignoredArg, filenameUnknown = '', **kwargs):   ###
        
        _list = []
        self.getDirList = False
        yield_count = 0
        cnt_ = -1
        
        try:
            READY_VAR.set('Mapping Registry')
            nolisterr = False
            info = getframeinfo(currentframe())         # source information for debug
                
                #
                # listOfKeys_ is the unadorned list of immediate key children to self.HKEYHandle
                #
            listOfKeys_, cnt_ = self.getListOfKeys4Key(self.HKEYRootHandle)  
            
            if cnt_ == 0:
                info = getframeinfo(currentframe())         # source information for debug
                debug_msg = '{} {}'. format('No list of children keys was found for ', self.regRootName)
                debug_msg += '\n {} -> {}'.format(info[0], info[2]) 
                raise NoListError(debug_msg)
                
            listOfKeysSorted = sorted(listOfKeys_[KEYLIST], key = str.lower)
            info = getframeinfo(currentframe())         # source information for debug
            self.getDirList = True
            self.listOfHive = []
            negiter = 0  ## negiter is only for identifying the secondary roots of hives
            yield_count = 0
            info = getframeinfo(currentframe())         # source information for debug
            for node in listOfKeysSorted:
                negiter -= 1
                #self.dictUnknowns = {}             ## self.dictUnknowns must be clear on each iteration

                # self.listOfHive is the list of tuples representing the children, grandchildren, ...
                # of self.regRootName : self.rootOfHiveIntAlias
                self.listOfHive = []                ## self.listOfHive must be clear on each iteration
                self.listOfHive.append((node, negiter, 0))
                try:
                    self.dirpath, self.parent_key_name, HKEYName = My_reg_PathJoin(self.kwargs['hiveroot'], node)
                except PermissionError as e:
                    continue

                # on the first pass, the value of the HKEY_... is what we want to open
                HKEYHandle_ = OpenKey(self.rootOfHiveIntAlias, self.parent_key_name, reserved = 0, access = KEY_READ)
                info = getframeinfo(currentframe())         # source information for debug
                
                self.recurse(HKEYHandle_, 0, self.parent_key_name)

                yield_count += 1
                yield self.listOfHive
                
                global GLOBAL_update_idletasks
                GLOBAL_update_idletasks(10)
                #TVU4REGKEYS.item(node, open = True)
                #input('click Enter to continue')
                #TVU4REGKEYS.item(node, open = False)
                     
        except NoListError:         # no operations necessary. Just Abort.
            nolisterr = True
            pass 
        except PermissionError as e:
            pass
        except OSError as e:
            debug_msg = 'OSError::function: [{}] -> lineno: [{}]\n'.format(info[FCN], info[LNO]) 
            #for x in e.args:
            #    debug_msg += x + '\n'
            prn_exception_info(e, 'OSError', debug_msg)
            if RE_RAISE:
                raise
        except Exception as e:
            debug_msg = 'Exception::function: [{}] -> lineno: [{}]\n'.format(info[FCN], info[LNO]) 
            prn_exception_info(e, 'Exception', debug_msg)
            if RE_RAISE:
                raise
        finally:
            READY_VAR.set('Ready')
            ITEM_CAP.set('')
            if nolisterr:           # two "normal" conditions get execution to this point
                ITEM_PATH.set('')   # 1) the HKEY_DYN_DATA key has no children
            else:                   # 2) mapping is completed.
                ITEM_PATH.set('Registry mapping complete. Mapped {} registry nodes'.format(self.output_iter))
            
            #TVU4REGKEYS.heading('#0', text = 'Ready', anchor = 'w')
        

    ######################################################################################################
    def recurse(self, HKEYHandle, ndntcnt, keyNameWPath = None ):
        """
            recurse is the main engine for extracting data from the registry
        """
        ## ndntcnt is the self.indentcount at the time of the call
        ## if ndntcnt == -1, initialize
       
        info = getframeinfo(currentframe())         # source information for debug
        debug_msg = '\n {} -> {}'.format(info[0], info[2]) 
        DONT_PRINT_ = True
        try:
            info = getframeinfo(currentframe())         # source information for debug
                # Due to the change from winregal to winreg, it is necessary to build a keylist  ################################### 
            _ListOfKeys_, keycount_ = self.getListOfKeys4Key(HKEYHandle)     # list of immediate key children to HKEYHandle   
            if keycount_ == 0:          # if no key children, this is a leaf for these purposes
                return
                #raise NoCountError('the parameter key is NOT a parent', 'no count')
            
            _ListOfKeys_ = sorted(_ListOfKeys_[KEYLIST], key=str.lower)
            #  KEEP THIS ON SORTING tuples: sorted(student_tuples, key=lambda student: student[2])
            #
            # let recurse build the _ListOfKeys_          ##########################################################################
            #     

            info = getframeinfo(currentframe())         # source information for debug
            ndntcnt += 1
            for loop_iter in range(0, keycount_):
                try:
                    item = _ListOfKeys_[loop_iter]        ## then, we iterate over list originally _ListOfKeys_[KEYLIST]
                    loop_iter += 1
                    
                    self.output_iter += 1
                    if self.output_iter % 100 == 0:
                        global ITERANNUNVAR
                        ITERANNUNVAR.set(str(self.output_iter))
                        global ITEM_CAP
                        ITEM_CAP.set(item)
                        global ITEM_PATH
                        ITEM_PATH.set(keyNameWPath)
                        global GLOBAL_update_idletasks
                        GLOBAL_update_idletasks(14)
                        
                        
                    self.listOfHive.append((item, self.output_iter, ndntcnt))
                    info = getframeinfo(currentframe())         # source information for debug
                    if MYL:
                        keyPathing = keyNameWPath
                        if len(keyPathing) > 60:
                            keyPathing = keyPathing[:27] +'...' + keyPathing[-30:]

                    try:
                        msg__ = '{0:60}->{1:50}{2:>6}{3:>4}\n'.format(keyPathing, item, self.output_iter, ndntcnt)
                        info = getframeinfo(currentframe())         # source information for debug
                        MYL.addRegistryLogentry(msg__)
                    # in a previous iteration of this effort, at this point both HKEY's and HKEYValue's
                    # were being handled in this loop. Now, we know at this point that "item" is, in fact,
                    # an HKEY name. But, in order to recurse, we need the fully qualified key path name
                    # LESS the "HKEY_CURRENT_USER" or other HKEY string
                    
                    # SINCE THIS IS A RegKey it will, PROBABLY, have children.
                    # this forces the recursion.
                    # That being said, this is the only time the recursion is necessary
                    
                        info = getframeinfo(currentframe())         # source information for debug
                        nextKeyNameWPath = keyNameWPath + BACKSLASH + item
                        hndl_ = OpenKey(self.rootOfHiveIntAlias, nextKeyNameWPath, reserved = 0, access = KEY_READ)
                    except FileNotFoundError as e:
                        hndl_ = self.testRegistryPath(nextKeyNameWPath)
                        if not hndl_:                       # this MUST be a childless key?
                            continue
                        elif RE_RAISE:
                            raise
                    except PermissionError as e:
                        self.listOfHive.append((e.args[1], self.output_iter, ndntcnt))
                        continue
                    
                    except UnicodeEncodeError as e:
                        if 'charmap' == e.args[0]:
                            strfromunicode = get_string_from_unicode(e.args[1])
                            MYL.addRegistryLogentry(strfromunicode)
                            self.listOfHive.append((strfromunicode, self.output_iter, ndntcnt))
                        continue
                    except Exception as e:
                        if 'charmap' == e.args[0]:
                            strfromunicode = get_string_from_unicode(e.args[1])

                            self.listOfHive.append((strfromunicode, self.output_iter, ndntcnt))
                        continue
                            
                    self.recurse(hndl_, ndntcnt, nextKeyNameWPath)

                except NoCountError:        # this is routine. The exception is the parent has no key children
                    return
                except WindowsError as e:
                    debug_msg = 'WindowsError::function: [{}] -> lineno: [{}]\n'.format(info[FCN], info[LNO]) 
                    debug_msg += '\tkeyNameWPath = [{}], ndntcnt = [{}]'.format(keyNameWPath, ndntcnt)
                    prn_exception_info(e, 'WindowsError', debug_msg)
                    if RE_RAISE:
                        raise
                    continue
            
        except OSError as e:
            debug_msg = 'OSError::function: [{}] -> lineno: [{}]\n'.format(info[FCN], info[LNO]) 
            debug_msg += '\tkeyNameWPath = [{}], ndntcnt = [{}]'.format(keyNameWPath, ndntcnt)
            prn_exception_info(e, 'OSError', debug_msg)
            if RE_RAISE:
                raise
        except Exception as e:
            debug_msg = 'Exception::function: [{}] -> lineno: [{}]\n'.format(info[FCN], info[LNO]) 
            debug_msg += '\tkeyNameWPath = [{}], ndntcnt = [{}]'.format(keyNameWPath, ndntcnt) + debug_msg
            prn_exception_info(e, 'Exception', debug_msg)
            if RE_RAISE:
                raise
        finally:
            try:    
                _ListOfKeys_ = []
                CloseKey(hndl_)
            except: pass


    def testRegistryPath(self, keyNameWPath, key_name = None):
        """  tests a Registry path that has failed """
        try:
            hndl = OpenKey(self.rootOfHiveIntAlias, keyNameWPath, 0, KEY_READ)
        except FileNotFoundError as e:
            # is this a childless key??? 
            # test it for HKEYValue children; that will verity the key path, maybe{?}
            if True:
                return None
            elif RE_RAISE:
                raise
        except Exception as e:
            if RE_RAISE:
                raise
            else:
                return None
        finally:
            try:
                CloseKey(hndl)
            except:
                pass

                            
    def getListOfKeys4Key(self, handle4root_):
        '''
            if the argument is an HKEY..., gathers immediate "key" children to handle4root_
            into the dictionary, returndict.
        '''
        
        info = getframeinfo(currentframe())         # source information for debug
        debug_msg  = 'handle4root_ = [{}]'.format(handle4root_)
        debug_msg += '\n {} -> {}'.format(info[0], info[2]) 
        
        keyList = []
        valList = []
        returnDict = {}
        try:
            """
            keycount, valcount, lastmod = QueryInfoKey(handle4root_)
            
            Returns information about a key, as a tuple. handle4root_ is an already open key, 
            or one of the predefined HKEY_* constants.
            The result is a tuple of 3 items:
                #0: An integer giving the number of sub keys this key has.
                #1: An integer giving the number of values this key has.
                #2 : An integer giving when the key was last modified (if available) 
                #     as 100’s of nanoseconds since Jan 1, 1601.            
            """
            self.i = 0
            def buildkeylist():
                while True:
                    try:
                        sid = EnumKey(handle4root_, self.i) 
                        keyList.append(sid)
                        self.i += 1

                    # OSError is raised when EnumKey no longer has product 
                    # specifically to break the "while True" loop
                    except OSError: 
                        break
                   
            buildkeylist()
            lenKeyList = len(keyList)
            if lenKeyList > 0:
                returnDict.update(klst = keyList)
                return returnDict, lenKeyList
            else:
                return {}, 0
    
        except Exception as e:
            prn_exception_info(e, 'OSError', debug_msg)
            return {}
        finally:
            pass
        

    def printValueOrKey(self, hierOfParentcy, me, toPrn = None, iter = None, indentCnt = None):
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


def GLOBAL_update_idletasks(WAITFOR = 15):
    TK_ALIAS.after(WAITFOR, TK_ALIAS.update())


if __name__ == '__main__':
    TK_ALIAS = win = tk.Tk()
    x = 1000
    y = 500
    win.geometry('+{0}+{1}'.format(x,y))
    win.attributes('-topmost', 1)
    win.config(bd = 4)
    
    ttl = os.path.basename(sys.argv[0])
    if DEBUG:
        MYL = MyLog()
    #MYL = MyLog()
    win.title(ttl)
    CHOOSE_REG_KEY_VAR = StringVar()
    
    gui = InitUI(win)

    YouMayResize = True
    win.protocol("WM_DELETE_WINDOW", gui._cancel)
    win.mainloop()



