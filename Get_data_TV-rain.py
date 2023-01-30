#!/usr/bin/env python
# coding: utf-8

# In[9]:


from bs4 import BeautifulSoup
import config
import requests
from urllib.parse import urljoin
from tqdm.auto import tqdm
import csv
import urllib.parse

headers = {'content-type': 'text/html'}

words_full = ["Россия", "Украина", "Путин", "Европа", "Зеленский"]
words_encode = []
for words in words_full:
    words_encode.append(urllib.parse.quote(words.encode('utf-8'))) # tvrain's url encodes queries in the utf-8 format

links_list = []
for words in words_encode: # loop for each search word
    articles_visited = 0
    for i in range(2,10): # loop for pages in each search
        url = f"https://tvrain.tv/archive/?query={words}&page={i}"
        doc = requests.get(url, headers=headers)
        soup = BeautifulSoup(doc.text, "html.parser")
        data = soup.findAll('div',attrs={'class':'chrono_list__item__info'})
        while articles_visited < 150:
            for div in data:
                links = div.findAll('a', attrs={'class':'chrono_list__item__info__name chrono_list__item__info__name--nocursor'})
                for a in links:
                    if a not in links_list:
                        links_list.append(a['href'])
                        articles_visited += 1
#print(links_list)
#print(len(links_list))


# In[10]:


with open("data_tvRain.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f)
    for link in tqdm(links_list):
        doc2 = requests.get(f'https://tvrain.tv/{link}', headers=headers)
        soup_article = BeautifulSoup(doc2.text, "html.parser")
        text = " "
        paragraphs = [paragraph.text for paragraph in soup_article.findAll('p')]
        text = text.join(paragraphs).strip()
        writer.writerow([text])

