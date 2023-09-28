# Natural Language Processing

# Sort words into a vector and count how often they appear
# Term Frequency - TF(d,t) = number of occurences of term t in document d
# Inverse Document Frequency - IDF(t) = log(D/t) 
# where D = total # of documents and t = # of documents with the term
# W(x,y) = tf(x,y) * log(N/df(x)) to get word count and importance of word in the entire collection of documents

# We'll be using a dataset of 5k text messages to identify spam
messages = [line.rstrip() for line in open('C:/Users/User/Desktop/python/c-rez11/learning/python/data_science/data/SMSSpamCollection')]
print(len(messages))

#for message_no, message in enumerate(messages[:10]):
    #print(message_no, message)
    #print('\n')

# Our data is labeled as 'ham' (normal messages) vs 'spam'. Let's train the model
import pandas as pd
messages = pd.read_csv('SMSSpamCollection', sep='\t',
                           names=["label", "message"])
print(messages.head())
print(messages.describe())
print(messages.groupby('label').describe())

# Think about what features might be indicative of a spam message. What about length of message?
messages['length'] = messages['message'].apply(len)
print(messages.head())

# Let's visualize it
import matplotlib.pyplot as plt
import seaborn as sns
messages.hist(column='length', by='label', bins=50,figsize=(12,4))
# Looks like longer messages tend to be spam

# To do classification, we'll need numbers, not text. How do we do this?
# By converting sequences of characters into vectors (sequences of numbers)

import string
import nltk
nltk.download('stopwords')

mess = 'Sample message! Notice: it has punctuation.'

# Check characters to see if they are in punctuation
nopunc = [char for char in mess if char not in string.punctuation]

# Join the characters again to form the string.
nopunc = ''.join(nopunc)

print(nopunc.split()) # the sample message no longer has punctuation

from nltk.corpus import stopwords
print(stopwords.words('english')[0:10]) # Show some stop words

# Now just remove any stopwords
clean_mess = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

# stopwords are common english words that we try to filter out because they are usually unimportant to our models

print(clean_mess)

# Function to apply to our DataFrame
def text_process(mess):
    """
    Takes in a string of text, then performs the following:
    1. Remove all punctuation
    2. Remove all stopwords
    3. Returns a list of the cleaned text
    """
    # Check characters to see if they are in punctuation
    nopunc = [char for char in mess if char not in string.punctuation]

    # Join the characters again to form the string.
    nopunc = ''.join(nopunc)
    
    # Now just remove any stopwords
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

# Check to make sure its working
print(messages['message'].head(5).apply(text_process))

# Vectorization

# We'll be converting our current list of messages (known as tokens)
#   into a vector that ML models can understand
# We'll use the bag-of-words model to
#   1. Count word frequency in a message
#   2. Weight each count so that frequent tokens get lower weight
#   3. Normalize the vectors to unit length to abstract from the original text length
# Each vector will have as many dimensions as there are unique words in the entire corpus
# Think of the rows as the list of words, and the columns as each text message

from sklearn.feature_extraction.text import CountVectorizer

# Might take awhile...
bow_transformer = CountVectorizer(analyzer=text_process).fit(messages['message'])

# Print total number of vocab words
print(len(bow_transformer.vocabulary_))

# Let's take one text message and get it's bag-of-words counts as a vector
# we take this
message4 = messages['message'][3]
print(message4)
# and turn it into this vector
bow4 = bow_transformer.transform([message4])
print(bow4)
print(bow4.shape) # there are two twice-repeated words. We can use their position to return what they are
print(bow_transformer.get_feature_names_out()[4073])
print(bow_transformer.get_feature_names_out()[9570])

# Now we can do this for our entire df
messages_bow = bow_transformer.transform(messages['message'])
print('Shape of Sparse Matrix: ', messages_bow.shape)
print('Amount of Non-Zero occurences: ', messages_bow.nnz)

sparsity = (100.0 * messages_bow.nnz / (messages_bow.shape[0] * messages_bow.shape[1]))
print('sparsity: {}'.format(round(sparsity)))

# Term frequency - inverse document frequency (TF-IDF)
# the TF-IDF weight is a stat measure used to evaluate how important a word is to a corpus
# importance increases proportionally to the number of times a word appears in the document
#   but is offset by the frequency of the word in the corpus
# variations of this are used in search engines to rank relevance/importance of a word

# Term frequency: TF(t) = (Number of times term t appears in a document)/(Total number of terms in the document)
# IDF(t) = log_e(Total number of documents / Number of documents with term t in it)

# example: a 100-word document where 'cat' appears 3 times
# TF = 3/100
# now, assume we have 10 million documents and 'cat' appears in 1,000 of the documents
# IDF = log_e(10,000,000 / 1,000) = 4
# thus, your final answer is 0.03 * 4 = 0.12

from sklearn.feature_extraction.text import TfidfTransformer

tfidf_transformer = TfidfTransformer().fit(messages_bow)
tfidf4 = tfidf_transformer.transform(bow4)
print(tfidf4)

# let's check a few random words
print(tfidf_transformer.idf_[bow_transformer.vocabulary_['u']])
print(tfidf_transformer.idf_[bow_transformer.vocabulary_['university']])

# transform the entire bag-of-words corpus into TF-IDF corpus at once
messages_tfidf = tfidf_transformer.transform(messages_bow)
print(messages_tfidf.shape) # now that we have vectors, we can train our model

# train the model using a Naive Bayes classifier
from sklearn.naive_bayes import MultinomialNB
spam_detect_model = MultinomialNB().fit(messages_tfidf, messages['label'])

print('predicted:', spam_detect_model.predict(tfidf4)[0])
print('actual:', messages.label[3])

all_predictions = spam_detect_model.predict(messages_tfidf)
print(all_predictions) # get all predictions

# but wait...we trained the model on ALL of our data, so it'd be dumb to test the model on that same data
# thus, the below classification report means nothing

from sklearn.metrics import classification_report
print (classification_report(messages['label'], all_predictions))
# even though this is meaningless, consider whether false positives or false negatives are worse.
#   which is worse?
# In this case, I think it's much worse to have a false positive (assuming spam = positive)
# I'd rather get a few spam text messages (false negatives) than miss an important text from a friend (false positive)


# Train-test split (as we've done many times before)
from sklearn.model_selection import train_test_split

msg_train, msg_test, label_train, label_test = \
train_test_split(messages['message'], messages['label'], test_size=0.2)

print(len(msg_train), len(msg_test), len(msg_train) + len(msg_test))


# create a data pipeline
# we'll run our model again and then predict off the test set
# we'll also automate the data transformation as we receive new data. This is our data pipeline

from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('bow', CountVectorizer(analyzer=text_process)),  # strings to token integer counts
    ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
    ('classifier', MultinomialNB()),  # train on TF-IDF vectors w/ Naive Bayes classifier
])

# now we can directly pass message text data and the pipeline will transform it for us, similar to an API
pipeline.fit(msg_train,label_train)
predictions = pipeline.predict(msg_test)
print(classification_report(predictions,label_test)) # now this is truly separate train-test data

#plt.show()