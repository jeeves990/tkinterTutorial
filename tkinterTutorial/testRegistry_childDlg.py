

from tkinter import Tk, Label, Button, StringVar, Toplevel, Entry, Text, Scrollbar, LabelFrame, \
        Menu, N,E,W,S
from tkinter.ttk import Treeview
import psutil
from time import clock, sleep
import time as TM
import os
import threading as THR
from concurrent.futures import ThreadPoolExecutor as pool
from PyUtilities  import setColRowWeight
from threadWTrace import thread_with_trace


def onExit(obj):
    obj.destroy()


class BldTreeView(Treeview):
    def __init__(self, win):
        Treeview.__init__(self, win)

        self['show'] = ('headings')
        self['columns'] = ('Time', 'CPUpct','CPUtime','MEMpct')
        #self.heading("#0",text="Name",anchor = 'w')
        capTime = '#1'
        CPUpct = '#2'
        CPUtime = '#3'
        MEMpct = '#4'
        
        self.heading(capTime, text="Time",anchor = 'e')
        self.heading(CPUpct, text="CPU %",anchor = 'w')
        self.heading(CPUtime, text="CPU Time",anchor = 'w')
        self.heading(MEMpct, text="Memory %",anchor = 'w')

        self.column(capTime, width = 50, anchor = 'e')
        self.column(CPUpct, width = 75, anchor = 'e')
        self.column(CPUtime, width = 75, anchor = 'e')
        self.column(MEMpct, width = 75, anchor = 'e')
        
        self.heading(capTime, text = 'Time')
        self.heading(CPUpct, text = 'CPU %')
        self.heading(CPUtime, text = 'CPU Time')
        self.heading(MEMpct, text = 'Memory %')


class bldMenu(Menu):
    def __init__(self, win):
        Menu.__init__(self, win)
        self.win = win
        fileMenu = Menu(self, tearoff=False)
        submenu = Menu(fileMenu , tearoff=False)
        submenu.add_command(label="New feed")
        submenu.add_command(label="Bookmarks")
        submenu.add_command(label="Mail")
        fileMenu.add_cascade(label='Import', menu=submenu , underline =0)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", underline=2, command = self.onExit)
        self.add_cascade(label="File", underline=1, menu=fileMenu)

        editMenu = Menu(self, tearoff = False)
        vuMenu = Menu(self , tearoff=False)
        vuMenu.add_command(label = "Choose font")
        vuMenu.add_checkbutton(label="Show statusbar")
        vuMenu.add_separator()
        vuMenu.add_command(label = 'get memory data', command = self.win.getMemData)
        self.add_cascade(label="View", menu=vuMenu)


    def onExit(self):
        onExit(self.win)


class RegistryMemoryUseChild(Toplevel):
    def __init__(self, parent, app = None, IAmAlive = None):
        Toplevel.__init__(self, parent)
        self.app = app
        self.killflag = False
        self.win = parent
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+parent.winfo_width(),
                                  parent.winfo_rooty()))
        self.initial_focus = self

        self.pid = os.getpid()
        psname = psutil.Process(self.pid).name()
        rsstring = '{0} pid:[{1}] resource: [{2}]'.format('Resource Usage Data', self.pid, psname)
        self.mainframe = mFrm = LabelFrame(self, text = rsstring, bg = 'beige')
        
        txtSVar = StringVar()
        #txtSVar.trace('w', self.tstSVarTrace)
        tvu = self.colvu = BldTreeView(mFrm)
        self.colvu.grid(row = 0, column = 0, sticky = 'news')

        ysb = Scrollbar(mFrm, orient = 'vertical', command = tvu.yview)
        xsb = Scrollbar(mFrm, orient = 'horizontal', command = tvu.xview)
        tvu.config(xscrollcommand = xsb.set, yscrollcommand = ysb.set)
        
        ysb.grid(row = 0, column = 1, sticky = 'ns')
        #xsb.grid(row = 1, column = 0, sticky = 'ew')
        #setColRowWeight(xsb, colCount = 1, rowCount = 2)

        mFrm.grid(row = 0, column = 0, sticky = 'news')
        
        self.menubar = bldMenu(self)
        self.config(menu=self.menubar)
 
        setColRowWeight(tvu, colCount = 1, rowCount = 1)
        setColRowWeight(ysb, colCount = 2, rowCount = 1)
        setColRowWeight(mFrm, 2, 2, colCount = 3, rowCount = 3)
        setColRowWeight(self, colCount = 3, rowCount = 3)

        '''
        the child must inform the parent it is alive. Otherwise the parent has
        no evidence of it until the child is destroyed. REM: wait_window
        '''
        if IAmAlive:
            IAmAlive(self)
        self.IAmAlive = IAmAlive
        self.wait_window(self)


    def threadTrace(self):

        return


    def start(self):
        #with pool(max_workers = 1 ) as exec:
        #    exec.map(self.thread_function)
        #self.thrx = THR.Thread(target = self.thread_function, args=(1,), daemon = True)
        self.thrx = thread_with_trace(target = self.thread_function) 
        self.thrx.start()

    
    def thread_function(self, *args):
        while True:
            if self.killflag: 
                break
                
            self.update()
            ltm = TM.localtime()
            localtime = "%2.2d:%2.2d:%2.2d" % (int(ltm[3]), int(ltm[4]), int(ltm[5]))
            ps = psutil.Process(os.getpid()).memory_info()
            cpuPct = psutil.cpu_percent()
            
            self.colvu.insert('', 0, text = '', values = (localtime, '%02.2f%%' % cpuPct, 
                                                          ps[1], '%02.2f%%' % self.getMemData(), ps[2]))
            sleep(1)
        self.thrx = None        # after the thread stops, this will be a flag

   
    def getMemData(self):
        p = psutil.Process(self.pid) 
        return p.memory_percent()
     
        
    def on_ok(self, *args):
        # send the data to the parent

        if len(self.ntryStringVar.get()) > 0:
            msg = self.ntryStringVar.get()
        else:
            msg = MSG
        self.app(msg)


    def cancel(self):
        self.killflag = True
        self.IAmAlive(None)
        self.destroy()







