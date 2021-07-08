'''
Buttons used for the GUI Display

Author: Alex Kim
'''
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import globalVar

class OpenFileBtn(tk.Button):
    def __init__(self):
        super().__init__(text='Open File', width=18, bg=globalVar.WHITE, command=lambda: self.onclick())
        self.filename = "/"

    def onclick(self):
        self.openFile()
        if self.filename != "/":
            self.process()
            self.filename = "/"

    def openFile(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                                   filetypes=(("CSV files", "*.csv"), ("All Files", "*.*")))

    def process(self):
        train_set = pd.read_csv(self.filename)
        print(train_set)

        # Clean the dataset
        train_set['abstract'] = train_set['abstract'].str.replace('\W', ' ')  # Removes punctuation
        train_set['abstract'] = train_set['abstract'].str.lower()
        train_set['abstract'] = train_set['abstract'].str.split()

        # Set up dictionary
        dict = [word for abstract in train_set['abstract']
                        for word in abstract]
        dict = list(set(dict))

        word_count_per_abstract = {unique_word: [0] * len(train_set['abstract']) for unique_word in dict}




# Extend a class then override the methods of the child class