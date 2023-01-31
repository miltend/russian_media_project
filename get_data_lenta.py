import csv
import config
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def initiate_crawler(word):
    url = f"https://lenta.ru/search?query={word}#size=10|sort=2|domain=1|modified,format=yyyy-MM-dd|type=1"
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver


def crawl(word, links_list):
    driver = initiate_crawler(word)
    articles_max = 1500
    articles_visited = 0
    pbar = tqdm(desc="while loop", total=articles_max)
    while articles_visited < articles_max:
        # print(articles_visited, articles_max)
        button = driver.find_element(by=By.CLASS_NAME, value="loadmore__button")
        button.click()
        driver.implicitly_wait(0.6)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "lxml")
        new_links = soup.find_all("a", class_="card-full-news")
        visited_per_cycle = 0
        for link in new_links:
            if link["href"] not in links_list:
                links_list.append(link["href"])
                articles_visited += 1
                visited_per_cycle += 1
        # print(visited_per_cycle, end="\r")
        pbar.update(visited_per_cycle)
    pbar.close()
    driver.quit()


def main():
    headers = {'User-Agent': config.HEADERS}
    words = ["Россия", "Украина", "Путин", "Европа", "Зеленский"]
    article_links = []
    for word in words:
        crawl(word, article_links)
        print(len(article_links))
    with open("data_lenta.txt", "w", encoding="utf-8") as f:
        # writer = csv.writer(f)
        for link in tqdm(article_links):
            doc = requests.get(f'https://lenta.ru{link}', headers=headers)
            soup_article = BeautifulSoup(doc.text, "html.parser")
            text = " "
            paragraphs = [paragraph.text for paragraph in soup_article.find_all("p", class_="topic-body__content-text")]
            text = text.join(paragraphs).strip()
            f.write(text + "\n")


if __name__ == "__main__":
    main()
