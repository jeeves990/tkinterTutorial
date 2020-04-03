
from tkinter import messagebox as MSGBOX

def setColRowWeight(obj, col_weight = 1, row_weight = 1):
    try:
        colCount, rowCount = obj.grid_size()
    
        for i in range(rowCount):
            obj.grid_rowconfigure(i, weight = row_weight)

        for i in range(colCount):
            obj.grid_columnconfigure(i, weight = col_weight)
    except Exception as e:
        msg = 'setColRowWeight has failed with [{0}]'.format(e.args)
        MSGBOX.showinfo('Exception', msg)


if __name__ == '__main__':
    from tkinter import Tk, Frame, Label, Button, Canvas

    win = Tk()
    frm = Canvas(win)
    frm.pack()
    for i in range(0, 5):
        Label(frm, text = "number is {0}".format(i)).pack()

    Button(frm, text = 'click', command = onClick).pack()

    win.mainloop()
