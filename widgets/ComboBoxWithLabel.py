import tkinter as tk
from tkinter import ttk

from Utils import ListsDataBase

class ComboBoxWithLabel(ttk.Frame):
    def __init__(self, parent, id, *args,**kwargs):
        super().__init__(parent, *args,**kwargs)

        self.object = ListsDataBase().get(id)

        self.label = ttk.Label(self, text=self.object.name+": ")
        self.label.pack(side="left")

        self.textvariable = tk.StringVar()

        self.comboBox = ttk.Combobox(self, textvariable=self.textvariable)
        self.comboBox.pack(side="right",fill="both",expand=True)

        def callback(*args):
            self.refresh()

        self.bind("<Enter>", callback)

        self.refresh()


    def refresh(self):
        self.comboBox["values"] = self.object.values

    def get(self):
        return self.textvariable.get()

    def get_index(self):
        return self.object.values.index(self.get())