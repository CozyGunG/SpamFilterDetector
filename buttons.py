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
        self.filename = ""

    def onclick(self):
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
        dictionary = list(set(dictionary))

        # Initialise word_counts to 0 for each unique word for each abstract
        word_count_per_abstract = {unique_word: [0] * len(abstracts_df) for unique_word in dictionary}

        # Fill in the word counts
        for index, abstract in enumerate(abstracts_df):
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

        # Process each class on different threads
        threadA = Thread(target=self.ThreadFunc(classes_df, word_counts_df, "A"))
        threadA.start()
        threadB = Thread(target=self.ThreadFunc(classes_df, word_counts_df, "B"))
        threadB.start()
        threadE = Thread(target=self.ThreadFunc(classes_df, word_counts_df, "E"))
        threadE.start()
        threadV = Thread(target=self.ThreadFunc(classes_df, word_counts_df, "V"))
        threadV.start()


        threadA.join()
        threadB.join()
        threadE.join()
        threadV.join()



    def ThreadFunc(self, class_set_df, word_counts_df, classvar):
        # Isolate each class
        index = class_set_df.index
        class_index = index[class_set_df == classvar]
        class_abstract = word_counts_df.iloc[class_index]

        # Number of Each Abstract
        n_class = len(class_abstract)

        # Calculate probabilities of each abstract
        p_class = n_class / len(class_set_df)

        print(classvar + " Has Finished")