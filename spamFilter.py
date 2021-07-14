'''
Spam Filtering using Bayesian Algorithms
Author: Alex Kim
'''
import tkinter as tk
from tkinter import ttk
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
        tk.Label(self.display, text='Spam Filter Detector', fg=globalVar.BLACK, bg=globalVar.LIGHT_GREEN,
                 font=globalVar.TITLE_FONT, pady=5) \
            .pack()

        tk.Label(self.display, text='Enter Text Here to Analyze:', fg=globalVar.BLACK, bg=globalVar.LIGHT_GREEN,
                 font=globalVar.HEADER_FONT, anchor='w') \
            .pack(fill='both', padx=40)

        text_box = tk.Text(self.display, height=10, width=60, font=globalVar.INPUT_FONT)
        text_box.pack()

        button_frame = tk.Frame(self.display, bg=globalVar.LIGHT_GREEN)
        button_frame.pack(pady=10)

        pb = ttk.Progressbar(self.display, orient='horizontal', mode='determinate', length=500)

        lb = tk.Label(self.display, width=60, bg=globalVar.LIGHT_GREEN)

        open_file_btn = functions.OpenFile(pb, lb)
        tk.Button(button_frame, text='Open File', width=20, bg=globalVar.WHITE, command=lambda: open_file_btn.onclick()) \
            .grid(row=0, column=0, padx=10)

        analyze_btn = functions.SpamFilter(open_file_btn, text_box)
        tk.Button(button_frame, text='Analyze', width=20, bg=globalVar.WHITE, command=lambda: analyze_btn.onclick()) \
            .grid(row=0, column=1, padx=10)



if __name__ == '__main__':
    MainMenu()