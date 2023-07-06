'''Tkinter utilities

This module contains a collection of Tkinter utilities, including:
    - CreateToolTip: Creates a tooltip for a given widget
'''

import tkinter as tk

class CreateToolTip(object):
    """Create a tooltip for a given widget"""
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                    background="#ffffff", relief='solid', borderwidth=1,
                    wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

def redimensionar_filas_columnas(frame):
    """ Redimensiona las filas y columnas de un frame """
    col_count, row_count = frame.grid_size()

    for col in range(col_count):
        frame.grid_columnconfigure(col, minsize=20)

    for row in range(row_count):
        frame.grid_rowconfigure(row, minsize=40)

def centrar_ventana(ventana):
    """ Centra una ventana en la pantalla """
    ventana.update_idletasks()
    w = ventana.winfo_screenwidth()
    h = ventana.winfo_screenheight()
    size = tuple(int(_) for _ in ventana.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    ventana.geometry("%dx%d+%d+%d" % (size + (x, y)))