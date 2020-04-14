
import tkinter as tk
from tkinter import Tk, Label, Button, StringVar, Toplevel, Entry
MSG = 'hello to main app'

class ChildDialog(Toplevel):
    def __init__(self, parent, app = None, IAmAlive = None):
        Toplevel.__init__(self, parent)
        self.app = app
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+150,
                                  parent.winfo_rooty()+150))
        self.initial_focus = self

        self.ntryStringVar = StringVar()
        
        ok_btn = Button(self, text = MSG, command = self.on_ok)
        lbl = Label(self, text = MSG)
        lntry = Entry(self, width = 50, textvariable = self.ntryStringVar)
        lntry.bind("<KeyRelease>", self.on_ok)
        
        lntry.pack()
        lbl.pack()
        ok_btn.pack()
        '''
        the child must inform the parent it is alive. Otherwise the parent has
        no evidence of it until the child is destroyed. REM: wait_window
        '''
        if IAmAlive:
            IAmAlive(self)
      
        self.wait_window(self)


    def on_ok(self, *args):
        # send the data to the parent
        print(self.ntryStringVar.get())
        if len(self.ntryStringVar.get()) > 0:
            msg = self.ntryStringVar.get()
        else:
            msg = MSG
        self.app(msg)


    def cancel(self):
        self.destroy()


class MainApplication(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.attributes('-topmost', True)

        self.lblSVar = StringVar()
        self.lblSVar.trace('w', self.lblStringVarCallback)

        nsv = self.ntrySVar = StringVar()
        nsv.trace("w", lambda name, index, mode,
                                nsv = nsv: self.ntrySVarCallback(nsv))
       
        ntry = Entry(self, width = 40, textvariable = nsv)
        ntry.bind("<KeyRelease>", self.ntrySVarCallback)
        lbl = Label(self, text = 'another msg', textvariable = self.lblSVar)
        btn = Button(self, text = 'click me', command = self.on_show_dialog)
        
        lbl.pack()
        ntry.pack()
        btn.pack()
        self.dlg = None
       

    def on_show_dialog(self):
        print(self.dlg)
        if not self.dlg:
            self.dlg = ChildDialog(self, self.new_data, self.dlgalive)
        print(self.dlg)
        

    def dlgalive(self, alive = False):
        self.dlg = alive
        return


    def new_data(self, data):
        self.lblSVar.set(data)
        pass


    def lblStringVarCallback(self, *args):
        #lbl['text'] = args[0]
        pass


    def ntrySVarCallback(self, *args):
        #if .!childdialog:
        self.dlg.ntryStringVar.set(self.ntrySVar.get())
        self.dlg.update()
        pass


if __name__ == '__main__':
    me = MainApplication()



    me.mainloop()