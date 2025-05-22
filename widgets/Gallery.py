import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

class Gallery(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, style="TLabelframe")
        self.images = ["images/1.png","images/2.png","images/3.png"]
        self.current_index = 0

        self.textvariable = tk.StringVar()

        self.Title = tk.Label(self, text="Вибрати зображення")
        self.Title.pack(padx=5, pady=5, fill=tk.X)

        self.image = tk.Label(self)
        self.image.pack(padx=5, expand=True, fill=tk.X)

        self.downFrame = ttk.Frame(self)
        self.downFrame.pack(padx=5, pady=5, fill=tk.X)

        self.labelImageIndex = ttk.Label(self.downFrame, anchor="center", text="0/0")
        self.prevImageButton = ttk.Button(self.downFrame, text="", command=self.prev_image)
        self.nextImageButton = ttk.Button(self.downFrame, text="", command=self.next_image)

        self.prevImageButton.pack(fill="both", padx=5, pady=5, side="left")
        self.labelImageIndex.pack(padx=5, pady=5, fill="both", expand=True, side="left")
        self.nextImageButton.pack(fill="both", padx=5, pady=5, side="right")

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

        self.textvariable.set(self.current_index)