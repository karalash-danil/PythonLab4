import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from PIL import Image, ImageTk

import sv_ttk

#------------------------

from Utils import *

from widgets.ComboBoxWithLabel import ComboBoxWithLabel
from widgets.ScrollFrame import ScrollFrame
from widgets.EntryWithLabel import EntryWithLabel
from widgets.SpinboxWithLabel import SpinboxWithLabel
from widgets.Gallery import Gallery

from ListsEditor import ListsEditor

'''
    Варіант 6 - Автомобіль
'''

class ObjectEditor(ttk.Frame):
    def show_editor(self):
        self.Editor.pack(padx=5, pady=5, fill="x")
    def hide_editor(self):
        self.Editor.pack_forget()

    def show_creator(self):
        self.Creator.pack(padx=5, pady=5, fill="x")
    def hide_creator(self):
        self.Creator.pack_forget()

    def create_object(self):
        obj = ObjectsDataBase().create()
        card = self.parent.objectsList.add_object(obj)
        self.open_object(obj,card)

    def close_object(self):
        if self.CurrentObject != None:
            self.save_data()
        self.CurrentObject = None

        if self.CurrentCard != None:
            self.CurrentCard.config(style="TButton")
        self.CurrentCard = None

        self.hide_editor()
        self.show_creator()

    def open_object(self, obj, card):
        self.close_object()

        self.CurrentObject = obj
        self.hide_creator()
        self.show_editor()

        self.CurrentCard = card
        try:
            self.CurrentCard.config(style="Accent.TButton")
        except Exception:
            pass

        self.load_data()

    def clear_data(self):
        self.detect_changes = False
        self.model.textvariable.set("")
        self.brand.textvariable.set("")
        self.speed.textvariable.set("0")

        self.price.textvariable.set("0")

        self.year.textvariable.set("0")
        self.month.textvariable.set("")

        self.fuelType.textvariable.set("")
        self.color.textvariable.set("")
        self.gallery.current_index = 0
        self.gallery.reload()
        self.detect_changes = True

    def load_data(self):
        self.detect_changes = False
        self.model.textvariable.set(self.CurrentObject.model)
        self.brand.textvariable.set(self.CurrentObject.brand)
        self.speed.textvariable.set(self.CurrentObject.speed)
        self.seats.textvariable.set(self.CurrentObject.seats)

        self.price.textvariable.set(self.CurrentObject.price)

        self.year.textvariable.set(self.CurrentObject.year)
        self.month.textvariable.set(self.CurrentObject.month)

        self.fuelType.textvariable.set(self.CurrentObject.fuelType)
        self.color.textvariable.set(self.CurrentObject.color)
        self.gallery.current_index = int(self.CurrentObject.imageId)
        self.gallery.reload()
        self.detect_changes = True

    def save_data(self):
        self.CurrentObject.model = self.model.get()
        self.CurrentObject.brand = self.brand.get()
        self.CurrentObject.speed = self.speed.get()
        self.CurrentObject.seats = self.seats.get()

        self.CurrentObject.price = self.price.get()

        self.CurrentObject.year = self.year.get()
        self.CurrentObject.month = self.month.get()

        self.CurrentObject.fuelType = self.fuelType.get()
        self.CurrentObject.color = self.color.get()
        self.CurrentObject.imageId = self.gallery.current_index

        self.CurrentCard.update()

    def delete_object(self):
        answer = tk.messagebox.askokcancel("Попередження", "Ви точно хочете видалити об`экт?")

        if answer:
            ObjectsDataBase().delete(self.CurrentObject.id)
            self.CurrentCard.destroy()
            self.CurrentObject = None
            self.CurrentCard = None

            self.close_object()

    def __init__(self, parent):
        super().__init__(parent, width=200, height=300, padding=15, style="Card.TFrame")
        self.CurrentCard = None
        self.CurrentObject = None
        self.detect_changes = False
        self.parent = parent
        self.Title = ttk.Label(self, text="Автомобіль", anchor="center", font=("Segoe UI", 11))
        self.Title.pack(padx=5, pady=5, fill="x")

        #-----------------------------

        self.Creator = ttk.Frame(self)
        self.Editor = ttk.Frame(self)

        #- Creator --------------------

        self.createButton = ttk.Button(self.Creator, text=" Створити", style="Accent.TButton", command=self.create_object)
        self.createButton.pack(padx=5, pady=5, fill="x")

        #- Editor ---------------------

        self.model = EntryWithLabel(self.Editor,text="Модель: ")
        self.model.pack(pady=5, fill="x")
        self.brand = ComboBoxWithLabel(self.Editor, "brand")
        self.brand.pack(pady=5, fill="x")
        self.speed = SpinboxWithLabel(self.Editor, text="Швидкість: ", from_= 0, to=999)
        self.speed.pack(pady=5, fill="x")
        self.seats = SpinboxWithLabel(self.Editor, text="Місць: ", from_=0, to=999)
        self.seats.pack(pady=5, fill="x")

        self.price = SpinboxWithLabel(self.Editor, text="Ціна(грн.): ", from_=0, to=999999)
        self.price.pack(pady=5, fill="x")

        ttk.Separator(self.Editor).pack(padx=5, pady=5, fill="x")

        self.year = SpinboxWithLabel(self.Editor, text="Рік: ", from_= 1900, to=3000)
        self.year.pack(pady=5, fill="x")
        self.month = ComboBoxWithLabel(self.Editor, "month")
        self.month.pack(pady=5, fill="x")

        ttk.Separator(self.Editor).pack(padx=5, pady=5, fill="x")

        self.fuelType = ComboBoxWithLabel(self.Editor, "fuelType")
        self.fuelType.pack(pady=5, fill="x")

        self.color = ComboBoxWithLabel(self.Editor, "color")
        self.color.pack(pady=5, fill="x")

        self.gallery = Gallery(self.Editor)
        self.gallery.pack(padx=5, pady=10, fill="x")

        self.bottomPanel = ttk.Frame(self.Editor, padding=5)
        self.bottomPanel.pack(fill="x")

        self.closeButton = ttk.Button(self.bottomPanel, text=" Закрити", style="Accent.TButton", command=self.close_object)
        self.closeButton.pack(side="right", padx=5, fill="x", expand=True)

        self.deleteButton = ttk.Button(self.bottomPanel, text=" Видалити", command=self.delete_object)
        self.deleteButton.pack(side="left", padx=5, fill="x", expand=True)

        #-------------------

        self.show_creator()

        def changed(a,b,c):
            print(a,b,c)
            if self.detect_changes:
                self.save_data()

        self.model.textvariable.trace_add("write", changed)
        self.brand.textvariable.trace_add("write", changed)
        self.speed.textvariable.trace_add("write", changed)
        self.seats.textvariable.trace_add("write", changed)

        self.price.textvariable.trace_add("write", changed)

        self.year.textvariable.trace_add("write", changed)
        self.month.textvariable.trace_add("write", changed)

        self.fuelType.textvariable.trace_add("write", changed)

        self.color.textvariable.trace_add("write", changed)

        self.gallery.textvariable.trace_add("write", changed)

class ObjectCard(ttk.Button):
    def update(self):
        super().update()
        self.configure(text=f"ID: {self.obj.id}"
                            f"\n{self.obj.brand} {self.obj.model}"
                            f"\nТип палива: {self.obj.fuelType}"
                            f"\nШвидкість: {self.obj.speed}"
                            f"\nМісць: {self.obj.seats}"
                            f"\n"
                            f"\nЦіна(грн.): {self.obj.price}"
                            f"\n"
                            f"\nДата: {self.obj.year} | {self.obj.month}"
                            f"\nКолір: {self.obj.color}"
                            f"")

        try:
            self.images = ["images/1.png", "images/2.png", "images/3.png"]

            self.ready_image = ImageTk.PhotoImage(Image.open(self.images[self.obj.imageId]).resize((120, 80)))
            self.config(image=self.ready_image)
            self.image = self.ready_image
        except Exception:
            pass

    def __init__(self,parent, obj, editor):
        super().__init__(parent, compound="left")
        self.obj = obj
        self.editor = editor

        def pressed():
            editor.open_object(obj, self)
        self.configure(command=pressed)

        self.update()

class ObjectsList(ScrollFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.objects = []

        for i in ObjectsDataBase().data:
            self.add_object(i)

    def add_object(self, obj):
        card = ObjectCard(self.viewport, obj, self.parent.objectEditor)
        card.pack(padx=5, pady=5, fill="x")
        return card

'''     Main Window     '''

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

class CarsFrame(ttk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.objectEditor=ObjectEditor(self)
        self.objectEditor.pack(padx=15, pady=15, side="left")

        self.objectsList=ObjectsList(self)
        self.objectsList.pack(padx=5, pady=5, side="right", fill="both", expand=True)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x900")
        self.title("База данных автомобілей")
        center_window(self)
        sv_ttk.use_dark_theme()

        #-----------------------------

        self.mainFrame = ttk.Frame(self)
        self.noteBook = ttk.Notebook(self.mainFrame)

        self.mainFrame.pack(fill="both", expand=True)
        self.noteBook.pack(fill="both", expand=True)

        #-----------------------------

        self.carsFrame = CarsFrame(self.mainFrame)
        self.listsEditor = ListsEditor(self.mainFrame)

        #-----------------------------

        self.noteBook.add(self.carsFrame, text="Автомобілі")
        self.noteBook.add(self.listsEditor, text="Редагування Списків")

if __name__ == "__main__":
    root = App()
    root.mainloop()