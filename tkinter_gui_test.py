import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        winWidth = 800
        winHeight = 600

        screenWidth = self.master.winfo_screenwidth()
        screenHeight = self.master.winfo_screenheight()

        x = int((screenWidth - winWidth) / 2)
        y = int((screenHeight - winHeight) / 2)

        self.master.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))

        self.master.title("ADC Analysis GUI")
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=3)
        self.master.columnconfigure(0, weight=3)
        self.master.columnconfigure(1, weight=1)

        self.frame1 = tk.Frame(self.master)
        self.frame2 = tk.Frame(self.master)
        self.frame3 = tk.Frame(self.master)

        self.label1 = tk.Button(self.frame1,text="Frame1",bg='yellow').pack()
        self.label2 = tk.Button(self.frame2,text="Frame2",bg='green').pack()
        self.label3 = tk.Button(self.frame3,text="Frame3",bg='blue').pack()

        # self.frame1.grid(row=0,columnspan=5,sticky=tk.NSEW)
        # self.frame2.grid(column=1, row=1,sticky=tk.NSEW)
        # self.frame3.grid(column=2, row=2,sticky=tk.NSEW)
        
        tk.Button(self.master,text='0,0').grid(column=0,row=0,columnspan=2,sticky=tk.NSEW)
        tk.Button(self.master,text='0,1').grid(column=0,row=1,sticky=tk.NSEW)
        tk.Button(self.master,text='1,1').grid(column=1,row=1,sticky=tk.NSEW)

    def say_hi(self):
        print("hi there, everyone!")


if __name__ == '__main__':
    win = tk.Tk()
    app = Application(master=win)

    app.mainloop()
