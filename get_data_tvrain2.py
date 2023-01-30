#!/usr/bin/env python
# coding: utf-8

# In[15]:


get_ipython().system('pip install config')
import csv
import config
import requests
from tqdm.auto import tqdm
from bs4 import BeautifulSoup
import csv


# In[7]:



headers = {'content-type': 'text/html'}


# In[22]:


def crawl(word, links_list):
    headers = {'content-type': 'text/html'}
    url = f'https://tvrain.tv/archive/?search_teleshow_cat=&search_year=0&search_month=0&search_day=0&query={word}&tab=2&page=2'
    articles_max = 150
    articles_visited = 0
    pbar = tqdm(desc="while loop", total=articles_max)
    doc = requests.get(url, headers=headers)
    while articles_visited < articles_max:
        soup = BeautifulSoup(doc.text, "lxml")
        links_list = []
        data = soup.findAll('div',attrs={'class':'chrono_list__item__info'})
        for div in data:
            links = div.findAll('a', attrs={'class':'chrono_list__item__info__name chrono_list__item__info__name--nocursor'})
            for a in links:
                if a not in links_list:
                    links_list.append(a['href'])
                    articles_visited += 1
        print(articles_visited, end="\r")
        pbar.update(articles_visited)
    pbar.close()

def main():
    headers = {'content-type': 'text/html'}
    words = ["Россия", "Украина", "Путин", "Европа", "Зеленский"]
    article_links = []
    for word in words:
        crawl(word, article_links)
        print(len(article_links))
    
    
    with open("data_tvRain.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f)
    text = " "
    for link in tqdm(article_links):
        doc2 = requests.get(f'https://tvrain.tv/{link}', headers=headers)
        soup_article = BeautifulSoup(doc2.text, "html.parser")
        paragraphs = [paragraph.text for paragraph in soup_article.findAll('p')]
        text = text.join(paragraphs).strip()
        writer.writerow([text])


if __name__ == "__main__":
    main()


# In[ ]:




