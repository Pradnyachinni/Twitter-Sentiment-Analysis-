from tkinter import *
import os
import tkinter.messagebox as tm
import re
import json
import tweepy
from tweepy import OAuthHandler
from IPython.display import display
from textblob import TextBlob
import pandas as pd     # To handle data
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt

class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        
        self.label_username = Label(self, text="Username",font=("Times new roman",15))
        self.label_title = Label(self, text="Twitter Sentiment Analysis",font=("Times new roman",20))
        self.label_space1 = Label(self, text=" ")        
        self.label_space2 = Label(self, text=" ")
        self.entry_username = Entry(self)

        self.label_username.grid(row=4, sticky=E)
        self.entry_username.grid(row=4, column=3)
        self.label_title.grid(row=2, sticky=E,columnspan=7)
        self.label_space1.grid(row=3, sticky=E,columnspan=7)
        self.label_space2.grid(row=5, sticky=E,columnspan=7)

        self.logbtn = Button(self, text="Submit", command=self._login_btn_clicked)
        self.logbtn.grid(columnspan=20)
        self.pack()
      
    def _login_btn_clicked(self):
        username = self.entry_username.get()
        consumer_key = 'O3AR0GBFXZyttonfUNUqfC20M'
        consumer_secret = '5gyIsBK9oGUB2AK0CLBRNQMoyf8rlAcH2ZVpLLruwUkl3bN7Xy'
        access_token = '936847131536629765-19pAXPWhQOMmRe8uBrLXare2CiHFyvQ'
        access_token_secret = 'wgKdJN4EDtsfkUie05dXaDR1yEk2k3VbVV1h0Au3BXaVk'
        def twitter_setup():           
            # Authentication and access using keys:
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)

            # Return API with authentication:
            api = tweepy.API(auth)
            return api
        extractor = twitter_setup()
        # We create a tweet list as follows:
        tweets = extractor.user_timeline(screen_name=username, count=200)
        print("Number of tweets extracted: {}.\n".format(len(tweets)))
        data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        def clean_tweet(tweet):
            return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        def analize_sentiment(tweet):
            analysis = TextBlob(clean_tweet(tweet))
            if analysis.sentiment.polarity > 0:
                return 1
            elif analysis.sentiment.polarity == 0:
                return 0
            else:
                return -1
        data['SA'] = np.array([ analize_sentiment(tweet) for tweet in data['Tweets'] ])
        # We display the updated dataframe with the new column:
        display(data.head(10))
        pos_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] > 0]
        neu_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] == 0]
        neg_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] < 0]
        print("Percentage of positive tweets: {}%".format(len(pos_tweets)*100/len(data['Tweets'])))
        print("Percentage of neutral tweets: {}%".format(len(neu_tweets)*100/len(data['Tweets'])))
        print("Percentage de negative tweets: {}%".format(len(neg_tweets)*100/len(data['Tweets'])))
         # printing first 5 positive tweets
        print("\n\nPositive tweets:")
        for tweet in pos_tweets[:5]:
                print(tweet)
        # printing first 5 negative tweets
        print("\n\nNegative tweets:")
        for tweet in neg_tweets[:5]:
                print(tweet)
        print("\n\nNeutral tweets: ")
        for tweet in neu_tweets[:5]:
                print(tweet)
        objects=('positive', 'neutral', 'negative')
        y_pos = np.arange(len(objects))
        p=len(pos_tweets)*100/len(data['Tweets'])
        neu=len(neu_tweets)*100/len(data['Tweets'])
        n=len(neg_tweets)*100/len(data['Tweets'])
        pt=[p,neu,n]
        colors = ['g', 'b', 'r']
        plt.bar(y_pos,pt,align='center',alpha=0.5,color=colors)
        plt.xticks(y_pos, objects)
        plt.ylabel('percentage')
        plt.title('sentiments')
        plt.show()
        explode = (0, 0, 0)  # explode 1st slice
        # Plot
        plt.pie(pt, explode=explode, labels=objects, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        plt.show()



root = Tk()
root.title("Twitter Data Analysis")
lf=LoginFrame(root)
root.mainloop()
