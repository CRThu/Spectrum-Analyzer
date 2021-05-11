import tkinter

import numpy as np
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure

def on_key_event(event,canvas,ax):
    print(f"you pressed {event.key}")
    ax.plot(t, 30 * np.sin(2 * np.pi * t))
    canvas.draw()
    return

def _quit(root):
    root.quit()
    root.destroy()

root = tkinter.Tk()
root.wm_title("Embedding in Tk")

fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot()

t = np.arange(0, 3, .01)
ax.plot(t, 2 * np.sin(2 * np.pi * t))

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()

canvas.mpl_connect(
   "key_press_event", func=lambda event: on_key_event(event,canvas,ax))

canvas.mpl_connect("key_press_event", key_press_handler)

button = tkinter.Button(master=root, text="Quit", command=lambda: _quit(root))

button.pack(side=tkinter.BOTTOM)
toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

tkinter.mainloop()
