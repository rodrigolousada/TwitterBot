from keys import *
import time
import tweepy
from reply_to_tweets import reply_to_tweets
from publish_image import publish_image

print('This is my TwitterBot', flush=True)

# Authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# Main
if __name__ == "__main__":
    while True:
        query = input("What do you want me to do?\n-> ")
        if(query.lower()=='publish image'):
            theme = input("Which theme do you want me to publish about?\n-> ")
            limit = input("How many?\n-> ")
            publish_image(api, theme, limit)
        elif(query.lower()=='reply to tweets'):
            while True:
                reply_to_tweets(api, 'last_seen_id.txt')
                time.sleep(15)
        elif(query.lower()=='quit' or query.lower()=='quit()'):
            print("Goodbye...")
            break
        else:
            print("Don't recognize command!")
