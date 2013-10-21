#!/usr/bin/python
import tweepy
import sqlite3
import datetime
import time

consumer_key = "*"
consumer_secret = "*"
access_token = "*"
access_token_secret = "*"

twitterbotdb = "/home/pi/TwitterBot/.twitterbot.db"
connection = sqlite3.connect(twitterbotdb)
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS twitterbot (tweet text, in_reply_to_status_id text, in_reply_to_user_id text, created_at text, id PRIMARY KEY)')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
# print api.me().name
# api.update_status("printing a tweet from Python on my Raspberry Pi")

user = "helenwalker78"

timeline = api.user_timeline(screen_name=user, include_rts=True, count=20)
for tweet in timeline:
    if tweet.retweeted == False:
        api.retweet(tweet.id)

mytimeline = api.home_timeline(count=50)
for tweets in mytimeline:
    cursor.execute("INSERT OR IGNORE INTO twitterbot VALUES (?, ?, ?, ?, ?)", (tweets.text, tweets.in_reply_to_status_id, tweets.in_reply_to_user_id, tweets.created_at, tweets.id))

connection.commit()

reply_sql = "SELECT COUNT(*) FROM twitterbot WHERE in_reply_to_status_id=?"

mymentions = api.mentions_timeline()
for mention in mymentions:
    tweet_time = datetime.datetime.now()
    reply_text = "Hey, it's "+tweet_time.strftime("%H:%M:%S")+" and you're still talking about me?"

    cursor.execute(reply_sql, [mention.id])
    result = cursor.fetchone()
    if result[0] == 0:
        time.sleep(1)
        api.update_status('@'+mention.author.screen_name+' '+reply_text, mention.id)
