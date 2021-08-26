import re
import json
import tweepy
consumer_key="5tlYTpVNtcxNR1tmPTcgMBC0j"
consumer_secret="wVE3fy3v6340sHINjsJ2LVj6lmxxWPuo6KgALIMkUhlTu5lH4"
access_token="1002907998923774093313-fCET9YfrjgVJLe1gZy1n8O4mnArToO"
access_token_secret="g7GBsQZYagufbl12QX5QXFSCER4mKyp5IVdOMcVKvE"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
if (api):
    print("Login Success")
else:
    print("Failed")
id_list=[25073877, 939091] #add the id's of twitter pages you want to get here. I randomly used trump and biden here.
individual_tweet_list=[]  # the tweets of 1 particular ID or page is stored here and replaced
final_tweet_list=[]
for i in range(len(id_list)):
    new_tweets=[]
    new_tweets = api.user_timeline(id= id_list[i],count=5,tweet_mode='extended') #count tell the number of most recent tweets you want
    for tweet in new_tweets:
        text=str(tweet.full_text)
        text = re.sub(r':', '', text)
        text = re.sub(r'‚Ä¶', '', text)           
        text = re.sub(r'[^\x00-\x7F]+',' ', text)
        print(text) 
        individual_tweet_list.append(text)
    final_tweet_list.append(individual_tweet_list) # This is the final answer. It is a 2D list. First row contains the tweets of first user  
