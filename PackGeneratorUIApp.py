from tkinter import *
from tkinter import ttk

from AIPackGenerator import PackGenerator, PackDecorator

class AIGenWindow:

    def __init__(self, root):
        root.title('AI Resource Pack Generator')

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

root = Tk()
AIGenWindow(root)
root.mainloop()