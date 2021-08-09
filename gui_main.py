from gui_set_params import SetParamsDialog
from matplotlib.figure import Figure
import numpy as np
from cmd_parse import DATA_DECODE_ARGS, FFTPLOT_ARGS, args_filter, cmd_parse
import os
import tkinter as tk
from tkinter.filedialog import askopenfilename
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import data_decode as dec
import fftplot as f


# --fullscale=10 --base=hex --encode=offset --adcbits=16 --vbias=0 --samplerate=200000 --nomalized=dBFS --window=HFT248D --zoom=Part --fin=1000 --hdmax=5 --plottime=False --plotspectrum=True --plotphase=False --impedance=600

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.defaultdir = './'
        self.default_argvs = '--base=hex --adcbits=16 --fullscale=10 --samplerate=200000 --hdmax=5 --window=HFT248D'
        self.create_widgets()

    def _quit(self):
        self.master.quit()
        self.master.destroy()

    def bind_rightkeyevent(self, root, control):
        control.bind(
            "<Button-3>", lambda event: self.rightkeyevent(event, root, control))

    def rightkeyevent(self, event, master, control):
        menu = tk.Menu(master, tearoff=False)
        menu.delete(0, tk.END)
        menu.add_command(
            label='Cut', command=lambda: control.event_generate("<<Cut>>"))
        menu.add_command(
            label='Copy', command=lambda: control.event_generate("<<Copy>>"))
        menu.add_command(
            label='Paste', command=lambda: control.event_generate('<<Paste>>'))
        menu.post(event.x_root, event.y_root)

    def choose_datafile(self):
        fn = askopenfilename(
            title='Please choose a data file.', initialdir=self.defaultdir)
        self.defaultdir = os.path.dirname(fn)
        self.filepath.set(fn)

    def set_params(self):
        setParamsDialog = SetParamsDialog(params=self.argvs.get())
        self.master.wait_window(setParamsDialog)
        self.argvs.set(setParamsDialog.paramsinfo)

    def update_canvas(self):
        argvs_dict = cmd_parse(self.argvs.get())
        if 'filepath' not in argvs_dict:
            argvs_dict['filepath'] = self.filepath.get()
        # print(argvs_dict)
        self.fig.clf()
        axes = self.fig.gca()
        self.axes_defaultcfg(axes)
        self.gen_fig(axes, argvs_dict)
        self.canvas.draw()

    def update_tktext(self, text: tk.Text, s: str):
        text.delete('1.0', tk.END)
        text.insert(tk.INSERT, s)

    def create_widgets(self):
        winWidth = 990
        winHeight = 660

        screenWidth = self.master.winfo_screenwidth()
        screenHeight = self.master.winfo_screenheight()

        x = int((screenWidth - winWidth) / 2)
        y = int((screenHeight - winHeight) / 2)

        self.master.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))

        self.master.title("ADC Analysis GUI")
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=3)
        self.master.columnconfigure(0, weight=5)
        self.master.columnconfigure(1, weight=3)

        self.frame1 = tk.Frame(self.master)
        self.frame2 = tk.Frame(self.master)
        self.frame3 = tk.Frame(self.master)

        self.frame1.grid(column=0, row=0, columnspan=2, sticky=tk.NSEW)
        self.frame2.grid(column=0, row=1, sticky=tk.NSEW)
        self.frame3.grid(column=1, row=1, sticky=tk.NSEW)
        self.frame1.grid_propagate(0)
        self.frame2.pack_propagate(0)
        self.frame3.pack_propagate(0)

        # FRAME1
        self.filepath = tk.StringVar()
        self.argvs = tk.StringVar(value=self.default_argvs)
        self.frame1.columnconfigure(0, weight=1)
        self.frame1.columnconfigure(1, weight=1)
        self.frame1.columnconfigure(2, weight=1)
        self.frame1.columnconfigure(3, weight=5)

        tk.Label(master=self.frame1, text="Path:").grid(
            row=0, column=0, padx=10, pady=10, sticky=tk.W)
        tk.Entry(master=self.frame1, textvariable=self.filepath).grid(
            row=0, column=1, padx=10, pady=10, columnspan=3, sticky=tk.EW)
        tk.Label(master=self.frame1, text="Params:").grid(
            row=1, column=0, padx=10, pady=10, sticky=tk.W)
        tk.Entry(master=self.frame1, textvariable=self.argvs).grid(
            row=1, column=1, padx=10, pady=10, columnspan=3, sticky=tk.EW)
        tk.Button(master=self.frame1, text="Open...",
                  command=lambda: self.choose_datafile()).grid(
            row=2, column=0, padx=10, pady=10, sticky=tk.EW)
        tk.Button(master=self.frame1, text="Set Params",
                  command=lambda: self.set_params()).grid(
            row=2, column=1, padx=10, pady=10, sticky=tk.EW)
        tk.Button(master=self.frame1, text="Update",
                  command=lambda: self.update_canvas()).grid(
            row=2, column=2, padx=10, pady=10, sticky=tk.EW)

        # FRAME2
        # pack_toolbar=False will make it easier to use a layout manager later on.
        self.init_fig()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame2)
        self.canvas.draw()
        toolbar = NavigationToolbar2Tk(
            self.canvas, self.frame2, pack_toolbar=False)
        toolbar.update()

        toolbar.pack(expand=1, fill=tk.X, side=tk.BOTTOM)
        self.canvas.get_tk_widget().pack(
            padx=10, pady=10, expand=1, fill=tk.BOTH, side=tk.TOP)

        # FRAME3
        self.reporttext = tk.Text(master=self.frame3)
        self.reporttext.pack(padx=10, pady=10, expand=1, fill=tk.BOTH)
        self.bind_rightkeyevent(self.frame3, self.reporttext)
        tk.Button(master=self.frame3, text="Quit",
                  command=lambda: self._quit()).pack(ipadx=10, padx=10, pady=10)

    def axes_defaultcfg(self, axes):
        axes.format_coord = self.format_coord

    def init_fig(self):
        self.fig = Figure(figsize=(8, 5), dpi=100)
        ax = self.fig.gca()
        self.axes_defaultcfg(ax)
        ax.set_title('Init Figure', fontsize=16)
        ax.grid(True, which='both')
        ax.plot([0, 1, 4, 9, 16, 25])
        ax.plot([0, 1, 8, 27, 64, 125])
        ax.plot([0, 1, 16, 81, 256, 625])

    def format_coord(self, cursorx, cursory):
        liney = []
        axes = self.fig.gca()
        for line2d in axes.get_lines():
            datax = line2d.get_xdata()
            indexx = np.searchsorted(datax, cursorx)
            if indexx == len(datax):
                indexx -= 1
            linex = datax[indexx]
            liney.append(line2d.get_ydata()[indexx])

        strout = '(%g, %s)' % (linex, ', '.join('%g' % yi for yi in liney))
        return strout

    def gen_fig(self, axes, args: dict):
        data_decode_kwargs = args_filter(args, DATA_DECODE_ARGS)
        adc_sample = dec.data_decode(**data_decode_kwargs)

        fftplot_kwargs = args_filter(args, FFTPLOT_ARGS)
        f.fftplot(signal=adc_sample, axes=axes,
                  override_print=lambda s: self.update_tktext(self.reporttext, s), **fftplot_kwargs)


if __name__ == '__main__':
    win = tk.Tk()
    win.wm_title("Embedding in Tk")
    app = Application(master=win)

    app.mainloop()

    win.quit()