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
        csv_file = functions.OpenFile()
        tk.Button(self.display, text='Open File', width=18, bg=globalVar.WHITE, command=lambda: csv_file.onclick()) \
            .grid(row=1, column=0, sticky=tk.NSEW)

        text_box = tk.Text(self.display, height=5, width=20)
        text_box.grid(row=3, column=0, sticky=tk.NSEW)

        input = functions.SpamFilter(csv_file, text_box)
        tk.Button(self.display, text='Analyze', width=18, bg=globalVar.WHITE, command=lambda: input.onclick()) \
            .grid(row=2, column=0, sticky=tk.NSEW)
        # tk.Button(self.display, text='Open File', width=18, command=lambda: self.swap_display(openFile.OpenFileBtn)) \
        #     .grid(row=1, column=0, sticky=tk.NSEW)

    '''Add Listeners for text_box in SpamFilter so you can grab the value in text_box in SpamFilter class instance'''

if __name__ == '__main__':
    MainMenu()