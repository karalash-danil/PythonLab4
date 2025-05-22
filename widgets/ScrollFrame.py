import tkinter as tk
from tkinter import ttk

class ScrollFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)  # create a frame (self)
        self.parent = parent

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(side="left", expand=True, fill="both") # place canvas on self

        self.viewport = tk.Frame(self.canvas, pady=5, padx=5)  # place a frame on the canvas, this frame will hold the child widgets

        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)  # place a scrollbar on self
        self.vsb.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.vsb.set)  # attach scrollbar action to scroll of canvas

        self.canvas_window = self.canvas.create_window((0, 0), window=self.viewport, anchor="nw")

        self.viewport.bind("<Configure>", self.onFrameConfigure)  # bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)  # bind an event whenever the size of the canvas frame changes.

        self.viewport.bind('<Enter>', self.onEnter)  # bind wheel events when the cursor enters the control
        self.viewport.bind('<Leave>', self.onLeave)  # unbind wheel events when the cursorl leaves the control

        self.onFrameConfigure(None)  # perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))  # whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window,
                               width=canvas_width)  # whenever the size of the canvas changes alter the window region respectively.

    def onMouseWheel(self, event):  # cross platform scroll wheel event
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


    def onEnter(self, event):  # bind wheel events when the cursor enters the control
        self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    def onLeave(self, event):  # unbind wheel events when the cursorl leaves the control
        self.canvas.unbind_all("<MouseWheel>")