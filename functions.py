'''
Functions used in the GUI

Author: Alex Kim
'''
from tkinter import filedialog
import pandas as pd
from threading import Thread
import re
from math import log

import globalVar
import prompts

'''from PyQt5.QtWidgets import (
    QApplication,
    QLabel
)'''


class OpenFile:
    def __init__(self, pb, lb):
        self.pb = pb
        self.lb = lb
        self.filename = ""
        self.dictionary = []
        self.p_word_given_class = {}
        self.p_class = {}

    def onclick(self):
        self.open_file()
        if self.filename != "":
            Thread(target=self.process).start()


    def open_file(self):
        self.filename = filedialog.askopenfilename(initialdir="/Users/alexk/Compsci 361/Assignment3",
                                                   title="Select A File",
                                                   filetypes=(("CSV files", "*.csv"), ("All Files", "*.*")))

    def process(self):
        self.pb.pack(pady=10)
        self.lb.pack()

        train_set = pd.read_csv(self.filename)

        abstracts_df = train_set['abstract']
        classes_df = train_set['class']

        # Clean the dataset
        abstracts_df = abstracts_df.str.replace('\W', ' ')  # Removes punctuation
        abstracts_df = abstracts_df.str.lower()
        abstracts_df = abstracts_df.str.split()

        self.pb['value'] = 10
        self.lb.configure(text='Finished Cleaning the Dataset')

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

        self.pb['value'] = 20
        self.lb.configure(text='Creating Word Counts')

        # Get the total word count for each word
        total_word_count = {}
        for word in self.dictionary:
            total_word_count[word] = sum(word_count_per_abstract[word])

        # Create a dataframe of the word counts for each abstract
        df = {}
        for word in self.dictionary:
            df[word] = word_count_per_abstract[word]
        word_counts_df = pd.DataFrame(df)

        self.pb['value'] = 60
        self.lb.configure(text='Finished Creating Word Counts Dataframe')

        class_var = [globalVar.class_A, globalVar.class_B, globalVar.class_E, globalVar.class_V]

        for c in class_var:
            # Isolate each class
            index = classes_df.index
            class_index = index[classes_df == c]
            class_abstract = word_counts_df.iloc[class_index]

            # Number of Each Abstract
            n_class = len(class_abstract)

            # Size of Dictionary
            n_dictionary = len(self.dictionary)

            # Calculate probabilities of each abstract
            p_class = n_class / len(classes_df)

            # Laplace smoothing Constant
            alpha = 1

            p_word_given_class = {unique_word: 0 for unique_word in self.dictionary}

            for word in self.dictionary:
                n_word_given_class = class_abstract[word].sum()
                p_word_given_class[word] = (n_word_given_class + alpha) / (n_class + alpha * n_dictionary)
            self.p_word_given_class[c] = p_word_given_class

            self.p_class[c] = p_class

            self.pb['value'] += 10
            self.lb.configure(text="Finished Processing " + c)

        self.pb.pack_forget()
        self.lb.pack_forget()

    def get_p_class(self):
        return self.p_class

    def get_p_word_give_class(self):
        return self.p_word_given_class


class SpamFilter:
    def __init__(self, csv_file, text_box):
        self.csv_file = csv_file
        self.text_box = text_box
        self.prediction = ""

    def onclick(self):
        self.process()
        print("Prediction is " + self.prediction)

    def process(self):
        abstract = self.text_box.get(1.0, "end-1c")
        abstract = re.sub('\W', ' ', abstract)
        abstract = abstract.lower().split()

        p_class_hashmap = self.csv_file.get_p_class()
        p_word_given_class_hashmap = self.csv_file.get_p_word_give_class()

        # Using log for probabilities to prevent underflow (to 0) of very small probability float values
        p_class_given_abstract_hashmap = {
            globalVar.class_A: log(p_class_hashmap[globalVar.class_A], 10),
            globalVar.class_B: log(p_class_hashmap[globalVar.class_B], 10),
            globalVar.class_E: log(p_class_hashmap[globalVar.class_E], 10),
            globalVar.class_V: log(p_class_hashmap[globalVar.class_V], 10)
        }

        for word in abstract:
            for c in p_class_given_abstract_hashmap:
                if word in p_word_given_class_hashmap[c]:
                    p_class_given_abstract_hashmap[c] += log(p_word_given_class_hashmap[c][word], 10)

        self.prediction = max(p_class_given_abstract_hashmap, key=p_class_given_abstract_hashmap.get)