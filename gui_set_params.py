from cmd_parse import ARGVS_LIST, cmd_parse
import tkinter as tk
from tkintertable import TableCanvas, TableModel
from tkinter import *


class SetParamsDialog(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Set params')

        self.init_gui()

    def __init__(self, params=None):
        super().__init__()
        self.title('Set params')

        self.init_gui(params)

    def init_gui(self, params=None):
        # draw table
        tframe = Frame(self)
        tframe.pack(fill="x")

        # subkeys = ['argv', 'dest', 'type', 'help']
        # data_tostr = []
        # for dic in ARGVS_LIST:
        #     newdict = sub_dict(dic, subkeys)
        #     newdict['type'] = newdict['type'].__name__
        #     newdict['param'] = ''
        #     data_tostr.append(newdict)

        # data = dict(zip(range(len(data_tostr)), data_tostr))

        subkeys = ['argv', 'dest', 'type', 'help']
        data = dict()
        for dic in ARGVS_LIST:
            newdict = sub_dict(dic, subkeys)
            newdict['type'] = newdict['type'].__name__
            newdict['param'] = ''

            dickey = newdict['dest']
            data[dickey] = newdict

        # parse params
        print('input params:', params)
        argvs_dict = cmd_parse(params)
        for k, v in argvs_dict.items():
            data[k]['param'] = str(v)

        self.model = TableModel()
        table = TableCanvas(tframe, model=self.model)
        table.show()

        model = table.model
        model.importDict(data)
        # model.addColumn(colname='param')
        table.redraw()

        # buttons
        row3 = tk.Frame(self)
        row3.pack(fill="x")
        tk.Button(row3, text="Cancel", command=self.cancel).pack(side=tk.RIGHT)
        tk.Button(row3, text="Ok", command=self.ok).pack(side=tk.RIGHT)

    def ok(self):
        # find dict with no empty 'param' key
        # get argv and param key only to the new dict
        rawdata = [sub_dict(pardict, ['argv', 'param'])
                   for _, pardict in self.model.data.items()
                   if len(pardict['param']) != 0]
        self.paramsinfo = params_dict2str(rawdata)
        self.destroy()

    def cancel(self):
        self.paramsinfo = None
        self.destroy()

def sub_dict(rawdict, subkeys):
    return dict((key, value) for key, value in rawdict.items() if key in subkeys)

def params_dict2str(dic):
    return ' '.join([i['argv'] + '=' + i['param'] for i in dic])


if __name__ == '__main__':
    master = tk.Tk()
    master.geometry('400x500')

    setParamsDialog = SetParamsDialog(
        params='--base=hex --adcbits=16 --fullscale=10 --samplerate=200000 --hdmax=5 --window=HFT248D')
    master.wait_window(setParamsDialog)
    print('return params:', setParamsDialog.paramsinfo)

    master.mainloop()
