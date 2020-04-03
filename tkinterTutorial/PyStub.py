
import sys
import tkinter as tk
from tkinter.ttk import *

class InitGUI(tk.Frame):
    def __init__(self, win):
        tk.Frame.__init__(self, win)
        self.pack(fill = 'both', expand = True)
        win.lbl = tk.Label(win, text=sys.argv[0])
        win.lbl.configure(relief='groove')
        win.lbl.pack(fill='x', expand=True, anchor='nw', side='top', padx=3, pady=3)


def main():
    win = tk.Tk()

    def versionInfo(win):
        try:
            if win.lbl:
                pass
        except:
            return

        from sys import version_info

        verstr: str = '{} ({}.{})'.format(sys.argv[0], version_info.major, version_info.minor)
        if version_info.major == 3:
            pass

        elif version_info.major == 2:
            try:
                input = raw_input
            except NameError:
                pass
        else:
            print("Unknown python version - input function not safe")
        win.lbl['text'] = verstr

    versionInfo(win)

    InitGUI(win)
    win.attributes('-topmost', 1)
    win.geometry("+300+300")
    win.mainloop()

if __name__ == '__main__':
    main()

