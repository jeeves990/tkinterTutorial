
import tkinter as tk
from tkinter import messagebox as MB
import traceback
import clipboard  as CB

class GlobalErrorHandler(object):
    def __init__(self, masterWindow):
        object.__init__(self)
        masterWindow.report_callback_exception = self.report_callback_exception

    def report_callback_exception(self, *args):
        err = traceback.format_exception(*args)
        errFormatted = ''
        for er in err:
            errFormatted += er + '\n__'
        errFormatted = errFormatted[:-3]
        CB.copy(errFormatted)

        MB.showerror('Exception', errFormatted)

class App(GlobalErrorHandler):
    def __init__(self, win):
        GlobalErrorHandler().__init__(masterWindow=win)
        ##win.report_callback_exception = self.report_callback_exception
        self.frame = tk.Frame(win)
        self.frame.pack()
        b = tk.Button(
            self.frame, text="This will cause an exception",
            command=self.cause_exception)
        b.pack()

    def cause_exception(self):
        a = []
        a.a = 0 #A traceback makes this easy to catch and fix

if __name__ == '__main__':
    win = tk.Tk()
    app = App(win)
    win.mainloop(0)