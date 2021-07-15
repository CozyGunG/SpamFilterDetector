'''
Setup global variables for the Spam Filters
Author: Alex Kim
'''
from nltk.corpus import stopwords

LIGHT_GREEN = '#90EE90'
BLACK = '#000000'
WHITE = '#FFFFFF'

TITLE_FONT = 'courier 19 bold'
HEADER_FONT = 'helvetica 11'
INPUT_FONT = 'helvetica 16'

CLASS_SPAM = 1
CLASS_NOT_SPAM = 0

STOP_WORDS = set(stopwords.words('english'))
STOP_WORDS.add('subject')

# Laplace smoothing Constant
alpha = 0.1