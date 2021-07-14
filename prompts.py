import tkinter as tk
from tkinter import ttk
import globalVar

class OpenFileDisplay:
    def __init__(self):
        self.display = tk.Toplevel()
        self.init_display()
        self.format_display()

    def init_display(self):
        self.display.title("Alert")
        self.display.geometry('300x200')
        self.display.configure(background=globalVar.LIGHT_GREEN)

    def format_display(self):
        self.pb = ttk.Progressbar(self.display, orient='horizontal', mode='determinate', length=500)
        self.pb.pack(pady=10)

    def set_progressbar_value(self, value):
        self.pb['value'] = value