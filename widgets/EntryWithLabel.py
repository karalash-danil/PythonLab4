import tkinter as tk
from tkinter import ttk

class EntryWithLabel(ttk.Frame):
    def __init__(self, *args,text="", textvariable:tk.StringVar=None,**kwargs):
        super().__init__(*args,**kwargs)
        self.label = ttk.Label(self, text=text)
        self.label.pack(side="left")

        if textvariable == None:
            self.textvariable = tk.StringVar()
        else:
            self.textvariable = textvariable
        self.input = ttk.Entry(self, textvariable=self.textvariable)
        self.input.pack(side="right",fill="both",expand=True)

    def get(self):
        return self.input.get()