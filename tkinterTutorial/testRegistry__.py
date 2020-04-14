

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
from ResourceUseProcess_childDlg import RegistryMemoryUseChild
from multiprocessing import Pool, Process, Queue, Pipe

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


roots_of_hives = {    
    "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
    "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
    "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
    "HKEY_USERS": winreg.HKEY_USERS,
    "HKEY_PERFORMANCE_DATA": winreg.HKEY_PERFORMANCE_DATA,
    "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
    "HKEY_DYN_DATA": winreg.HKEY_DYN_DATA
}

HivesList = list(roots_of_hives)
        

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
parent_conn, child_conn = Pipe()
YouMayResize = False
DEBUGFILENAME = './{}.txt'.format(os.getpid())
CHOOSE_REG_KEY_VAR = None


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
            
        '''
        def dlgIsAlive(_dlg):
            """ dlgIsAlive: for threading, the RegistryMemoryUseChild must report 
                that it is initializing before the wait_window loop is begun.
            """
            if _dlg:
                self._memusedlg = _dlg
                #_dlg.start()
            else:
                self._memusedlg = None
         '''

        @staticmethod
        @property
        def memoryUsageDlg(self):
            return self


        @staticmethod
        @memoryUsageDlg.deleter
        def memoryUsageDlg(self):
            del self


class InitUI(Frame):
 
    def __init__(self, parent):
        Canvas.__init__(self, parent)

        YouMayResize = False                  ## flag to prevent resizing during initialization
        # what is my (script) name
        scriptname = os.path.basename(__file__)
        
        self.lstUnknown = {}                    ## dictionary for registry "unknowns", usually unicode
                                                ## Created in RecursiveRegistry.recurse and used in bldRegTree
        self.parent = parent
        win.bind("<Configure>", self.on_resize)
        
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

        self['bg'] = 'blanched almond'
        
        self.style = ttk.Style()
            
        self.fontVar = tk.StringVar()
        self.fontVar.trace("w", self.check_fontVar)        
        
        self.rootsOfTree = []   # a list to contain the IID of each of the tree roots
                                # list is built as the Treeview is built

        self.srchTreeStringVar = StringVar()
        ##self.srchTreeStringVar.trace('w', self.onSrchTree)

        bldNBKFrame = BldTabNotebookFrame(self)
        bldNBKFrame.pack(fill = 'both', expand = 'yes')

        self.pnWin = BldPanedWindow(bldNBKFrame.mainHiveFrame)
        self.pnWin.pack(fill = 'both', expand = True)
        #self.win.bind("<Button-1>", self.on_button_1_down)

        
        self.memusedlg = None                   # testRegistry_childDlg
        
        menu = Main_menu(master = self)
        parent.configure(menu = menu)


        frm_sbar = Frame_StatusBar(self)
        frm_sbar.pack(anchor = 'sw', side = 'bottom', fill = 'x', expand = False)
        
        YouMayResize = True
        #self.sashXWas = self.pnWin.sash_coord(0)[0]
        self.pack(fill = 'both', anchor = 'center', expand = True)
        self.origsashposition = self.sashXWas = 350
        self.chooseFrameOriginalHeight = 0
    
        InitUI_utilities(self, parent)

        return 


    def on_button_1_down(self, event):
        #self.update()
        #self.chooseFrameOriginalHeight = self.chooseFrame['height']
        return
        
    
    def on_resize(self, event):
        if not YouMayResize:
            return
        if self.width == event.width:
            return
        # determine the ratio of old width/height to new width/height
        try:
            wscale = float(event.width)/self.width
            hscale = float(event.height)/self.height
        except Exception as esc:
            return

            print(s, esc.args)
        
        self.width = event.width
        self.height = event.height
        
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        
        
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
        #self.chooseFrame['height'] = self.chooseFrameOriginalHeight


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
            EnumKeysFrame3.lsBoxEnumKeys['font'] = fontString

    
    @staticmethod
    def _cancel():
        if MB.askokcancel("Question", "Are you sure you wish to quit?"):
            if MemoryUsageChild.memoryUsageDlg:
                del MemoryUsageChild.memusedlg
            sys.exit(0)

   
class InitUI_utilities:
    def __init__(self, master, master_parent):
        pass

    @staticmethod
    @property
    def DlgParent(self):
        return master_parent

          
class Main_menu(Menu):
    """ main menu and sundry """
    def __init__(self, master):
        Menu.__init__(self, master)
        self.parent = master
        fileMenu = Menu(self, tearoff=False)
        submenu = Menu(fileMenu , tearoff=False)
        submenu.add_command(label="New feed")
        submenu.add_command(label="Bookmarks")
        submenu.add_command(label="Mail")
        fileMenu.add_cascade(label='Import', menu=submenu , underline =0)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", underline=2, command = self.parent._cancel)
        self.add_cascade(label="File", underline=1, menu=fileMenu)

        
        editMenu = Menu(self, tearoff = False)
        srchTreeCmd = editMenu.add_command(label = 'Search Tree', command = self.srchRegKeyTree)
        
        ###   master.bind('<Control-F>', self.srchRegKeyTree)

        self.add_cascade(label = 'Edit', underline = True, menu = editMenu)

        self.showStat = tk.BooleanVar()
        self.showStat.set(True)
        
        vuMenu = Menu(self , tearoff=False)
        vuMenu.add_command(label = "Choose font", command = self.chooseFont)
        vuMenu.add_checkbutton(label="Show statusbar",
                command = self.toggleStatusBar , variable=self.showStat , onvalue=True , offvalue=False)
        vuMenu.add_separator()
        vuMenu.add_command(label = 'View memory used')
        self.add_cascade(label="View", menu=vuMenu)

        class TheBuildMenu(Menu):
            def __init__(self, master):
                Menu.__init__(self, master)
                self.configure(tearoff = False)
            
                chooseRegKeyMenu = Menu(self, tearoff = True)
                i = 0
                for item in HivesList:
                    chooseRegKeyMenu.add_radiobutton(label = item, variable = CHOOSE_REG_KEY_VAR)
                    i += 1

                self.add_cascade(label = "Choose RegKey", menu = chooseRegKeyMenu, underline = 1)
                self.add_cascade(label = 'Build RegKey', underline = 1, command = BuildRegKeyTree.buildRegKeyTree(CHOOSE_REG_KEY_VAR))

                master.bind('c', lambda e : edit_btn.event_generate('<<Invoke>>'))

                self.add_separator()

                self.add_cascade(label = 'Clear RegKey Tree', underline = 3, command = Treeview_4_RegKeys.clearRegKeys)
                self.add_cascade(label = 'Test enum_keys generator', command = NoteBookUtilities.testEnumKeys())

        self.add_cascade(label = 'Build', underline = 2, menu = TheBuildMenu(self))

        
    
        class Menu_choose_RegKey(Menu):
            def __init__(self, parent):
                Menu.__init__(self, parent)
                self.configure(tearoff = False)
                self.hiveSubMenu = Menu(tearoff = True)
        
                for item in HivesList: 
                    self.hiveSubMenu.add_radiobutton(label = item, variable = CHOOSE_REG_KEY_VAR)  
        
                self.add_cascade(label = "Choose registry hive", menu = self.hiveSubMenu, underline = True)
        
                self.add_cascade(label = 'Build Hive', underline = 1, command = TheBuildMenu(parent))
                parent.bind('c', lambda e: edit_btn.event_generate('<<Invoke>>'))

                self.add_separator()
                self.add_cascade(label = 'Clear RegKey Tree', underline = 3, command = Treeview_4_RegKeys.clearRegKeys)
                self.add_cascade(label = 'Test enum_keys generator', command = NoteBookUtilities.testEnumKeys)

        Menu_choose_RegKey(self.parent)


        #self.add_cascade(label = 'Build', underline = 1, menu = self.bldMenu)
        
        aboutMenu = Menu(self, tearoff = False)
        pidsubmenu = Menu(fileMenu , tearoff=False)
        pidsubmenu.add_command()
        aboutMenu.add_cascade(label="Process Id: [{}]".format(os.getpid()) )
        self.add_cascade(label = 'About', underline = 1, menu = aboutMenu)

  
    def returnFrame(self):
        return Frame(self)

 
    @staticmethod
    def srchRegKeyTree(self, *args):
        dlg = TreeviewUtilities(self.win)
        dlg.SearchTree(self.tvu_4_roots)
        self.win.wait_window(dlg.top)
        return


    def setNotebookTab(self, *args):
        return


    def getNotebookTab(self, *args):
        return self.tabNdxIntVar.get()


    def onClick(self):
        pass

    
    def toggleStatusBar(self):
        if (self.showStat.get() == True):
            self.sbarFrame.pack(anchor = 'w', side = 'bottom', fill = 'both', expand = True)
        else:
            self.sbarFrame.pack_forget()


    
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
            
        self.treebldbtn = Button(self, text = 'Build', command = BuildRegKeyTree.buildRegKeyTree(CHOOSE_REG_KEY_VAR))
        setColRowWeight(cbOpt)
        self.treebldbtn.grid(row = 0, column = 3, padx = 3, sticky = 'e')
        self.treebldbtn['state'] = 'disable'
        
        CHOOSE_REG_KEY_VAR.trace('w', self.onChooseRegKey)
        

    def onChooseRegKey(self, *args):
        if CHOOSE_REG_KEY_VAR.get() != '':            
            self.treebldbtn['state'] = 'normal'
        else:            
            self.treebldbtn['state'] = 'disable'


class BuildRegKeyTree():
        """  class BuildRegKeyTree uses the RecursiveRegistry generator .send   """

        @staticmethod
        def buildRegKeyTree(self, regkey = None):
            Treeview_4_RegKeys.clearRegKeys
            

            if not regkey:
                regkey = CHOOSE_REG_KEY_VAR.get()
                if regkey == '':
                    return
            
            reg = RecursiveRegistry(hiveroot = regkey)
                                   
            snd = reg.RecursiveRegistry_yield(0)
            try:
                for iid in self.rootsOfTree:
                    self.hiveTreeview.delete(self.hiveTreeview.get_children(iid))
                self.rootsOfTree.clear()
                Treeview_4_RegKeys.clearRegKeys
                self.hiveTreeview.heading('#0', text = self.StrVar_4_Reg_Roots.get())
            except:
                pass
            for tpl in snd:
                ##self.writeTvuToFile(tpl, testfile = True)
                self.bldRegTree(tpl)
                ##self.hiveTreeview.update()
                ##self.walkTheTree()
    
       
class Frame_4_RegKeysContainer(LabelFrame):
    """  contains two elements: Frame_4_RegKey_choice <above>::has  Combobox and Build button
                        -and-   Frame_4_RegKeys <below>
    """
    def __init__(self, parent):
        LabelFrame.__init__(self, parent)
        self.configure(bg = 'light cyan', text = 'turquoise:::Frame_4_RegKeys')

        frm_4_RegKey_choice = Frame_4_RegKey_choice(self)
        frm_4_RegKeys = Frame_4_RegKeys(self)
        setColRowWeight(frm_4_RegKey_choice)
        setColRowWeight(frm_4_RegKeys)
        setColRowWeight(self)

        frm_4_RegKey_choice.pack(side = 'top', fill = 'x', expand = False, anchor = 'w')
        frm_4_RegKeys.pack(side = 'top', fill = 'both', expand = True, anchor = 'w')

class BldChooseFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
            
        self['bg'] = parent['bg']
        self.bindtags = ['chooseFrame']

        cbOpt = ttk.Combobox(self, justify = 'center')
        
        setColRowWeight(cbOpt)
        cbOpt.grid(row = 0, column = 0, sticky = 'ew', columnspan = 3)
        setColRowWeight(cbOpt, rowCount = 1, col_weight = 1, colCount = 3)

        self.treebldbtn = Button(self, text = 'Build')
        self.treebldbtn.grid(row = 0, column = 3, padx = 3, sticky = 'e')

        self.grid(sticky = 'new', columnspan = 3)
        setColRowWeight(self)
        

        @property
        def chooseFrameHeight(self):
            return self._chooseFrameHeight

        @chooseFrameHeight.setter
        def  chooseFrameHeight(self, value):
            _chooseFrameHeight = value
            self.chooseFrame['height'] = int(round(value))
         

class Frame_4_RegKeys(LabelFrame):
    """
        contains tvu_4_RegKeyHive and two Scrollbars
    """
    def __init__(self, parent):
        LabelFrame.__init__(self, parent)
        self.config(bd = 2, bg = 'light pink', text = 'Frame_4_RegKeys')
        tvu_4_RegKeys = Treeview_4_RegKeys(self)
        
        ysb = tk.Scrollbar(self, orient='vertical', command= tvu_4_RegKeys.yview)
        ysb.config(activebackground = 'firebrick1', width = 12)
        xsb = tk.Scrollbar(self, orient='horizontal', command = tvu_4_RegKeys.xview)
        xsb.config(activebackground = 'firebrick1')
        tvu_4_RegKeys.configure(yscroll=ysb.set, xscroll=xsb.set)
            
        tvu_4_RegKeys.columnconfigure(0, minsize = 300, pad = 15)
        tvu_4_RegKeys.grid(row = 0, column = 0, sticky = 'news', rowspan = 3, columnspan = 3)
        setColRowWeight(tvu_4_RegKeys, colCount = 3, rowCount = 3)
            
        colCount, rowCount = self.grid_size()
        ysb.grid(row = 0, column = 3, sticky = 'news', rowspan = rowCount)
        xsb.grid(row = 3, column = 0, sticky = 'swe', columnspan = colCount)
        setColRowWeight(ysb)    
        setColRowWeight(xsb)    


class Treeview_4_RegKeys(Treeview):
    def __init__(self, parent):
        Treeview.__init__(self, parent)
        self.configure(padding = (2,2,2,2))
        self.bind('<Double-Button-3>', self.clearRegKeys)
        self.heading('#0', text = REGHIVETXT, anchor = 'w')

    @property
    def tvu4Hive(self):
        return self
    
    @staticmethod
    @property
    def clearRegKeys(self):
        if not self:
            MB.showinfo('Nothing to do', 'Treeview_4_RegKeys is unbuilt')
            return
        for i in self.get_children():
            self.delete(i)
        self.heading('#0', text = REGHIVETXT, anchor = 'w')
        

        ####self.hiveTreeview.heading('#0', text = REGHIVETXT, anchor = 'w')

    @staticmethod
    @property
    def walkTheTree(self):
        EnumKeysFrame3.lsBoxEnumKeys.delete(0, 'end')
        for child in self.tvu_4_roots.get_children():
            S = "{0:>60} :: {1}".format(self.item(child)["text"], self.tvu_4_roots.item(child)["values"])
            EnumKeysFrame3.lsBoxEnumKeys.insert('end', S)
            info = getframeinfo(currentframe())
            DoDebugPrint(S, scriptname = info[0], lineno = info[1], fcnname= info[2])
            DoDebugPrint(child, scriptname = info[0], lineno = info[1], fcnname= info[2])
         
    


    @staticmethod
    @property
    def clearHiveTvu(self):
        return clear_roots_tvu


class Frame_StatusBar(LabelFrame):
    def __init__(self, parent):
        LabelFrame.__init__(self, parent)
        
        ready_StrVar = StringVar()
        ready_StrVar.set("Ready")
        lblsb = Label(self , textvariable = ready_StrVar, relief = 'groove')
        lblsb.pack(side = LEFT, anchor = 'w')

        sep0 = ttk.Separator(self, orient = 'vertical')
        sep0.pack(side = 'left', anchor = 'w', padx = 15, fill = 'x')


        self.selection_StrVar = StringVar()
        self.selection_StrVar.set('Selection: ')
        lblselcap = Label(self, text = 'Selection: ', relief = 'solid')
        lblselcap.pack(side = 'left')

        lblsel = tk.Label(self, textvariable = self.selection_StrVar, 
                          relief = 'sunken', width = 35)
        lblsel.pack(side = 'left', padx = 3)
        setColRowWeight(self)

    @staticmethod
    @property
    def StatusBar_ready_SVar(self):
        return __init__.ready_StrVar

    @staticmethod
    @property
    def StatusBar_selection_SVar(self):
        return __init__.selection_StrVar



MYTAB = ' '*2

KEYLIST = 'klst'
VALLIST = 'vlst'

MASTERWINDOW = None
class getRegDict():
    def __init__(self, *args, **kwargs):
        WR = winregal()
        regdict = WR.to_dict()
        return


class RecursiveRegistry(GlobalErrorHandler):  ##Generator
    def __init__(self, **kwargs):
        GlobalErrorHandler(MASTERWINDOW).__init__(MASTERWINDOW)
        
        lstUnknown = {}
        self.indentcount = 0
        self._iter = 0
        self.kwargs = kwargs
      
        self.listOfHive = []
        

    @property
    def lstUnknown(self):
        return lstUnknown


    def RecursiveRegistry_yield(self, ignoredArg, filenameUnknown = '', **kwargs):   ###
        _list = []
        self.getDirList = False
        yield_count = 0
        self.dictUnknowns = {}

        ## the RegKey to process
        if 'hiveroot' in self.kwargs:
            regkeyname = kwargs['hiveroot']
        else:
            raise ValueError('No RegKey passed to {} by {}', format(inspect.stack[0][3], inspect.stack[0][0]))

        regkey = roots_of_hives[regkeyname]
        ## getRegKeyTopLvlList is probably overkill. RegKey had enum_keys that should do it
        self.keyValLists = self.getRegKeyTopLvlList(regkey)
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
        if not filename:
            filename = DEBUGFILENAME+'unknowns'
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
      
    
    def getRegKeyTopLvlList(self, root):
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
    MASTERWINDOW = win
    CHOOSE_REG_KEY_VAR = StringVar()
    
    gui = InitUI(win)
    
    win.protocol("WM_DELETE_WINDOW", gui._cancel)
        ##main()
    win.mainloop()



