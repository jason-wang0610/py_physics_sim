import tkinter as tk

class Controls:
    def __init__(self):
        self.master = tk.Tk()
        b = tk.Button(self.master, text="hello", command=self.hello)
        b.pack()
        tk.mainloop()
    def hello(self):
        print('hello')

control_panel = Controls()
