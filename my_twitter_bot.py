import tweepy
from keys import *

print('this is my twitter bot')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

mentions = api.mentions_timeline()

# print("Mentions keys are: ", mentions[0].__dict__.keys())
# print("Last mention was: ", mentions[0].text)
# print("Last mention id: ", mentions[0].id)
# print("Type of last last mention id: ", type(mentions[0].id))

for mention in mentions:
    print(str(mention.id) + ' - ' + mention.text)
    if '@guiguifonfon' in mention.text.lower():
        print("found @guiguifonfon!")
        print("responding back...")
