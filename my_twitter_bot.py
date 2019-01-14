from keys import *
import tweepy
import time
import os
import requests
from bs4 import BeautifulSoup as bs
import cfscrape

print('This is my TwitterBot', flush=True)

# Authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


# =============== REPLY TO MENTIONS ========================
mentions = api.mentions_timeline()

# print("Mentions keys are: ", mentions[0].__dict__.keys())
# print("Last mention was: ", mentions[0].text)
# print("Last mention id: ", mentions[0].id)
# print("Type of last last mention id: ", type(mentions[0].id))

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    print("retrieving and replying to tweets...")
    #DEV NOTE: for TEST purpose use 376831330887036928 in last_seen_id.txt
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode="extended")
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#helloworld' in mention.full_text.lower():
            print("found #helloworld!", flush=True)
            print("responding back...", flush=True)
            api.update_status('@' + mention.user.screen_name 
                                    + ' Hello World is a good hashtag!', mention.id)


# ==================== Publish Pictures ==================

# model scraping for TwitterBot
def scrap_images(search_content,limit):

    # website with images
    url = 'https://www.pexels.com/search/'+ search_content + '/'

    scraper = cfscrape.create_scraper()
    
    # download page for parsing
    page = scraper.get(url)
    soup = bs(page.text, 'html.parser')

    # locate all elements with image tag
    image_tags = soup.findAll('img')

    # create directory for model images
    if not os.path.exists(search_content):
        os.makedirs(search_content)

    # move to new directory
    os.chdir(search_content)

    # image file name variable
    x = 0

    # writing images
    for image in image_tags:
        if x >= int(limit):
            break
        try:
            url = image['src']
            response = scraper.get(url)
            if response.status_code == 200 and image['class'][0] == 'photo-item__img':
                with open(search_content + '-' + str(x) + '.jpg', 'wb') as f:
                    f.write(scraper.get(url).content)
                    f.close()
                    x += 1
        except:
            pass


def publish_image(search_content,limit):
    scrap_images(search_content,limit)

    # iterates over pictures in folder
    for image in os.listdir('.'):
        print("publishing image...", flush=True)
        api.update_with_media(image)
        os.remove(image)
        time.sleep(15)

    # delete directory
    os.chdir('..')
    os.rmdir(search_content)


# ====================== MAIN ============================
if __name__ == "__main__":

    while True:
        query = input("What do you want me to do?\n-> ")
        if(query.lower()=='publish image'):
            theme = input("Which theme do you want me to publish about?\n-> ")
            limit = input("How many?\n-> ")
            publish_image(theme, limit)
        elif(query.lower()=='reply to tweets'):
            while True:
                reply_to_tweets()
                time.sleep(15)
        elif(query.lower()=='quit' or query.lower()=='quit()'):
            print("Goodbye...")
            break
        else:
            print("Don't recognize command!")
