
from tkinter import messagebox as MSGBOX
import os
import psutil


process = psutil.Process(os.getpid())
print(process.memory_percent())


def setColRowWeight(obj, col_weight = 1, row_weight = 1, **kwargs):
    try:
        colCount, rowCount = obj.grid_size()
            
        if 'colCount' in kwargs:
            colCount = kwargs['colCount']
        if 'rowCount' in kwargs:
            rowCount = kwargs['rowCount']

        for i in range(0, rowCount):
            obj.grid_rowconfigure(i, weight = row_weight)

        for i in range(0, colCount):
            obj.grid_columnconfigure(i, weight = col_weight)
    except Exception as e:
        msg = 'setColRowWeight: has failed with [{}]'.format(e.args)
        MSGBOX.showinfo('Exception: non fatal', msg)


def get_widget_attributes(widgetParent):
    return(0)
    #aList = list(widgetParent.children.values()) 
    #lst = widgetParent.children()

    for key in widgetParent.children.items():
        print('key = [{0}] and value = [{1}]'.format(key, ''))
    all_widgets = widgetParent.winfo_children()
    for widg in all_widgets:
        print('\nWidget Name: {}'.format(widg.winfo_class()))
        keys = widg.keys()
        for key in keys:
            print("Attribute: {:<20}".format(key), end=' ')
            value = widg[key]
            vtype = type(value)
            print('Type: {:<30} Value: {}'.format(str(vtype), value))

if __name__ == '__main__':
    from tkinter import Tk, Frame, Label, Button, Canvas

    win = Tk()
    frm = Canvas(win)
    frm.pack()
    for i in range(0, 5):
        Label(frm, text = "number is {0}".format(i)).pack()

    Button(frm, text = 'click', command = onClick).pack()

    win.mainloop()
