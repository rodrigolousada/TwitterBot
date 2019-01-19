import os
import time
import requests
from bs4 import BeautifulSoup as bs
import cfscrape

# model scraping for TwitterBot
def scrap_images(search_content, limit):

    # website with images
    url = 'https://www.pexels.com/search/' + search_content + '/'

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


# Publish Image Function
def publish_image(api, search_content, limit):
    scrap_images(search_content, limit)

    # iterates over pictures in folder
    for image in os.listdir('.'):
        print("publishing image...", flush=True)
        api.update_with_media(image)
        os.remove(image)
        time.sleep(15)

    # delete directory
    os.chdir('..')
    os.rmdir(search_content)
