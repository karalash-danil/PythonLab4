import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog  # Import messagebox
from PIL import Image, ImageTk
import random

'''
    Варіант 6 - Автомобіль
'''


class Car:
    def __init__(self, m: str, b: str, s: float, y: int, color: str, body_type: str, engine_volume: float,
                 wheel_size: int):
        self.fuel = "Газ"
        self.model = m
        self.brand = b
        self.speed = s
        self.year = y
        self.color = color  # Новий атрибут
        self.body_type = body_type  # Новий атрибут
        self.engine_volume = engine_volume  # новий атрибут
        self.wheel_size = wheel_size  # новий атрибут


class ElectricCar(Car):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fuel = "Електроенергія"


class EntryWithLabel(ttk.Frame):
    def __init__(self, *args, text="", **kwargs):
        super().__init__(*args, **kwargs)
        self.label = ttk.Label(self, text=text)
        self.input = ttk.Entry(self)

        self.label.pack(side=tk.LEFT)
        self.input.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def get(self):
        return self.input.get()


class Gallery(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.images = ["images/1.png", "images/2.png", "images/3.png"]
        self.current_index = 0

        self.Title = ttk.Label(self, text="Вибрати зображення")
        self.Title.pack(padx=5, pady=5, fill=tk.X)

        self.image = ttk.Label(self)
        self.image.pack(padx=5, expand=True, fill=tk.X)

        self.downFrame = ttk.Frame(self)
        self.downFrame.pack(padx=5, fill=tk.X)

        self.labelImageIndex = ttk.Label(self.downFrame, text="0/0")
        self.prevImageButton = ttk.Button(self.downFrame, text="<- Назад", command=self.prev_image)
        self.nextImageButton = ttk.Button(self.downFrame, text="Вперед ->", command=self.next_image)

        self.prevImageButton.pack(fill=tk.X, side="left")
        self.labelImageIndex.pack(padx=5, fill=tk.X, expand=True, side="left")
        self.nextImageButton.pack(fill=tk.X, side="right")

        self.reload()

    def prev_image(self):
        self.current_index = max(self.current_index - 1, 0)
        self.reload()

    def next_image(self):
        self.current_index = min(self.current_index + 1, len(self.images) - 1)
        self.reload()

    def reload(self):
        self.labelImageIndex.config(text=f"{self.current_index + 1}/{len(self.images)}")
        try:
            self.ready_image = ImageTk.PhotoImage(Image.open(self.images[self.current_index]).resize((180, 120)))
            self.image.config(image=self.ready_image)
            self.image.image = self.ready_image
        except Exception as e:
            print(f"Error loading image: {e}")
            # Handle the error, e.g., display a placeholder image
            self.image.config(text="Image Not Found")


class PanelCreateObjectElectricCar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, relief=tk.RIDGE, borderwidth=5, width=200, height=300)
        self.Title = ttk.Label(self, text="Створення Об'єкта \"Електро Мобіль\"")
        self.Title.pack(padx=5, pady=5, fill=tk.X)

        self.model = EntryWithLabel(self, text="Модель: ")
        self.model.pack(padx=5, fill=tk.X)
        self.brand = EntryWithLabel(self, text="Бренд: ")
        self.brand.pack(padx=5, fill=tk.X)
        self.speed = EntryWithLabel(self, text="Швидкість: ")
        self.speed.pack(padx=5, fill=tk.X)
        self.year = EntryWithLabel(self, text="Рік: ")
        self.year.pack(padx=5, fill=tk.X)

        # Нові атрибути з використанням списків та кортежів
        self.colors_list = ["Червоний", "Синій", "Зелений", "Чорний", "Білий"]
        self.body_types_tuple = ("Седан", "Хетчбек", "Універсал", "Кросовер", "Мінівен")
        self.engine_volumes_list = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
        self.wheel_sizes_list = [15, 16, 17, 18, 19]

        self.color_var = tk.StringVar(value=self.colors_list[0])
        self.color_label = ttk.Label(self, text="Колір:")
        self.color_label.pack(padx=5, fill=tk.X)
        self.color_combobox = ttk.Combobox(self, textvariable=self.color_var, values=self.colors_list)
        self.color_combobox.pack(padx=5, fill=tk.X)

        self.body_type_var = tk.StringVar(value=self.body_types_tuple[0])
        self.body_type_label = ttk.Label(self, text="Тип кузова:")
        self.body_type_label.pack(padx=5, fill=tk.X)
        self.body_type_combobox = ttk.Combobox(self, textvariable=self.body_type_var, values=self.body_types_tuple,
                                               state="readonly")  # Кортеж, readonly
        self.body_type_combobox.pack(padx=5, fill=tk.X)

        self.engine_volume_var = tk.StringVar(value=self.engine_volumes_list[0])
        self.engine_volume_label = ttk.Label(self, text="Об'єм двигуна:")
        self.engine_volume_label.pack(padx=5, fill=tk.X)
        self.engine_volume_combobox = ttk.Combobox(self, textvariable=self.engine_volume_var,
                                                   values=self.engine_volumes_list)
        self.engine_volume_combobox.pack(padx=5, fill=tk.X)

        self.wheel_size_var = tk.StringVar(value=self.wheel_sizes_list[0])
        self.wheel_size_label = ttk.Label(self, text="Розмір колес:")
        self.wheel_size_label.pack(padx=5, fill=tk.X)
        self.wheel_size_combobox = ttk.Combobox(self, textvariable=self.wheel_size_var, values=self.wheel_sizes_list)
        self.wheel_size_combobox.pack(padx=5, fill=tk.X)

        # Кнопки для операцій зі списками
        self.list_operations_frame = ttk.Frame(self)
        self.list_operations_frame.pack(padx=5, fill=tk.X)

        self.add_color_button = ttk.Button(self.list_operations_frame, text="Додати колір", command=self.add_color)
        self.add_color_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.edit_color_button = ttk.Button(self.list_operations_frame, text="Редагувати колір",
                                            command=self.edit_color)
        self.edit_color_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.sort_color_button = ttk.Button(self.list_operations_frame, text="Сортувати кольори",
                                            command=self.sort_colors)
        self.sort_color_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.delete_color_button = ttk.Button(self.list_operations_frame, text="Видалити колір",
                                              command=self.delete_color)
        self.delete_color_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.check_color_list_button = ttk.Button(self.list_operations_frame, text="Перевірити список кольорів",
                                                  command=self.check_color_list)
        self.check_color_list_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.reverse_color_list_button = ttk.Button(self.list_operations_frame, text="Змінити порядок кольорів",
                                                    command=self.reverse_color_list)
        self.reverse_color_list_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.check_color_list_size_button = ttk.Button(self.list_operations_frame,
                                                       text="Перевірити розмір списку кольорів",
                                                       command=self.check_color_list_size)
        self.check_color_list_size_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.gallery = Gallery(self)
        self.gallery.pack(padx=5, fill=tk.X)

        self.createButton = ttk.Button(self, text="+ Створити", command=self.create_car_object)
        self.createButton.pack(padx=5, pady=5, fill=tk.X)

    def create_car_object(self):
        try:
            color = self.color_var.get()
            body_type = self.body_type_var.get()
            engine_volume = float(self.engine_volume_var.get())
            wheel_size = int(self.wheel_size_var.get())
            car = ElectricCar(self.model.get(), self.brand.get(), float(self.speed.get()), int(self.year.get()), color,
                              body_type, engine_volume, wheel_size)
            self.parent.objectsList.add_object(car, self.gallery.images[self.gallery.current_index])
        except ValueError:
            messagebox.showerror("Помилка",
                                 "Будь ласка, введіть коректні числові значення для швидкості, року, об'єму двигуна та розміру колес.")

    # Функції для операцій зі списком кольорів
    def add_color(self):
        new_color = tk.simpledialog.askstring("Додати колір", "Введіть новий колір:")
        if new_color:
            self.colors_list.append(new_color)
            self.color_combobox.config(values=self.colors_list)
            self.color_var.set(new_color)  # set the Combobox to the new color
            messagebox.showinfo("Успіх", f"Колір '{new_color}' додано до списку.")

    def edit_color(self):
        old_color = self.color_var.get()
        new_color = tk.simpledialog.askstring("Редагувати колір", f"Введіть новий колір для '{old_color}':")
        if new_color:
            try:
                index = self.colors_list.index(old_color)
                self.colors_list[index] = new_color
                self.color_combobox.config(values=self.colors_list)
                self.color_var.set(new_color)  # update the Combobox
                messagebox.showinfo("Успіх", f"Колір '{old_color}' змінено на '{new_color}'.")
            except ValueError:
                messagebox.showerror("Помилка", f"Колір '{old_color}' не знайдено у списку.")

    def sort_colors(self):
        self.colors_list.sort()
        self.color_combobox.config(values=self.colors_list)
        messagebox.showinfo("Успіх", "Список кольорів відсортовано.")

    def delete_color(self):
        color_to_delete = self.color_var.get()
        try:
            self.colors_list.remove(color_to_delete)
            self.color_combobox.config(values=self.colors_list)
            if self.colors_list:
                self.color_var.set(self.colors_list[0])  # update combobox
            else:
                self.color_var.set("")
            messagebox.showinfo("Успіх", f"Колір '{color_to_delete}' видалено зі списку.")
        except ValueError:
            messagebox.showerror("Помилка", f"Колір '{color_to_delete}' не знайдено у списку.")

    def check_color_list(self):
        if self.colors_list:
            messagebox.showinfo("Список не порожній", "Список кольорів не порожній.")
        else:
            messagebox.showinfo("Список порожній", "Список кольорів порожній.")

    def reverse_color_list(self):
        self.colors_list.reverse()
        self.color_combobox.config(values=self.colors_list)
        messagebox.showinfo("Успіх", "Список кольорів змінено на зворотній.")

    def check_color_list_size(self):
        limit = tk.simpledialog.askinteger("Перевірити розмір списку", "Введіть лімітний розмір:")
        if limit is not None:
            if len(self.colors_list) <= limit:
                messagebox.showinfo("Розмір списку в межах ліміту",
                                    f"Розмір списку кольорів ({len(self.colors_list)}) не перевищує ліміт ({limit}).")
            else:
                messagebox.showinfo("Розмір списку перевищує ліміт",
                                    f"Розмір списку кольорів ({len(self.colors_list)}) перевищує ліміт ({limit}).")


class CardCarObject(ttk.Frame):
    def __init__(self, parent, obj, image):
        super().__init__(parent, width=400, height=100, relief=tk.RIDGE, borderwidth=5)
        self.obj = obj
        self.label = ttk.Label(self, justify="left",
                               text=f"Тип палива: {obj.fuel}\nМодель: {obj.model}\nБренд: {obj.brand}\nШвидкість: {obj.speed}\nРік: {obj.year}\n"
                                    f"Колір: {obj.color}\nТип кузова: {obj.body_type}\nОб'єм двигуна: {obj.engine_volume}\nРозмір колес: {obj.wheel_size}")
        self.label.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        try:
            self.ready_image = ImageTk.PhotoImage(Image.open(image).resize((130, 90)))
            self.image = ttk.Label(self, image=self.ready_image)
            self.image.pack(padx=5, expand=True, fill=tk.X)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.image = ttk.Label(self, text="Image Not Found")
            self.image.pack(padx=5, expand=True, fill=tk.X)

        self.deleteButton = ttk.Button(self, text="- Видалити", command=lambda: self.destroy_object(parent))
        self.deleteButton.pack(padx=5, pady=5, fill=tk.X)

    def destroy_object(self, parent):
        parent.remove_object(self)  # Call the remove_object method of ObjectsList
        self.destroy()  # Destroy the widget


class ObjectsList(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", width=50, command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: self.scrollable_frame.config(width=e.width))
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="center")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.objects = []

    def add_object(self, obj, image):
        card = CardCarObject(self, obj, image)
        self.objects.append(card)  # Store the card, not just the object
        card.pack(pady=5, fill=tk.X)

    def remove_object(self, card_to_remove):
        for card in self.objects:
            if card == card_to_remove:
                self.objects.remove(card)
                break


'''    Main Window    '''


class CarApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")  # Збільшено висоту вікна
        self.title("Створення Об'єкта Електро Мобіль")
        self.eval('tk::PlaceWindow . center')

        self.panelCreateObjectElectricCar = PanelCreateObjectElectricCar(self)
        self.panelCreateObjectElectricCar.pack(padx=5, pady=5, side=tk.LEFT)

        self.objectsList = ObjectsList(self)
        self.objectsList.pack(padx=5, pady=5, side=tk.RIGHT, fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = CarApp()
    root.mainloop()
