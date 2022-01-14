#!/usr/bin/env python3
"""
Sentiment Classifier :

The file named project_twitter_data.csv has some synthetic (fake, semi-randomly generated) twitter data 
which has the text of a tweet, the number of retweets of that tweet, and the number of replies to that tweet. 
The files positive_words.txt and negative_words.txt contain words that express positive sentiment and 
negative sentiment respectively.

This program detects how positive or negative each tweet is. 
Inputs for the program are the tweets in the "project_twitter_data.csv" file. 
Outputs of the program are one csv file named "resulting_data.csv" and a plot named 'Retweets_vs_NetSentimentalScore.png'.
The csv file output contains columns for the Number of Retweets, Number of Replies, 
Positive Score (which is how many happy words are in the tweet), 
Negative Score (which is how many angry words are in the tweet), and the Net Score for each tweet. 
The image has a plot of the Net Score vs Number of Retweets. 
"""

import pandas as pd 
import matplotlib.pyplot as plt 
import csv

punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']

# Making the list of positive words. 
positive_words = []
with open("positive_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            positive_words.append(lin.strip())


# Making the list of negative words. 
negative_words = []
with open("negative_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            negative_words.append(lin.strip())




def strip_punctuation(s):
    """
    input:
    s - string

    output:
    The string which is stripped off all the punctuations
    """
    for c in punctuation_chars:
        if c in s:
            s = s.replace(c,"")
    return s



def get_pos(stri):
    """
    Input :
    stri - string

    Output :
    The number of positive words in the string.     
    """
    stri_lst = stri.split(" ")
    count = 0
    for wrd in stri_lst:
        if strip_punctuation(wrd).lower() in positive_words:
            count += 1
    return count


def get_neg(stri):
    """
    Input : 
    stri - string

    Output :
    The number of negative words in the string. 
    """
    stri_lst = stri.split(" ")
    count = 0
    for wrd in stri_lst:
        if strip_punctuation(wrd).lower() in negative_words :
            count += 1
    return count

fields = ["Number of Retweets", "Number of Replies", "Positive Score", "Negative Score", "Net Score"]
fvar_write = open("resulting_data.csv", "w")
writer = csv.writer(fvar_write)
writer.writerow(fields)

with open("project_twitter_data.csv", "r") as fvar_read:
    reader = csv.DictReader(fvar_read)

    for row in reader:
        text_of_tweet = row["tweet_text"]
        n_retweets = row["retweet_count"]
        n_replies = row["reply_count"]
    
        text_of_tweet = strip_punctuation(text_of_tweet)      # getting the string removing all the punctuation
        
        n_positive = get_pos(text_of_tweet)                   # getting the number of positive words in the line
        n_negative = get_neg(text_of_tweet)                   # getting the number of negative words in the line
        net_score = n_positive - n_negative                   # getting the difference between the number of positive and negative words

        # writing the values to the file
        writer.writerow([n_retweets , n_replies,  n_positive, n_negative, net_score])
fvar_write.close()


df = pd.read_csv("resulting_data.csv")
xvalues = df["Net Score"].values
yvalues = df["Number of Retweets"].values 


plt.scatter(xvalues, yvalues)
plt.xlabel("Net Sentimental Score")
plt.ylabel("Number of Retweets")
plt.savefig('Retweets_vs_NetSentimentalScore.png', dpi=300)










            
