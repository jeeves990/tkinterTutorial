# tkinter treeview utilities


DATAMASK = 0b001
VALUEMASK = 0b010
KEYMASK = 0b100


from tkinter import *
import tkinter.ttk as ttk
from PyUtilities import setColRowWeight

class TreeviewUtilities(object):
    def __init__(self, win, *args):
        
        self.searchFoundAt = -1
        self.tree2search = None
        self.searchString = ''
        self.where2search = None

        self.top = Toplevel(win)
        self.top.lift()
        self.top.focus_force()
        self.top.grab_set()
        """
            def setActive(self):
                self.lift()
                self.focus_force()
                self.grab_set()
                self.grab_release()
        """
        """
        wn = win.winfo_geometry()
        print(wn)
        wnHt = win.winfo_height()
        wnPar = self.top.winfo_parent()  ## returns a string; the mangled name
        wnReqHt = win.winfo_reqheight()
        wnReqWd = win.winfo_reqwidth()
        """

        x = self.top.winfo_x()
        y = self.top.winfo_y()

        self.top.geometry("+{0}+{1}".format(x, y))
        self.build4treeSearch()
      
    

    def SearchTree(self, *args, **kwargs):
        self.build4treeSearch()

        # must have args are (0) the tree to search (2) what to search for
        self.tree2search = args[0]
        #self.searchString = args[1]
        if 'where2search' in kwargs:
            self.keyValRData = kwargs['where2search']
            if self.keyValRData | KEYMASK:
                print('search keys')
            if self.keyValRData | VALUEMASK:
                print ('search values')
            if self.keyValRData | DATAMASK:
                print ('search data')
        return

        children = self.tree2search.get_children()
        for child in children:
            text = self.tree.item(child, 'text')
            if text.startswith(self.entry.get()):
                self.tree.selection_set(child)
                return True
            else:
                res = self.search(child)
                if res:
                    return True

    def build4treeSearch(self):
        self.top.title = 'Search Treeview'
        leftPane = PanedWindow(self.top, orient = 'vertical')

        ntryLblFrame = LabelFrame(leftPane, text = 'Find what:', height = 3)
       
        ntry = Entry(ntryLblFrame, width = 40)
        ntry.grid(columnspan = 4, sticky = 'news')
        leftPane.add(ntryLblFrame)


        optframe = LabelFrame(leftPane, text = 'Look at', width = 20)
        self.keyCkBox = Checkbutton(optframe, text = 'Keys  ', width = 12)
        self.valCkBox = Checkbutton(optframe, text = 'Values', width = 12)
        self.dtaCkBox = Checkbutton(optframe, text = 'Data  ', width = 12)
        self.keyCkBox.grid(row = 0, column = 0, sticky = 'w')
        #self.keyCkBox.place(x = 40, y = 4)
        self.dtaCkBox.grid(sticky = 'w')
        self.valCkBox.grid(sticky = 'w')
        
        leftPane.add(optframe)
        
        frmMatchBtn = Frame(leftPane)
        matchBtn = Checkbutton(frmMatchBtn, text = 'Match whole string only')
        matchBtn.grid(sticky = 'w')
        leftPane.add(frmMatchBtn)

        btnPane = PanedWindow(self.top, orient = 'vertical')

        fnNxBtn = Button(btnPane, text = 'Find next', underline = 2, width = 12)
        fnNxBtn.grid(row = 0, column = 0, sticky = 'n', pady = 2, padx = 2)
        cxBtn = Button(btnPane, text = 'Cancel', width = 12)
        cxBtn.grid(column = 0, sticky = 's', pady = 2, padx = 2)
        setColRowWeight(btnPane)
        
        """
        colCount, rowCount = leftPane.grid_size()
        #for i in range(0, colCount):
        #    Label(leftPane, text = " ", width = 9, height = 1).grid(row = 3, column = i)
        
        sep = ttk.Separator(leftPane, orient = 'horizontal')
        sep.grid(row = rowCount, column= 0, sticky = 'news')
        """
        setColRowWeight(leftPane)
        leftPane.grid(column = 0, sticky = 'news')
        btnPane.grid(row = 0, column = 1, sticky = 'nes', 
                    padx = 4, pady = 4,
                    columnspan = 2, rowspan = 3)
       

FILENAME = "ModalDialogTest.txt"
class Treeview4Test(Frame):
    def __init__(self, win):
        Frame.__init__(self, win)
        self.win = win
        self.testTvu()


    def testTvu(self):
        TreeviewUtilities(self)

    def LoadFromFile(self):
        with open(FILENAME, 'r') as file:
            for line in file:
                pass
            
            pass
        pass


class MyDialog:

    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        Label(top, text="Value").pack()
        self.e = Entry(top)
        self.e.pack(padx=5)
        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)
    def ok(self):
        print( "value is", self.e.get())
        self.top.destroy()


def doClick():
    Treeview4Test(tk)


if __name__ == '__main__':
    tk = Tk()
    tk.geometry("+{}+{}".format(600, 800))
    tk.update()
    Button(tk, text = 'click to operate', command =  doClick).pack()
    tk.mainloop()


    

