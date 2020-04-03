# -*- coding: utf -8 -*-
"""
        ZetCode Tkinter e-book
        In this script , we show how to
        use the Scale widget.
        Author: Jan Bodnar
        Last modified: November 2015
        Website: www.zetcode.com
"""
import tkinter as tk
from tkinter import Tk, BOTH , IntVar , LEFT, ttk
from tkinter.ttk import Frame , Label , Scale, Style, Spinbox, LabelFrame

class Example(ttk.LabelFrame):
    def __init__(self , parent):
        LabelFrame.__init__(self , parent)
        self['text'] = 'My LabelFrame'

        self.parent = parent
        self.style = Style()
        
        self.bldScrollbarStyle()

        ##self.printStuff("My.Horizontal.TScrollbar")
       
        self.initUI("My.Horizontal.TScrollbar")
        self.bldSpinbox()
        self.bldOptionMenu()
        self.bldComboBox()


    def bldComboBox(self):
        sepcb= ttk.Separator(self.parent, orient = 'horizontal')
        sepcb.pack(side = 'top', anchor = 'sw', fill = 'both', expand = 1)

        cbFrm = tk.LabelFrame(self.parent, text = 'ComboBox')
        cbFrm.pack(side = 'top', fill = 'both', expand = 1)

        self.cvar = tk.StringVar()
        combo = ttk.Combobox(cbFrm , textvariable=self.cvar)


        """      either of the following work to create the event     """
        ##combo.event_generate("<<ComboboxSelected>>", when = 'tail')
        combo.event_add("<<ComboboxSelected>>", "Button-1")
     
        combo.bind("<<ComboboxSelected>>", self.onComboSelect)

        combo['values'] = ('OpenBSD', 'NetBSD', 'FreeBSD')
        combo.current (0)
        combo.pack(side=LEFT, padx=15)

        self.lcbvar = tk.StringVar()
        self.lcbvar.set("OpenBSD")
        lbl = Label(cbFrm , textvariable=self.lcbvar)
        lbl.pack(side=LEFT)


    def onComboSelect(self, e):
        w = e.widget
        self.lcbvar.set(w.get())


    def bldOptionMenu(self):
        sepOpt= ttk.Separator(self.parent, orient = 'horizontal')
        sepOpt.pack(side = 'bottom', anchor = 'sw', fill = 'both', expand = 1)

        optFrm = tk.LabelFrame(self.parent, text = 'OptionMenu')
        optFrm.pack(side = 'bottom', fill = 'both', expand = 1)
        
        self.optvar = tk.StringVar()
        options = ["OpenBSD", "NetBSD", "FreeBSD"]

        om = ttk.OptionMenu(optFrm , self.optvar , options[0], *options , command=self.onOptSelect)
        om.pack(side=LEFT , padx=5)   ##, fill = 'left')

        self.loptvar = tk.StringVar()
        self.loptvar.set("OpenBSD")
        lbl = Label(optFrm , textvariable=self.loptvar)
        lbl.pack(side=LEFT)

        filfrm = tk.Frame(optFrm, relief = 'groove', background = 'light pink') #optFrm['bg'])
        filfrm.pack(side = 'left', padx = 10, fill = 'both', expand = 1, anchor = 'w')

        ttk.Separator(optFrm, orient = 'horizontal').pack(side='bottom', anchor = 'sw', fill = 'both', expand = 1)
        Label(filfrm, text = '---'*40).pack(side = 'left', anchor = 'w', fill = 'both', expand = 1)

        
    def onOptSelect(self, a):
        self.loptvar.set(a)


    def bldSpinbox(self):
        frm = LabelFrame(self.parent, text = 'Spinbox')
        frm.pack(side = 'top', fill = 'both', expand = 1)

        self.spBox = Spinbox(frm, from_=0, to=100, command=self.spinboxOnClick)
        self.spBox.pack(side=LEFT, fill = 'both', expand = 1, padx=15, )

        self.var = IntVar()
        self.label = Label(frm , text=0, textvariable=self.var)
        self.label.pack(side=LEFT)


    def spinboxOnClick(self):
        val = self.spBox.get()
        self.var.set(val)


    def initUI(self, stylename):
        self.parent.title("Scale")
        self.pack(fill=BOTH , expand=1)
        
        sep = ttk.Separator(self, orient = 'horizontal')
        ##sep.pack(anchor = 'nw', side = 'left', fill = 'x', expand = 1)
        sep.grid(row = 0, column = 0, sticky = 'new')
        
        scale = Scale(self, orient = 'horizontal', from_=0, to=100, command=self.onScale)
        ##scale.config(weight = 5)
        ##scale.pack(side=LEFT, padx=15, fill = BOTH, anchor = 'w', expand = 1)
        scale.grid(row = 1, column = 0, sticky = 'new')

        self.var = IntVar()
        self.label = Label(self , text=0, textvariable=self.var)
        ##self.label.pack(side=LEFT)
        self.label.grid(row = 1, column = 1, sticky = 'new')
    
        sep1 = ttk.Separator(self, orient = 'horizontal')
        ##sep1.pack(anchor = 'nw', fill = 'both', expand = 1)
        sep1.grid(row = 2, sticky = 'new')
       
        lbl = Label(self, text = '---'*40)
        ##lbl.pack()
        lbl.grid(row = 3, sticky = 'news')

        ##lbl.pack(side = 'left', fill = 'both', expand = 1)


    def onScale(self , val):
        v = int(float(val))
        self.var.set(v)


    def bldScrollbarStyle(self):
        # import the 'trough' element from the 'default' engine.
        self.style.element_create("My.Horizontal.Scrollbar.trough", "from", "default")

        # Redefine the horizontal scrollbar layout to use the custom trough.
        # This one is appropriate for the 'vista' theme.
        """
        self.style.layout("My.Horizontal.TScrollbar",
            [('My.Horizontal.Scrollbar.trough', {'children':
                [('Horizontal.Scrollbar.leftarrow', {'side': 'left', 'sticky': ''}),
                 ('Horizontal.Scrollbar.rightarrow', {'side': 'right', 'sticky': ''}),
                 ('Horizontal.Scrollbar.thumb', {'unit': '1', 'children':
                     [('Horizontal.Scrollbar.grip', {'sticky': ''})],
                'sticky': 'news'})],
            'sticky': 'we'})])
        """
        # Copy original style configuration and add our new custom configuration option.
        self.style.configure("My.Horizontal.TScrollbar", troughcolor="red")
        self.style.configure("My.Horizontal.TScrollbar", self.style.configure("Horizontal.TScrollbar"))
        
        
    def printStuff(self, stylename):
        style = self.style
        layout = str(style.layout(stylename))
        print('Stylename = {}'.format(stylename))
        print('Layout    = {}'.format(layout))
        elements=[]
        for n, x in enumerate(layout):
            if x=='(':
                element=""
                for y in layout[n+2:]:
                    if y != ',':
                        element=element+str(y)
                    else:
                        elements.append(element[:-1])
                        break
        print('\nElement(s) = {}\n'.format(elements))

        # Get options of widget elements
        for element in elements:
            print('{0:30} options: {1}'.format(
                element, style.element_options(element)))

def main():
    root = Tk()
    ex = Example(root)
    root.geometry("+300+300")
    root.attributes('-topmost', 1)
    root.mainloop()

if __name__ == '__main__':
    main()

