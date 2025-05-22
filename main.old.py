import tkinter as ttk
from PIL import Image, ImageTk

'''
    Варіант 6 - Автомобіль
'''

class Car:
    def __init__(self, m: str, b: str, s: float, y: int):
        self.fuel = "Газ"

        self.model = m
        self.brand = b
        self.speed = s
        self.year = y

class ElectricCar(Car):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fuel = "Електроенергія"

class EntryWithLabel(ttk.Frame):
    def __init__(self, *args,text="",**kwargs):
        super().__init__(*args,**kwargs)
        self.label = ttk.Label(self, text=text)
        self.input = ttk.Entry(self)

        self.label.pack(side=ttk.LEFT)
        self.input.pack(side=ttk.RIGHT,fill=ttk.BOTH,expand=True)

    def get(self):
        return self.input.get()

class Gallery(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.images = ["images/1.png","images/2.png","images/3.png"]
        self.current_index = 0

        self.Title = ttk.Label(self, text="Вибрати зображення")
        self.Title.pack(padx=5, pady=5, fill=ttk.X)

        self.image = ttk.Label(self)
        self.image.pack(padx=5, expand=True, fill=ttk.X)

        self.downFrame = ttk.Frame(self)
        self.downFrame.pack(padx=5, fill=ttk.X)

        self.labelImageIndex = ttk.Label(self.downFrame, text="0/0")
        self.prevImageButton = ttk.Button(self.downFrame,text="<- Назад", command=self.prev_image)
        self.nextImageButton = ttk.Button(self.downFrame,text="Вперед ->", command=self.next_image)

        self.prevImageButton.pack(fill=ttk.X, side="left")
        self.labelImageIndex.pack(padx=5, fill=ttk.X, expand=True, side="left")
        self.nextImageButton.pack(fill=ttk.X, side="right")

        self.reload()

    def prev_image(self):
        self.current_index = max(self.current_index-1,0)
        self.reload()
    def next_image(self):
        self.current_index = min(self.current_index+1,len(self.images)-1)
        self.reload()

    def reload(self):
        self.labelImageIndex.config(text=f"{self.current_index+1}/{len(self.images)}")

        self.ready_image = ImageTk.PhotoImage(Image.open(self.images[self.current_index]).resize((180,120)))
        self.image.config(image=self.ready_image)
        self.image.image = self.ready_image

class PanelCreateObjectElectricCar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, relief=ttk.RIDGE, borderwidth = 5, width=200, height=300)
        self.Title = ttk.Label(self, text="Створення Об`єкта \"Електро Машина\"")
        self.Title.pack(padx=5, pady=5, fill=ttk.X)

        self.model = EntryWithLabel(self,text="Модель: ")
        self.model.pack(padx=5, fill=ttk.X)
        self.brand = EntryWithLabel(self, text="Бренд: ")
        self.brand.pack(padx=5, fill=ttk.X)
        self.speed = EntryWithLabel(self, text="Швидкість: ")
        self.speed.pack(padx=5, fill=ttk.X)
        self.year = EntryWithLabel(self, text="Рік: ")
        self.year.pack(padx=5, fill=ttk.X)

        self.gallery = Gallery(self)
        self.gallery.pack(padx=5, fill=ttk.X)

        self.createButton = ttk.Button(self, text="+ Створити", command=lambda: parent.objectsList.add_object(ElectricCar(self.model.get(),self.brand.get(),self.speed.get(),self.year.get()),self.gallery.images[self.gallery.current_index]))
        self.createButton.pack(padx=5,pady=5,fill=ttk.X)

class CardCarObject(ttk.Frame):
    def __init__(self,parent, obj, image):
        super().__init__(parent, width=400, height=100, relief=ttk.RIDGE, borderwidth = 5)
        self.label = ttk.Label(self,justify="left",text=f"Тип палива: {obj.fuel}\nМодель: {obj.model}\nБренд: {obj.brand}\nШвидкість: {obj.speed}\nРік: {obj.year}")
        self.label.pack(padx=5, pady=5, fill=ttk.BOTH, expand=True)

        self.ready_image = ImageTk.PhotoImage(Image.open(image).resize((130, 90)))
        self.image = ttk.Label(self, image=self.ready_image)
        self.image.pack(padx=5, expand=True, fill=ttk.X)

        self.deleteButton = ttk.Button(self, text="- Видалити", command=lambda: self.destroy())
        self.deleteButton.pack(padx=5, pady=5, fill=ttk.X)

class ObjectsList(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        canvas = ttk.Canvas(self)
        scrollbar = ttk.Scrollbar(self,orient="vertical",width=50,command=canvas.yview)
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

    def add_object(self, obj:ElectricCar, image):
        card = CardCarObject(self.scrollable_frame,obj, image)
        card.pack(pady=5,fill=ttk.X)

'''     Main Window     '''
class CarApp(ttk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500")
        self.title("Creating Object ElectricCar")
        self.eval('tk::PlaceWindow . center')

        self.panelCreateObjectElectricCar=PanelCreateObjectElectricCar(self)
        self.panelCreateObjectElectricCar.pack(padx=5, pady=5, side=ttk.LEFT)

        self.objectsList=ObjectsList(self)
        self.objectsList.pack(padx=5, pady=5, side=ttk.RIGHT, fill=ttk.BOTH, expand=True)

if __name__ == "__main__":
    root = CarApp()
    root.mainloop()