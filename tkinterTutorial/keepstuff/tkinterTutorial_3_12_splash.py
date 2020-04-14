
# -*- coding: utf -8 -*-
from tkinter import Tk, Toplevel , PhotoImage , BOTH
from tkinter.ttk import Frame , Label , Button
"""
ZetCode Tkinter e-book
This script creates a splash screen before
displaying the main application window.
Author: Jan Bodnar
Last modified: November 2015
Website: www.zetcode.com
"""

class MySplash(Toplevel):
    def __init__(self , parent):
        Toplevel.__init__(self)
        self.delay = 3000
        self.parent = parent
        self.initUI()


    def initUI(self):
        self.splash_image = PhotoImage(file="C:/pythonSecondTutorial/tkinterTutorial/battery.gif")
        w = self.splash_image.width()
        h = self.splash_image.height()
        
        self.overrideredirect(True)
        
        x = (self.parent.winfo_screenwidth() - w) / 2
        y = (self.parent.winfo_screenheight () - h) / 2
        self.geometry('{0}x{1}+{2}+{3}'.format(w, h, int(x), int(y)))
        self.splash_label = Label(self , image=self.splash_image)
        self.splash_label.pack()
        self.after(self.delay , self.close)


    def close(self):
        self.parent.build_app()
        self.destroy()


class Example(Frame):
    def __init__(self , parent):
        Frame.__init__(self , name="frame")
        self.parent = parent
        self.initUI()


    def initUI(self):
        self.pack(fill=BOTH , expand=True)
        self.parent.title('Application')
        self.parent.withdraw()
        self.showSplashScreen()
    
        
    def build_app(self):
        self.quitButton = Button(self , text='Quit', command=self.quit)
        self.quitButton.pack(padx=10, pady=10)
        self.parent.deiconify()


    def showSplashScreen(self):
        MySplash(self)



def main():
    root = Tk()
    root.geometry('250x200+300+300')
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()