from matplotlib.pyplot import fill
from tkintertable.Prefs import Preferences
from cmd_parse import ARGVS_LIST, cmd_parse
import tkinter as tk
from tkintertable import TableCanvas, TableModel
from tkinter import *


class SetParamsDialog(tk.Toplevel):
    def __init__(self, params=None):
        super().__init__()
        winWidth = 800
        winHeight = 600

        screenWidth = self.master.winfo_screenwidth()
        screenHeight = self.master.winfo_screenheight()

        x = int((screenWidth - winWidth) / 2)
        y = int((screenHeight - winHeight) / 2)

        self.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
        self.title('Set params Dialog')
        self.paramsinfo = None
        self.init_gui(params)

    def init_gui(self, params=None):
        # draw table
        tktframe = Frame(self)
        tktframe.pack(padx=10, pady=10, expand=1, fill=tk.BOTH)

        # draw buttons
        btnsframe = tk.Frame(self)
        btnsframe.pack(fill=X)
        tk.Button(btnsframe, text="Cancel", command=self.cancel).pack(
            ipadx=10, padx=10, pady=10, side=RIGHT)
        tk.Button(btnsframe, text="Ok", command=self.ok).pack(
            ipadx=10, padx=10, pady=10, side=RIGHT)

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
        table = TableCanvas(tktframe, model=self.model)

        perf = {'textsize': 14, 'windowwidth': 800,
                'windowheight': 600, 'rowheight': 30}
        preferences = Preferences('SetParamsDialog', perf)
        table.loadPrefs(preferences)

        table.show()

        model = table.model
        model.importDict(data)
        # model.addColumn(colname='param')
        table.redraw()

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
