import os
from tkinter.font import Font
from matplotlib import pyplot
from numpy.core.fromnumeric import size

from fftplot import fftplot
import tkinter as tk
from tkinter.filedialog import askopenfilename
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import numpy as np

import data_decode as dec
import fftplot as f

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.defaultdir = './'
        self.create_widgets()

    def _quit(self):
        self.master.quit()
        self.master.destroy()

    def choose_datafile(self):
        fn = askopenfilename(
            title='Please choose a data file.', initialdir=self.defaultdir)
        self.defaultdir=os.path.dirname(fn)
        self.filepath.set(fn)

    def update_canvas(self):
        self.fig.gca().clear()
        self.gen_fig(self.fig.gca(), self.filepath.get())
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
        tk.Entry(master=self.frame1,).grid(
            row=1, column=1, padx=10, pady=10, columnspan=3, sticky=tk.EW)
        tk.Button(master=self.frame1, text="Open",
                  command=lambda: self.choose_datafile()).grid(
            row=2, column=0, padx=10, pady=10, sticky=tk.EW)
        tk.Button(master=self.frame1, text="Update",
                  command=lambda: self.update_canvas()).grid(
            row=2, column=1, padx=10, pady=10, sticky=tk.EW)

        # FRAME2
        # pack_toolbar=False will make it easier to use a layout manager later on.
        self.fig = self.init_fig()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame2)
        self.canvas.draw()
        toolbar = NavigationToolbar2Tk(
            self.canvas, self.frame2, pack_toolbar=False)
        toolbar.update()

        toolbar.pack(expand=1, fill=tk.X)
        self.canvas.get_tk_widget().pack(padx=10, pady=10, expand=1, fill=tk.BOTH)

        # FRAME3
        self.reporttext = tk.Text(master=self.frame3)
        self.reporttext.pack(padx=10, pady=10, expand=1, fill=tk.BOTH)
        tk.Button(master=self.frame3, text="Quit",
                  command=lambda: self._quit()).pack(padx=10, pady=10)

    def init_fig(self):
        fig = pyplot.figure(figsize=(8, 5))
        ax = fig.gca()
        ax.set_title('Init Figure', fontsize=16)
        ax.grid(True, which='both')
        ax.plot([0, 1, 2, 3, 4, 5])
        return fig

    def gen_fig(self, axes, filepath):
        fs = 200000
        FS = 10  # +/-10V

        vbias = 0
        Zoom_fin = 1000

        adc_sample = dec.data_decode(filepath, base='hex',
                                     encode='offset', adcbits=16, fullscale=FS, vbias=vbias)

        f.fftplot(signal=adc_sample, samplerate=fs, Nomalized='dBFS', fullscale=FS, window='HFT248D',
                  zoom='Part', zoom_expfin=Zoom_fin,
                  HDx_max=5,
                  PlotT=False, PlotSA=True, PlotSP=False,
                  axes=axes, override_print=lambda s: self.update_tktext(self.reporttext, s))


if __name__ == '__main__':
    win = tk.Tk()
    win.wm_title("Embedding in Tk")
    app = Application(master=win)

    app.mainloop()
    win.quit()
