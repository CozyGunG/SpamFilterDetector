'''
Spam Filtering using Bayesian Algorithms
Author: Alex Kim
'''
import tkinter as tk
import globalVar
import functions
import numpy as np

class MainMenu:
    def __init__(self):
        self.display = tk.Tk()
        self.init_display()
        self.format_display()
        self.display.mainloop()

    def init_display(self):
        self.display.title("Spam Filter Detector")
        self.display.geometry('800x600')
        self.display.configure(background=globalVar.LIGHT_GREEN)

    def swap_display(self, new_display):
        self.display.destroy()
        new_display()

    def format_display(self):
        btn1 = tk.Button(self.display, text='Open File', width=18, bg=globalVar.WHITE,
                         command=lambda: functions.OpenFile())
        btn1.grid(row=1, column=0, sticky=tk.NSEW)
        # tk.Button(self.display, text='Open File', width=18, command=lambda: self.swap_display(openFile.OpenFileBtn)) \
        #     .grid(row=1, column=0, sticky=tk.NSEW)

if __name__ == '__main__':
    MainMenu()