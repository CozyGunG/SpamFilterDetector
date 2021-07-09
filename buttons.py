'''
Buttons used for the GUI Display

Author: Alex Kim
'''
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from threading import Thread
'''from PyQt5.QtWidgets import (
    QApplication,
    QLabel
)'''
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
        self.filename = filedialog.askopenfilename(initialdir="/Users/alexk/Compsci 361/Assignment3", title="Select A File",
                                                   filetypes=(("CSV files", "*.csv"), ("All Files", "*.*")))

    def process(self):
        train_set = pd.read_csv(self.filename)

        # Clean the dataset
        train_set['abstract'] = train_set['abstract'].str.replace('\W', ' ')  # Removes punctuation
        train_set['abstract'] = train_set['abstract'].str.lower()
        train_set['abstract'] = train_set['abstract'].str.split()

        # Set up dictionary
        dictionary = [word for abstract in train_set['abstract']
                                        for word in abstract]
        dictionary = list(set(dictionary))

        # Initialise word_counts to 0 for each unique word for each abstract
        word_count_per_abstract = {unique_word: [0] * len(train_set['abstract']) for unique_word in dictionary}

        # Fill in the word counts
        for index, abstract in enumerate(train_set['abstract']):
            for word in abstract:
                word_count_per_abstract[word][index] += 1

        # Get the total word count for each word
        total_word_count = {}
        for word in dictionary:
            total_word_count[word] = sum(word_count_per_abstract[word])

        # Create a dataframe of the word counts for each abstract
        df = {}
        for word in dictionary:
            df[word] = word_count_per_abstract[word]
        word_counts_df = pd.DataFrame(df)

        # Isolate abstract
        index = train_set.index
        A_index = index[train_set['class'] == "A"]
        A_abstract = word_counts_df.iloc[A_index]
        B_index = index[train_set['class'] == "B"]
        B_abstract = word_counts_df.iloc[B_index]
        E_index = index[train_set['class'] == "E"]
        E_abstract = word_counts_df.iloc[E_index]
        V_index = index[train_set['class'] == "V"]
        V_abstract = word_counts_df.iloc[V_index]

        # Number of Each Abstract
        n_A = len(A_abstract)
        n_B = len(B_abstract)
        n_E = len(E_abstract)
        n_V = len(V_abstract)

        # Calculate probabilities of each abstract
        p_A = n_A / len(train_set)
        p_B = n_B / len(train_set)
        p_E = n_E / len(train_set)
        p_V = n_V / len(train_set)



# Extend a class then override the methods of the child class
