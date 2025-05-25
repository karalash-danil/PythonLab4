import tkinter as tk
from tkinter import ttk

import sv_ttk

#------------------------

from Utils import *


class ValueEditor(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.canDetect = False

        self.Title = ttk.Label(self, text="Редагування значення", justify="center", anchor="center")
        self.Title.pack(padx=5, pady=5, fill="x")

        self.inputTextvariable = tk.StringVar()
        self.inputEdit = ttk.Entry(self, textvariable=self.inputTextvariable)
        self.inputEdit.pack(padx=5, pady=5, fill="x")

        self.deleteButton = ttk.Button(self, text=" Видалити", command=self._nametowidget(self.winfo_parent()).delete)
        self.deleteButton.pack(padx=5, pady=5, side="bottom", fill="both", expand=True)

        self.closeButton = ttk.Button(self, text=" Закрити", style="Accent.TButton", command=self._nametowidget(self.winfo_parent()).close)
        self.closeButton.pack(padx=5, pady=5, side="bottom", fill="both", expand=True)

        def callback(*args):
            if self.canDetect:
                self._nametowidget(self.winfo_parent()).save()
                print(self.inputTextvariable.get())

        self.inputTextvariable.trace_add("write", callback)

class ListsFrame(ttk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.canDetect = True

        self.Title = ttk.Label(self, text="Операції зі Списками", justify="center", anchor="center")
        self.Title.pack(padx=5, pady=5, fill="x")

        self.lists_textvariable = tk.StringVar()
        self.comboBoxLists = ttk.Combobox(self, values=ListsDataBase().getNames(), textvariable=self.lists_textvariable, state="readonly")
        self.comboBoxLists.pack(padx=5, pady=5, fill="x", expand=True)


        self.frameListBox = ttk.Frame(self)
        self.frameListBox.pack(padx=5, pady=5, fill="x")

        self.listValues = tk.Listbox(self.frameListBox)
        self.listValues.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.frameListBox, orient="vertical")
        scrollbar.config(command=self.listValues.yview)
        scrollbar.pack(side="right", fill="y")

        self.listValues.config(yscrollcommand=scrollbar.set)


        self.createButton = ttk.Button(self, text=" Створити", style="Accent.TButton", command=self._nametowidget(self.winfo_parent()).create, state="disabled")
        self.createButton.pack(padx=5, pady=5, fill="x", expand=True)

        self.bottomPanel = ttk.Frame(self)
        self.bottomPanel.pack(fill="x")

        self.reverseButton = ttk.Button(self.bottomPanel, text=" Реверсувати", command=self._nametowidget(self.winfo_parent()).reverse, state="disabled")
        self.reverseButton.pack(padx=5, pady=5, side="right", fill="both", expand=True)

        self.sortButton = ttk.Button(self.bottomPanel, text=" Відсортувати", command=self._nametowidget(self.winfo_parent()).sort, state="disabled")
        self.sortButton.pack(padx=5, pady=5, side="left", fill="both", expand=True)

        def callback(*args):
            if self.canDetect:
                self._nametowidget(self.winfo_parent()).select_list(ListsDataBase().getNames().index(self.lists_textvariable.get()))

        def callback1(event):
            if self.canDetect:
                if len(event.widget.curselection()) > 0:
                    self._nametowidget(self.winfo_parent()).open(event.widget.curselection()[0])

        self.listValues.bind("<<ListboxSelect>>", callback1)
        self.lists_textvariable.trace_add("write", callback)

class ListsEditor(ttk.Frame):
    def create(self):
        try:
            self.listsFrame.canDetect = False
            self.CurrentListData.append("Нове значення")
            self.listsFrame.canDetect = True
            self.open(self.CurrentListData.size() - 1)
        except Exception as e:
            print(e)

    def _onAdded(self, index, value):
        self.listsFrame.listValues.insert(index, value)

    def _onRemoved(self, index, value):
        self.listsFrame.listValues.delete(index)

    def _onChanged(self, index, value):
        self.listsFrame.listValues.delete(index)
        self.listsFrame.listValues.insert(index, value)
        self.listsFrame.listValues.select_set(index)

    def _onFullChanged(self):
        self.refresh_list()

    def unload(self):
        self.valueEditor.canDetect = False
        self.CurrentValue = None

    def load(self, index):
        self.unload()

        self.CurrentValue = index
        self.valueEditor.inputTextvariable.set(ListsDataBase().get(list(ListsDataBase().data.keys())[self.CurrentList]).values[self.CurrentValue])

        self.valueEditor.canDetect = True

    def save(self):
        if not(self.CurrentValue is None):
            self.listsFrame.canDetect = False
            self.CurrentListData.change(self.CurrentValue, self.valueEditor.inputTextvariable.get())
            self.listsFrame.canDetect = True

    def open(self, index):
        self.close()
        self.load(index)

        self.listsFrame.canDetect = False
        self.listsFrame.listValues.select_set(index)
        self.listsFrame.canDetect = True

        self.listsFrame.pack_forget()
        self.valueEditor.pack(anchor="w", expand=True, padx=5, pady=5, side="right")
        self.listsFrame.pack(anchor="e", expand=True, padx=5, pady=5, side="left")

    def close(self):
        self.unload()

        self.listsFrame.canDetect = False
        self.listsFrame.listValues.select_clear(0, "end")
        self.listsFrame.canDetect = True

        self.valueEditor.pack_forget()
        self.listsFrame.pack_forget()
        self.listsFrame.pack(expand=True, padx=5, pady=5, side="left")

    def delete(self):
        temp = self.CurrentValue
        self.close()
        self.CurrentListData.pop(temp)

    def refresh_list(self):
        self.listsFrame.canDetect = False

        self.listsFrame.listValues.delete(0, "end")
        for i in self.CurrentListData.values:
            self.listsFrame.listValues.insert(tk.END, i)
            if self.CurrentValue is not None:
                if i == self.valueEditor.inputTextvariable.get():
                    index = self.CurrentListData.index(self.valueEditor.inputTextvariable.get())
                    self.listsFrame.listValues.select_set(index)
                    self.CurrentValue = index

        self.listsFrame.canDetect = True

    def sort(self):
        self.listsFrame.canDetect = False
        self.CurrentListData.sort()
        self.listsFrame.canDetect = True

    def reverse(self):
        self.listsFrame.canDetect = False
        self.CurrentListData.reverse()
        self.listsFrame.canDetect = True

    def select_list(self, index):
        self.close()
        self.valueEditor.canDetect = False
        self.CurrentList = index

        if self.CurrentListData is not None:
            if self.CurrentListData._AddedValue.has(self._onAdded):
                self.CurrentListData._AddedValue.remove(self._onAdded)
            if self.CurrentListData._RemovedValue.has(self._onRemoved):
                self.CurrentListData._RemovedValue.remove(self._onRemoved)
            if self.CurrentListData._ChangedValue.has(self._onChanged):
                self.CurrentListData._ChangedValue.remove(self._onChanged)
            if self.CurrentListData._FullChanged.has(self._onFullChanged):
                self.CurrentListData._FullChanged.remove(self._onFullChanged)

        self.CurrentListData = ListsDataBase().get(list(ListsDataBase().data.keys())[self.CurrentList])

        if not self.CurrentListData._AddedValue.has(self._onAdded):
            self.CurrentListData._AddedValue.add(self._onAdded)
        if not self.CurrentListData._RemovedValue.has(self._onRemoved):
            self.CurrentListData._RemovedValue.add(self._onRemoved)
        if not self.CurrentListData._ChangedValue.has(self._onChanged):
            self.CurrentListData._ChangedValue.add(self._onChanged)
        if not self.CurrentListData._FullChanged.has(self._onFullChanged):
            self.CurrentListData._FullChanged.add(self._onFullChanged)

        self.refresh_list()

        self.listsFrame.createButton.config(state="normal")
        self.listsFrame.reverseButton.config(state="normal")
        self.listsFrame.sortButton.config(state="normal")

        self.valueEditor.canDetect = True

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.CurrentList = None
        self.CurrentListData = None
        self.CurrentValue = None

        self.listsFrame = ListsFrame(self, style="Card.TFrame", padding=10)
        self.valueEditor = ValueEditor(self, style="Card.TFrame", padding=10)

        self.close()

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x700")
        self.title("(Тест) Редагування списків")
        center_window(self)
        sv_ttk.use_dark_theme()

        self.listsEditor = ListsEditor(self)
        self.listsEditor.place(relwidth=1, relheight=1)

if __name__ == "__main__":
    root = App()
    root.mainloop()