import config
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def initiate_crawler(url):
    # url = f"https://lenta.ru/search?query={word}#size=10|sort=2|domain=1|modified,format=yyyy-MM-dd|type=1"
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver


def crawl(word, links_list):

    articles_max = 160
    articles_visited = 0
    page = 0
    pbar = tqdm(desc="while loop", total=articles_max)

    while articles_visited < articles_max:
        url = f"https://lenta.ru/search?query={word}#from={page}|size=10|sort=2|domain=1|modified," \
                      "format=yyyy-MM-dd|type=1|modified,from=2022-01-01"
        driver = initiate_crawler(url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "lxml")
        new_links = soup.find_all("div", class_="b-search__result-item-title")
        visited_per_cycle = 0
        page += 10
        for link in new_links:
            if link.a["href"] not in links_list:
                links_list.append(link.a["href"])
                articles_visited += 1
                visited_per_cycle += 1
        pbar.update(visited_per_cycle)
        button = driver.find_element(by=By.CLASS_NAME, value="js-search__paginator-next")
        button.click()
        driver.implicitly_wait(0.5)
    pbar.close()
    driver.quit()


def main():
    headers = {'User-Agent': config.HEADERS}
    words = ["Россия", "Украина", "Путин", "Европа", "Зеленский"]
    article_links = []
    for word in words:
        crawl(word, article_links)
        print(len(article_links))
    with open("data_lenta_new.txt", "w", encoding="utf-8") as f:
        # writer = csv.writer(f)
        for link in tqdm(article_links):
            doc = requests.get(link, headers=headers)
            soup_article = BeautifulSoup(doc.text, "html.parser")
            text = " "
            paragraphs = [paragraph.text for paragraph in soup_article.find_all("p", class_="topic-body__content-text")]
            text = text.join(paragraphs).strip()
            f.write(text + "\n")


if __name__ == "__main__":
    main()
