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
    articles_max = 150
    articles_visited = 0
    pbar = tqdm(desc="while loop", total=articles_max)

    while articles_visited < articles_max:
        button = driver.find_element(by=By.CLASS_NAME, value="loadmore__button")
        button.click()
        driver.implicitly_wait(0.5)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "lxml")
        new_links = soup.find_all("a", class_="card-full-news")
        for link in new_links:
            if link["href"] not in links_list:
                links_list.append(link["href"])
                articles_visited += 1
        print(articles_visited, end="\r")
        pbar.update(articles_visited)
    pbar.close()
    driver.quit()


def main():
    headers = {'User-Agent': config.HEADERS}
    words = ["Россия", "Украина", "Путин", "Европа", "Зеленский"]
    article_links = []
    for word in words:
        crawl(word, article_links)
        print(len(article_links))

    with open("data_lenta.csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        for link in tqdm(article_links):
            doc = requests.get(f'https://lenta.ru{link}', headers=headers)
            soup_article = BeautifulSoup(doc.text, "html.parser")
            text = soup_article.find("div", class_="topic-body__content")
            writer.writerow([text.text])


if __name__ == "__main__":
    main()
