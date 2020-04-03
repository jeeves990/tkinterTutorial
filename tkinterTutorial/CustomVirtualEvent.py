# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:14:20 2020

@author: FBA_S
"""

#Custom Virtual Event

try:
    from Tkinter import *
    import tkMessageBox
except ImportError:
    try:
        from tkinter import *
        from tkinter import messagebox
    except Exception:
        pass

import time
from threading import Thread

VirtualEvents=["<<APP_DATA>>","<<POO_Event>>"]

def TS_decorator(func):
    def stub(*args, **kwargs):
        func(*args, **kwargs)

    def hook(*args,**kwargs):
        Thread(target=stub, args=args).start()

    return hook

class myApp:
    def __init__(self):
        self.root = Tk()
        self.makeWidgets(self.root)
        self.makeVirtualEvents()
        self.state=False
        self.root.attributes('-topmost', 1)
        self.root.geometry('+800+500')
        self.root.mainloop()

    def makeWidgets(self,parent):
        self.lbl=Label(parent, width = 45)
        self.lbl.pack()
        Button(parent,text="Get Data",command=self.getData).pack()

    def onVirtualEvent(self,event):
        print("Virtual Event Data: {}".format(event.VirtualEventData))
        self.lbl.config(text=event.VirtualEventData)

    def makeVirtualEvents(self):
        for e in VirtualEvents:
            self.root.event_add(e,'None') #Can add a trigger sequence here in place of 'None' if desired
            self.root.bind(e, self.onVirtualEvent,"%d")

    def FireVirtualEvent(self,vEvent,data):
        Event.VirtualEventData=data
        self.root.event_generate(vEvent)


    def getData(self):
        if not self.state:
            VirtualServer(self)
        else:
            pooPooServer(self)

        self.state = not self.state


@TS_decorator
def VirtualServer(m):
    time.sleep(3)
    m.FireVirtualEvent(VirtualEvents[0],"Hello From Virtual Server")

@TS_decorator
def pooPooServer(m):
    time.sleep(3)
    m.FireVirtualEvent(VirtualEvents[1],"Hello From Poo Poo Server")


if __name__=="__main__":
    app=myApp()
    