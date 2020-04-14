
import tkinter as tk
from tkinter import Tk, Label, Button, StringVar, Toplevel
MSG = 'hello to main app'

class ChildDialog(Toplevel):
    def __init__(self, parent, app = None):
        self.app = app
        ok_button = Button(parent, text = MSG, command = self.on_ok)
        self.lbl = Label(parent, text = MSG)
        self.lbl.pack()
        ok_btn.pack()

    def on_ok(self):
        # send the data to the parent
        self.app.new_data(MSG)


class MainApplication(Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.lblStringVar = StringVar()
        self.lblStringVar.trace('w', self.lblStringVarCallback)
        lbl = Label(self, text = 'another msg', textvariable = self.lblStringVar)


    def on_show_dialog(self):
        dialog = ChildDialog(self)
        dialog.show()

    def new_data(self, data):
        #... process data that was passed in from a dialog ...
        pass

    def lblStringVarCallback():

        pass

if __name__ == '__main__':
    me = MainApplication()



    me.mainloop()