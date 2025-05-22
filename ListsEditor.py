import tkinter as tk
from os import unlink
from tkinter import ttk, Widget
from tkinter import messagebox
from xml.etree.ElementPath import prepare_self

import sv_ttk

from Utils import *

from widgets.ScrollFrame import ScrollFrame
from widgets.EntryWithLabel import EntryWithLabel
from widgets.Gallery import Gallery


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
        self.comboBoxLists.pack(padx=5, pady=5, fill="x")

        self.listValues = tk.Listbox(self)
        self.listValues.pack(padx=5, pady=5, fill="x")

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
                #else:
                #    self.listValues.select_set(self._nametowidget(self.winfo_parent()).CurrentValue)

        self.listValues.bind("<<ListboxSelect>>", callback1)
        self.lists_textvariable.trace_add("write", callback)


class ListsEditor(ttk.Frame):
    def create(self):
        print("F")
        try:
            self.listsFrame.canDetect = False
            self.listsFrame.listValues.insert("end", "Нове значення")
            self.listsFrame.listValues.select_set(self.listsFrame.listValues.size() - 1)

            ListsDataBase().get(list(ListsDataBase().data.keys())[self.CurrentList]).values.append("Нове значення")

            self.listsFrame.canDetect = True

            self.open(self.listsFrame.listValues.size() - 1)

            print("H")
        except Exception as e:
            print(e)


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

            self.listsFrame.listValues.delete(self.CurrentValue)
            self.listsFrame.listValues.insert(self.CurrentValue, self.valueEditor.inputTextvariable.get())
            self.listsFrame.listValues.select_set(self.CurrentValue)

            ListsDataBase().get(list(ListsDataBase().data.keys())[self.CurrentList]).values[self.CurrentValue] = self.valueEditor.inputTextvariable.get()

            self.listsFrame.canDetect = True

    def open(self, index):
        self.close()

        self.load(index)

        self.listsFrame.pack_forget()
        self.valueEditor.pack(anchor="w", expand=True, padx=5, pady=5, side="right")
        self.listsFrame.pack(anchor="e", expand=True, padx=5, pady=5, side="left")

    def close(self):
        self.unload()

        self.valueEditor.pack_forget()
        self.listsFrame.pack_forget()
        self.listsFrame.pack(expand=True, padx=5, pady=5, side="left")

    def delete(self):
        temp = self.CurrentValue
        self.close()

        self.listsFrame.listValues.delete(temp)
        ListsDataBase().get(list(ListsDataBase().data.keys())[self.CurrentList]).values.pop(temp)

    def refresh_list(self):
        self.listsFrame.canDetect = False

        self.listsFrame.listValues.delete(0, "end")
        for i in ListsDataBase().get(list(ListsDataBase().data.keys())[self.CurrentList]).values:
            self.listsFrame.listValues.insert(tk.END, i)
            if self.CurrentValue is not None:
                if i == self.valueEditor.inputTextvariable.get():
                    index = ListsDataBase().get(list(ListsDataBase().data.keys())[self.CurrentList]).values.index(
                        self.valueEditor.inputTextvariable.get())
                    self.listsFrame.listValues.select_set(index)
                    self.CurrentValue = index

        self.listsFrame.canDetect = True

    def sort(self):
        self.listsFrame.canDetect = False

        ListsDataBase().get(list(ListsDataBase().data.keys())[self.CurrentList]).values.sort()

        self.refresh_list()

        self.listsFrame.canDetect = True

    def reverse(self):
        self.listsFrame.canDetect = False

        ListsDataBase().get(list(ListsDataBase().data.keys())[self.CurrentList]).values.reverse()

        self.refresh_list()

        self.listsFrame.canDetect = True

    def select_list(self, index):
        self.close()

        self.valueEditor.canDetect = False

        self.CurrentList = index

        self.listsFrame.listValues.delete(0, "end")
        for i in ListsDataBase().get(list(ListsDataBase().data.keys())[index]).values:
            self.listsFrame.listValues.insert(tk.END, i)

        self.listsFrame.createButton.config(state="normal")
        self.listsFrame.reverseButton.config(state="normal")
        self.listsFrame.sortButton.config(state="normal")

        self.valueEditor.canDetect = True

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.CurrentList = None
        self.CurrentValue = None

        self.listsFrame = ListsFrame(self, style="Card.TFrame", padding=10)
        self.valueEditor = ValueEditor(self, style="Card.TFrame", padding=10)

        self.close()



#----------------------------

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
        #self.eval('tk::PlaceWindow . center')
        center_window(self)
        sv_ttk.use_dark_theme()

        self.listsEditor = ListsEditor(self)
        self.listsEditor.place(relwidth=1, relheight=1)

if __name__ == "__main__":
    root = App()
    root.mainloop()