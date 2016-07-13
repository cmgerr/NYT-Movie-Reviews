from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
from time import sleep
import pickle

# import csv with all url's for full reviews
df = pd.read_csv('../../NYT_movie_reviews.csv')


full_reviews = []

# code to loop through list of links and collect review text from webpage
for reviewurl in df['link_url']:
    # open webpage and pull review text
    page = requests.get(reviewurl)
    soup = BeautifulSoup(page.text, 'html.parser')
    paragraphs = soup.findAll("p", {'class': 'story-body-text story-content'})
    # create one string per review
    revText = ''
    for item in paragraphs:
        revText+=(item.text+' ')
    # some pages have different html structure, those get captured by below code
    if revText == '':
        paragraphs = soup.findAll('p')
        for item in paragraphs:
            revText += (item.text + ' ')
    full_reviews.append(revText)
    # save reviews list in case loop runs into issues midway
    with open('full_reviews.pickle', 'wb') as handle:
        pickle.dump(full_reviews, handle)
    # add pause between requests
    sleep(1.+abs(np.random.randn()))

# add reviews as new dataframe column and save to CSV
df['full_review_text'] = full_reviews
df.to_csv('../../NYT_full_reviews.csv', encoding='utf-8', index=False)


# # code below uses lxml html module, but it excludes text that is a hyperlink
# tree = html.fromstring(page.content)
# paragraphs = tree.xpath('//p[@class="story-body-text story-content"]/text()')
# print paragraphs
