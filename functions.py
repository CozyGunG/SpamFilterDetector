'''
Functions used in the GUI

Author: Alex Kim
'''
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from threading import Thread
from math import log
'''from PyQt5.QtWidgets import (
    QApplication,
    QLabel
)'''
import globalVar


class OpenFile():
    def __init__(self):
        self.filename = ""
        self.openFile()
        if self.filename != "":
            self.process()
            self.filename = ""

    def openFile(self):
        self.filename = filedialog.askopenfilename(initialdir="/Users/alexk/Compsci 361/Assignment3", title="Select A File",
                                                   filetypes=(("CSV files", "*.csv"), ("All Files", "*.*")))

    def process(self):
        train_set = pd.read_csv(self.filename)

        abstracts_df = train_set['abstract']
        classes_df = train_set['class']

        # Clean the dataset
        abstracts_df = abstracts_df.str.replace('\W', ' ')  # Removes punctuation
        abstracts_df = abstracts_df.str.lower()
        abstracts_df = abstracts_df.str.split()

        # Set up dictionary
        dictionary = [word for abstract in abstracts_df
                                        for word in abstract]
        self.dictionary = list(set(dictionary))

        # Initialise word_counts to 0 for each unique word for each abstract
        word_count_per_abstract = {unique_word: [0] * len(abstracts_df) for unique_word in self.dictionary}

        # Fill in the word counts
        for index, abstract in enumerate(abstracts_df):
            for word in abstract:
                word_count_per_abstract[word][index] += 1

        # Get the total word count for each word
        total_word_count = {}
        for word in self.dictionary:
            total_word_count[word] = sum(word_count_per_abstract[word])

        # Create a dataframe of the word counts for each abstract
        df = {}
        for word in self.dictionary:
            df[word] = word_count_per_abstract[word]
        word_counts_df = pd.DataFrame(df)

        self.p_word_given_class = {}
        self.p_class_given_abstract = {}

        # Process each class on different threads
        thread_A = Thread(target=self.ThreadFunc(classes_df, word_counts_df, "A"))
        thread_A.start()
        thread_B = Thread(target=self.ThreadFunc(classes_df, word_counts_df, "B"))
        thread_B.start()
        thread_E = Thread(target=self.ThreadFunc(classes_df, word_counts_df, "E"))
        thread_E.start()
        thread_V = Thread(target=self.ThreadFunc(classes_df, word_counts_df, "V"))
        thread_V.start()

        thread_A.join()
        thread_B.join()
        thread_E.join()
        thread_V.join()



    def ThreadFunc(self, class_set_df, word_counts_df, classvar):
        # Isolate each class
        index = class_set_df.index
        class_index = index[class_set_df == classvar]
        class_abstract = word_counts_df.iloc[class_index]

        # Number of Each Abstract
        n_class = len(class_abstract)

        # Size of Dictionary
        n_dictionary = len(self.dictionary)

        # Calculate probabilities of each abstract
        p_class = n_class / len(class_set_df)

        # Laplace smoothing Constant
        alpha = 1

        p_word_given_class = {unique_word:0 for unique_word in self.dictionary}

        for word in self.dictionary:
            n_word_given_class = class_abstract[word].sum()
            p_word_given_class[word] = (n_word_given_class + alpha) / (n_class + alpha*n_dictionary)
        self.p_word_given_class[classvar] = p_word_given_class

        # Using log for probabilities to prevent underflow (to 0) of very small probability float values
        self.p_class_given_abstract[classvar] = log(p_class, 10)
