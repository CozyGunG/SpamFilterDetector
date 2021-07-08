'''
Buttons used for the GUI Display

Author: Alex Kim
'''
import tkinter as tk
from tkinter import filedialog
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import pandas as pd
import globalVar

ps = PorterStemmer()


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

        # Clean the dataset
        train_set['abstract'] = train_set['abstract'].str.replace('\W', ' ')  # Removes punctuation
        split_abstracts = [word_tokenize(abstract) for abstract in train_set['abstract']]

        # Set up dictionary
        dictionary = [ps.stem(word) for abstract in split_abstracts
                                        for word in abstract]
        dictionary = list(set(dictionary))
        print(dictionary)

        # Initialise word_counts to 0 for each unique word for each abstract
        word_count_per_abstract = {unique_word: [0] * len(train_set['abstract']) for unique_word in dictionary}

        # Fill in the word counts
        for index, abstract in enumerate(split_abstracts):
            for word in abstract:
                word = ps.stem(word)
                word_count_per_abstract[word][index] += 1

        # Get the total word count for each word
        total_word_count = {}
        for word in dictionary:
            total_word_count[word] = sum(word_count_per_abstract[word])

# Extend a class then override the methods of the child class
