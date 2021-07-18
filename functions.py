'''
Backend Functions used to Process the Data

Author: Alex Kim
'''
from tkinter import filedialog
import pandas as pd
from threading import Thread
from nltk.stem import WordNetLemmatizer
import re
from math import log

import globalVar


def remove_stopwords(abstract):
    return [word for word in abstract if word not in globalVar.STOP_WORDS]


def lemmatize_abstract(abstract):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word) for word in abstract]


class OpenFile:
    def __init__(self, text_box):
        self.text_box = text_box

    def onclick(self):
        filename = filedialog.askopenfilename(initialdir="/Users/alexk/Compsci 361/Assignment3",
                                              title="Select A File",
                                              filetypes=(("Text files", "*.txt"), ("All Files", "*.*")))
        if filename != "":
            f = open(filename, "r")
            abstract = f.read()

            self.text_box.delete(1.0, "end")
            self.text_box.insert(1.0, abstract)


class ProcessData:
    def __init__(self, pb, lb):
        self.pb = pb
        self.lb = lb
        self.p_word_given_class = {}
        self.p_class = {}
        Thread(target=self.process).start()

    def process(self):
        train_set = pd.read_csv("emails.csv", header=1, names=["abstract", "class"])

        self.pb.pack(pady=10)
        self.lb.pack()

        abstracts_df = train_set['abstract']
        classes_df = train_set['class']

        # Clean the dataset
        abstracts_df = abstracts_df.str.replace('\W', ' ')
        abstracts_df = abstracts_df.str.lower()
        abstracts_df = abstracts_df.str.split()

        abstracts_df = abstracts_df.apply(lambda abstract: remove_stopwords(abstract))
        abstracts_df = abstracts_df.apply(lambda abstract: lemmatize_abstract(abstract))

        self.pb['value'] = 10
        self.lb.configure(text='Finished Cleaning the Dataset')

        # Set up dictionary
        dictionary = [word for abstract in abstracts_df for word in abstract]
        dictionary = list(set(dictionary))

        # Initialise word_counts to 0 for each unique word for each abstract
        word_count_per_abstract = {unique_word: [0] * len(abstracts_df) for unique_word in dictionary}

        # Fill in the word counts
        for index, abstract in enumerate(abstracts_df):
            for word in abstract:
                word_count_per_abstract[word][index] += 1

        self.pb['value'] = 20
        self.lb.configure(text='Creating Word Counts')

        DF_score = {unique_word: 0 for unique_word in dictionary}
        for unique_word in dictionary:
            for word_count in word_count_per_abstract[unique_word]:
                if word_count > 0:
                    DF_score[unique_word] += 1

        IDF_score = {unique_word: log(len(train_set['abstract']) / DF_score[unique_word], 10)
                     for unique_word in dictionary}

        # Get the total word count for each word
        total_word_count = {}
        for word in dictionary:
            total_word_count[word] = sum(word_count_per_abstract[word])

        # Create a dataframe of the word counts for each abstract
        df = {}
        for word in dictionary:
            df[word] = word_count_per_abstract[word]
        word_counts_per_abstract_df = pd.DataFrame(df)

        self.pb['value'] = 60
        self.lb.configure(text='Finished Creating Word Counts Dataframe')

        class_var = [globalVar.CLASS_SPAM, globalVar.CLASS_NOT_SPAM]

        for c in class_var:
            # Isolate class
            index = classes_df.index
            class_index = index[classes_df == c]
            class_word_counts_per_abstract_df = word_counts_per_abstract_df.iloc[class_index]

            # Number of Each Abstract
            n_word_given_class = {word: class_word_counts_per_abstract_df[word].sum() * IDF_score[word]
                                  for word in dictionary}
            n_class = sum(n_word_given_class.values())

            # Size of Dictionary
            n_dictionary = len(dictionary)

            # Calculate probabilities of each abstract
            p_class = n_class / len(classes_df)

            p_word_given_class = {unique_word: 0 for unique_word in dictionary}
            for word in dictionary:
                # Use Laplace smoothing + DF-IDF to calculate the probabilities of each word
                p_word_given_class[word] = (n_word_given_class[word] + globalVar.alpha) / (n_class + globalVar.alpha * n_dictionary)
            self.p_word_given_class[c] = p_word_given_class

            self.p_class[c] = p_class

            self.pb['value'] += 10
            self.lb.configure(text="Finished Processing {}".format(c))

        self.pb.pack_forget()
        self.lb.pack_forget()

    def get_p_class(self):
        return self.p_class

    def get_p_word_give_class(self):
        return self.p_word_given_class


class SpamFilter:
    def __init__(self, csv_file, text_box, lb):
        self.csv_file = csv_file
        self.text_box = text_box
        self.prediction = ""
        self.lb = lb

    def onclick(self):
        self.process()
        self.lb.pack()
        self.lb.configure(text="Prediction is " + self.prediction)

    def process(self):
        # Read the abstract in the text box; pre-process it
        abstract = self.text_box.get(1.0, "end-1c")
        abstract = re.sub('\W', ' ', abstract)
        abstract = abstract.lower().split()

        # Get the probabilities from the csv file used to train the model
        p_class_hashmap = self.csv_file.get_p_class()
        p_word_given_class_hashmap = self.csv_file.get_p_word_give_class()

        # Using log for probabilities to prevent underflow (to 0) of very small probability float values
        p_class_given_abstract_hashmap = {
            globalVar.CLASS_SPAM: log(p_class_hashmap[globalVar.CLASS_SPAM], 10),
            globalVar.CLASS_NOT_SPAM: log(p_class_hashmap[globalVar.CLASS_NOT_SPAM], 10)
        }

        for word in abstract:
            for c in p_class_given_abstract_hashmap:
                if word in p_word_given_class_hashmap[c]:
                    p_class_given_abstract_hashmap[c] += log(p_word_given_class_hashmap[c][word], 10)

        if max(p_class_given_abstract_hashmap, key=p_class_given_abstract_hashmap.get):
            self.prediction = "spam"
        else:
            self.prediction = "not spam"
