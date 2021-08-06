from cmd_parse import ARGVS_LIST
import tkinter as tk
from tkintertable import TableCanvas, TableModel
from tkinter import *


class MyDialog(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Set params')

        self.init_gui()

    def init_gui(self):
        # draw table
        tframe = Frame(self)
        tframe.pack(fill="x")

        data_stred=ARGVS_LIST
        for dic in data_stred:
            for k,v in dic.items():
                dic[k]=str(v)

        data = dict(zip(range(len(data_stred)), data_stred))

        self.model = TableModel()
        table = TableCanvas(tframe, model=self.model)
        table.show()

        model = table.model
        model.importDict(data)
        model.addColumn(colname='param')
        table.redraw()

        # buttons
        row3 = tk.Frame(self)
        row3.pack(fill="x")
        tk.Button(row3, text="Cancel", command=self.cancel).pack(side=tk.RIGHT)
        tk.Button(row3, text="Ok", command=self.ok).pack(side=tk.RIGHT)

    def ok(self):
        self.paramsinfo = self.model.getData()
        self.destroy()

    def cancel(self):
        self.paramsinfo = dict()
        self.destroy()


if __name__ == '__main__':

    master = tk.Tk()
    master.geometry('400x500')

    inputDialog = MyDialog()
    master.wait_window(inputDialog)
    print('return data:', inputDialog.paramsinfo)

    master.mainloop()
