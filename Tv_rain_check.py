#!/usr/bin/env python
# coding: utf-8

# In[55]:


from bs4 import BeautifulSoup
import config
import requests
from urllib.parse import urljoin
from tqdm.auto import tqdm

headers = {'content-type': 'text/html'}

word = "Россия"
i = 2

url = "https://tvrain.tv/archive/?search_teleshow_cat=&search_year=0&search_month=0&search_day=0&query={word}&tab=2&page={i}"
#text = urllib2.urlopen(url).read()
doc = requests.get(url, headers=headers)
soup = BeautifulSoup(doc.text, "html.parser")


links_list = []
data = soup.findAll('div',attrs={'class':'chrono_list__item__info'})
for div in data:
    links = div.findAll('a', attrs={'class':'chrono_list__item__info__name chrono_list__item__info__name--nocursor'})
    for a in links:
        if a not in links_list:
                links_list.append(a['href'])
#list_full_links = ['https://tvrain.tv/' + i for i in links_list]
print(links_list)
print(len(links_list))


# In[54]:


text = " "
for link in tqdm(links_list):
    doc2 = requests.get(f'https://tvrain.tv/{link}', headers=headers)
    print(f'https://tvrain.tv/{link}')
    soup_article = BeautifulSoup(doc2.text, "html.parser")
#    soup_article2 = soup_article.findAll('p')
    paragraphs = [paragraph.text for paragraph in soup_article.findAll('p')]
    text = text.join(paragraphs).strip()
print(text)


# In[ ]:


abv 

