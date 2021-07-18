# SpamFilterDetector
Uses Naive Bayesian algorithm to differentiate spam mails to non-spam mails.  
Data was Preprocessed (Removing punctuation, lowercase, splitting words)  
Lemmatization was used instead of NLTK Stemming due to inconsistencies.  
Laplace smoothing was done when calculating the probabilities.  
![GUI](https://i.gyazo.com/fff3f14f99b8b2c4cc4619cd15d8c8a3.png)
![GUI](https://i.gyazo.com/5247de6cfc527a3636ba9a02dc50e54e.png)

# Running Spam Filter
1. Download and extract the files into the same folder.
2. Make sure that emails.csv is in the project folder (same folder as the other files). 
emails.csv data can be downloaded from https://www.kaggle.com/karthickveerakumar/spam-filter
3. Run spamFilter.py

# What I learnt
- Using Tkinter functions (Labels, Buttons, Frames, Entry Boxes, Output Boxes, Grid System, Opening Files)
- Using Multi-threading to process data
- Pre-processing raw data into more useful data
- Implementing Naive Bayesian Algorithm with using bag of words 
(Applying DF-IDF weights and Laplace smoothing)

# Future goals
- Faster Data Processing
- Use Thread Pools
- Use larger size Data for more precise predictions
- Use this system to separate spam and non spam emails sent to my inbox  