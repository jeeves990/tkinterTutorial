

import tkinter as tk
import sys
import winreg as winreg


class JustOneLevel4_1_hive:
    def __init__(self, lbox):
        aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
        (numsubkeys, numvalues, lastmod) = QueryInfoKey(aKey)
        aString = "# subkeys: {0}, # values: {1}".format(numsubkeys, numvalues)
        lbox.insert('end', aString)

        i = 0
        keyname = EnumKey(aKey, i)
        print(keyname)
        for i in range(0, numsubkeys -1):
            try:
        
                asubkey = OpenKey(aKey, keyname)
                try:
                    val = QueryValueEx(asubkey, "DisplayName")
                    aString = "\t{0}".format(str(val))
                    lbox.insert('end', aString)
                except:
                    aString = "-----{0}_____".format(keyname)
                    lbox.insert('end', aString)
                i += 1
                keyname = EnumKey(aKey, i)
            except WindowsError:
                break


if __name__ == '__main__':
    win = tk.Tk()
    x = 500
    y = 500
    win.geometry('+{0}+{1}'.format(x,y))
    win.attributes('-topmost', 1)
    lbox = InitUI(win).bldBase()
    JustOneLevel4_1_hive(lbox)
    win.mainloop()

    
