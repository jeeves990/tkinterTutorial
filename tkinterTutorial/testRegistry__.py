

import tkinter as tk
from tkinter.ttk import Treeview
import tkinter.ttk as ttk
from tkinter import PanedWindow, Frame, Label, BOTH, VERTICAL, HORIZONTAL, Entry, Scale, Button,\
        Menu, messagebox as MB, IntVar, StringVar, LEFT, Canvas

import sys

import winreg as winreg
from winreg import *
from winregal import *
from PyUtilities  import setColRowWeight
from MyLogging import MyLog

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


def onExit():
    if MB.askokcancel("Question", "Are you sure you wish to quit?"):
        sys.exit(0)


class InitUI(Frame):
 
    def __init__(self, win):
        Canvas.__init__(self, win)

        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

        self.win = win
        self['bg'] = 'blanched almond'
        self.bldPanedWindow()
        self.pack(fill = 'both', anchor = 'center', expand = True)
        self.bldMenu()
        self.bldStatusBar()
        

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
        fileMenu.add_command(label="Exit", underline=0, command = onExit)
        self.menubar.add_cascade(label="File", underline=0, menu=fileMenu)

        self.showStat = tk.BooleanVar()
        self.showStat.set(True)

        viewMenu = Menu(self.menubar , tearoff=False)
        viewMenu.add_checkbutton(label="Show statusbar",
                command = self.toggleStatusBar , variable=self.showStat , onvalue=True , offvalue=False)
        
        hiveSubMenu = Menu(viewMenu, tearoff = True)
        self.hiveSubMenuVar = IntVar()
        self.hiveSubMenuVar.trace('w', self.onSelectHive)
        lst = roots_hives.items()
        i = 0
        for item in lst:
            print(item)
            #continue
            hiveSubMenu.add_radiobutton(label = item[0], value = i, variable = self.hiveSubMenuVar)
            i += 1


        viewMenu.add_cascade(label = "Choose registry hive", menu = hiveSubMenu, underline = True)
        
        self.menubar.add_cascade(label="View", menu=viewMenu)


    def returnFrame(self):
        return Frame(self)


    def onClick(self):
        pass


    def onSelectHive(self, varname, ndx, action):
        lst = list(roots_hives)
        self.hiveLblVar.set(lst[self.hiveSubMenuVar.get()])
        #print('[', lst[self.hiveSubMenuVar.get()], '] was selected')
        pass


    def bldStatusBar(self):
        self.sbarFrame = Frame(self)
        self.svarready = StringVar()
        self.svarready.set("Ready")
        self.sb = Label(self.sbarFrame , textvariable=self.svarready, relief = 'groove')
        self.sb.pack(side = LEFT, anchor = 'w', expand = 0)

        ttk.Separator(self.sbarFrame, orient = 'vertical').pack(side = 'left', anchor = 'w', 
                                                     padx = 15, fill = 'x', expand = 0)


        self.svarselection = StringVar()
        self.svarselection.set('Selection: ')
        lblselcap = Label(self.sbarFrame, text = 'Selection: ', relief = 'solid')
        lblselcap.pack(side = 'left')

        lblsel = tk.Label(self.sbarFrame, textvariable = self.svarselection, relief = 'sunken', width = 35)
        lblsel.pack(side = 'left', padx = 3, expand = 1)
        self.sbarFrame.pack(anchor = 'w', side = 'bottom', fill = 'both', expand = True)
        setColRowWeight(self.sbarFrame)


    def toggleStatusBar(self):
        if (self.showStat.get() == True):
            self.sbarFrame.pack(anchor = 'w', side = 'bottom', fill = 'both', expand = True)
        else:
            self.sbarFrame.pack_forget()


    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        
        self.width = event.width
        self.height = event.height
        
        self.scale()
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        #self.scale("all",0,0,wscale,hscale)


    def bldPanedWindow(self):
        self.pnWin = PanedWindow(self)
        self.pnWin.config(bg = 'CadetBlue1', orient = 'horizontal', sashwidth = 4)
        
        hiveFrame = Frame(self.pnWin, bd = 3, bg = 'yellow2', width = 35)
        self.hiveLblVar = StringVar()
        self.hiveLblVar.trace('w', self.setHiveLbl)
        self.hiveLblVar.set('Hive')
        self.hiveLbl = Label(hiveFrame, textvariable = self.hiveLblVar, relief = 'raised')
        ##self.hiveLbl.pack(side = 'top', fill = 'x', expand = 'true')
        self.hiveLbl.grid(row = 0, column = 0, sticky = 'ew')
        self.pnWin.add(hiveFrame)

        self.bldHiveView(hiveFrame)
        setColRowWeight(hiveFrame)

        valueFrame = Frame(self.pnWin, bd = 5, bg = 'purple1', width = 35)
        self.valueFrameLbl = Label(valueFrame, text = 'hello', relief = 'raised')
        self.valueFrameLbl.pack(side = 'top', fill = 'x', expand = 'true')
        self.pnWin.add(valueFrame)
        self.addValueTvu(valueFrame)

        self.pnWin.paneconfig(hiveFrame, minsize = 200)
        self.pnWin.paneconfig(valueFrame, minsize = 200)
        self.pnWin.pack(fill = BOTH, anchor = 'center', padx = 4, pady = 4, expand = True)

    
    def setHiveLbl(self, var, dx, val):
        pass

    
        
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


    def bldHiveView(self, parent):
        self.hiveTvu = Treeview(parent)
        self.hiveTvu["columns"] = ('hive')
        self.hiveTvu['show'] = 'headings'

        ##self.hiveTvu.pack(anchor = 'center', fill = BOTH, expand = True)
        self.hiveTvu.grid(row = 1, column = 0, sticky = 'news')
        
        
        self.hiveTvu.insert('', 'end', 'widgets', text='Widget Tour')
 
        # Same thing, but inserted as first child:
        self.hiveTvu.insert('', 0, 'gallery', text='Applications')

        # Treeview chooses the id:
        id = self.hiveTvu.insert('', 'end', text='Tutorial')

        # Inserted underneath an existing node:
        self.hiveTvu.insert('widgets', 'end', text='Canvas')
        self.hiveTvu.insert(id, 'end', text='Tree')

        return self.hiveTvu


    def bldBase(self):
        titleLbl = tk.Label(self.win, text = sys.argv[0], justify = 'center').pack(fill ='x', expand = True)
        tvu = self.bldTree(self)
        tvu.pack(side = 'left', fill = 'y', expand = True)
        sep = tk.Separator(self, width = 5, orient = 'vertical'). pack(anchor = 'w', expand = False)
        lbox = tk.Listbox(win, width = 50, height = 25)
        lbox.pack(fill = 'both', expand = True, padx = 4, pady = 4)
        return lbox, tvu
        

class InitAsPanedwindow(PanedWindow):
    def __init__(self, parent):
        PanedWindow.__init__(self, parent)
        self.configure(orient = 'horizontal', sashwidth = 4)
        self.config(bg = 'CadetBlue1')
        
        left = Entry(self, bd = 5)
        self.add(left)

        m2 = PanedWindow(self, orient = VERTICAL)
        self.add(m2)

        top = Scale( m2, orient = HORIZONTAL)
        m2.add(top)

        bottom = Button(m2, text = "OK")
        m2.add(bottom)
        
        self.pack(fill = BOTH, anchor = 'center', expand = 1, padx = 4, pady = 4)



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


MYTAB = ' '*2

from GlobalErrorHandling import GlobalErrorHandler
class RecursiveRegistry(GlobalErrorHandler):
    def __init__(self, win):
        GlobalErrorHandler(win).__init__(win)
        ##for hive in roots_hives:
        self.indentcount = 0
        self.iter = 0
        self.origdirpath = r"HKEY_CURRENT_USER\Software"
        self.recurse(r"HKEY_CURRENT_USER\Software")


    def recurse(self, dirpath):
        
        with RegKey(dirpath) as key:
            _str = "{0} {1} {2}".format('----', dirpath, '-------------')
            self.printValueOrKey(_str, self.iter)
                 
            for item in key:
                self.iter += 1
                if self.iter % 50 == 0:
                    input('any key to continue')
                if isinstance(item, RegValue):
                    self.printValueOrKey(item, self.iter)
                    ##print(item.name, item.data)
                elif isinstance(item, RegKey):
                    
                    if dirpath == self.origdirpath:
                        self.indentcount = 0
                    else:
                        self.indentcount += 1
                    self.printValueOrKey(item.name, self.iter, self.indentcount)
                    ##print('------------------', dirpath, '-------------')
                    _dir = dirpath + "\\" + item.name
                    ##yield str2print
                    self.recurse(_dir)
                    

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



def main():
    win = tk.Tk()
    frm = tk.Frame(win).pack()
    lsbox = tk.Listbox(win)
    lsbox.pack()


    for item in reg_list:
        if regDtypeDict[item]:
            lsbox.insert('end', regDtypeDict[item])
        else:
            lsbox.insert('end', item)


    RecursiveRegistry(win)
    """
    i = 0
    for item in RecursiveRegistry():
        lsbox.insert(END, item)
        if i > 99:
            break
        i += 1
    """
    tk.mainloop()



class JustOneLevel4_1_hive:
    def __init__(self):    ##, lbox):
        aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                       KEY_READ | KEY_WOW64_64KEY)
        (numsubkeys, numvalues, lastmod) = QueryInfoKey(aKey)
        aString = "# subkeys: {0}, # values: {1}".format(numsubkeys, numvalues)
        ##lbox.insert('end', aString)
        self.indentCount = 0
        
        self.recurse(aKey)
        
        
    def recurse(self, aKey):
        self.indentCount += 0
        i = 0
        keyname = EnumKey(aKey, i)
        print(keyname)
        (numsubkeys, numvalues, lastmod) = QueryInfoKey(aKey)
        for i in range(0, numsubkeys):
            try:
                asubkey = OpenKey(aKey, keyname)
                # is this asubkey a value--
                #   --- or, does it have subkey's
                (numskey_, numvals_, lastmod_) = QueryInfoKey(aKey)
                if numskey_ > 0:
                    self.indentCount += 1
                    try:
                        subkeyname = EnumKey(asubkey, 0)
                        aKey = OpenKey(aReg, asubkey)
                        recurse(aKey)
                    except:
                        self.doSomething()
                try:
                    dir, type = QueryValueEx(asubkey, "DisplayName")
                    aString = "\t{0:>8}\t  [{1}]".format(i, str(dir))
                    lbox.insert('end', aString)
                except:
                    aString = "{0:>8}-----{1}_____".format(i, keyname)
                    ##lbox.insert('end', aString)
                i += 1
                keyname = EnumKey(aKey, i)
            except WindowsError:
                break

    def doSomething(self):
       
        return


class MyLittleFrame(Frame):
    def __init__(self, win):
        Frame.__init__(self, win)
        self.config(width = 150, height = 150, bg = 'DarkOrchid1')
        self.pack(anchor = 'nw', fill = BOTH, expand = True)

    def getFrame(self):
        return Frame(self)

if __name__ == '__main__':
    win = tk.Tk()
    x = 500
    y = 500
    win.geometry('+{0}+{1}'.format(x,y))
    win.attributes('-topmost', 1)
    win.protocol("WM_DELETE_WINDOW", onExit)

    InitUI(win)
    ##main()
    win.mainloop()

    
