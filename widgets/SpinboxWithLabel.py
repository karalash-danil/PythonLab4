import tkinter as tk
from sys import prefix
from tkinter import ttk

class SpinboxWithLabel(ttk.Frame):
    def __init__(self, *args, text="", textvariable:tk.StringVar=None, from_=0, to=999,**kwargs):
        super().__init__(*args,**kwargs)
        self.label = ttk.Label(self, text=text)
        self.label.pack(side="left")

        if textvariable == None:
            self.textvariable = tk.StringVar()
        else:
            self.textvariable = textvariable
        self.input = ttk.Spinbox(self, textvariable=self.textvariable, from_=from_, to=to)
        self.input.pack(side="right",fill="both",expand=True)

    def get(self):
        return self.input.get()