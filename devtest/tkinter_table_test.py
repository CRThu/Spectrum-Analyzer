import tkinter
from tkintertable import TableCanvas, TableModel
from tkinter import *

master = tkinter.Tk()
master.geometry('400x500')

tframe = Frame(master)
tframe.pack(expand=1,fill=BOTH)

data = {'rec1': {'col1': 99.88, 'col2': 108.79, 'label': 'rec1'},
        'rec2': {'col1': 99.88, 'col2': 108.79, 'label': 'rec2'}
        }

model = TableModel()
table = TableCanvas(tframe, model=model)
table.show()

model = table.model
model.importDict(data) 
table.redraw()

master.mainloop()
