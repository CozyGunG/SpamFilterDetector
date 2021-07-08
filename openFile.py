'''
Open a File

Author: Alex Kim
'''
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import globalVar

class OpenFileBtn(tk.Button):

    def __init__(self):
        super().__init__(text='Open File', width=18, bg=globalVar.WHITE, command=lambda: self.openFile())

    def openFile(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                                   filetypes=(("CSV files", "*.csv"), ("All Files", "*.*")))
        self.readFile()

