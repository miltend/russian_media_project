import config
import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

headers = {'User-Agent': config.HEADERS}

word = "Россия"

news_list = []
for i in tqdm(range(1, 5)):
    url = f'https://tvrain.tv/archive/?query={word}&tab=2&page={i}'
    doc = requests.get(url, headers=headers)
    soup = BeautifulSoup(doc.text, "html.parser")
    news = soup.find_all("div", class_="chrono_list__item")
    news_list.extend(news)

print(len(news_list))
