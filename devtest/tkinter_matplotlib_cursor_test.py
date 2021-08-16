import tkinter
import matplotlib

import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

x = np.arange(0, 2, 0.1)
y = 2 * np.sin(2 * np.pi * x)

def _quit(root):
    root.quit()
    root.destroy()

def scroll(event):
    axtemp = event.inaxes
    x_min, x_max = axtemp.get_xlim()
    fanwei_x = (x_max - x_min) / 10
    if event.button == 'up':
        axtemp.set(xlim=(x_min + fanwei_x, x_max - fanwei_x))
    elif event.button == 'down':
        axtemp.set(xlim=(x_min - fanwei_x, x_max + fanwei_x))
    fig.canvas.draw_idle()

def motion(event):
    try:
        line_x.set_ydata(event.ydata)
        line_y.set_xdata(event.xdata)

        text0.set_position((event.xdata, event.ydata))
        text0.set_text('%f,%f'%(event.xdata, event.ydata))

        canvas.draw_idle()
    except:
        pass


root = tkinter.Tk()
root.wm_title("Embedding in Tk")

fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot()

len_y = len(y)
_y = [y[0]]*len_y

 
ax.plot(x, y, color='blue')

line_x = ax.axhline(y=y[0], color='skyblue')
line_y = ax.axvline(x=x[0], color='skyblue')
text0 = ax.text(x=x[0],y=y[0],s=str(y[0]),fontsize = 10)

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()

canvas.mpl_connect('scroll_event', scroll)
canvas.mpl_connect('motion_notify_event', motion)
button = tkinter.Button(master=root, text="Quit", command=lambda: _quit(root))

button.pack(side=tkinter.BOTTOM)
toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

tkinter.mainloop()
