import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By


def parse_poems():
    data = []
    chrome = start_parse()
    parse_pushkin(chrome, data)
    parse_lermontov(chrome, data)
    parse_esenin(chrome, data)
    parse_nekrasov(chrome, data)
    parse_mayakovskii(chrome, data)
    parse_akhmatova(chrome, data)
    df = pd.DataFrame(data, columns=['Autor', 'Poem'])
    df.to_csv('../Data/PoemsDataset.csv', index=False)
    chrome.quit()


def start_parse():
    webdriver_path = 'chromedriver.exe'
    chrome = run_chrome_driver(webdriver_path)
    return chrome


def run_chrome_driver(webdriver_path):
    chrome_service = ChromeService(executable_path=webdriver_path)
    chrome_options = webdriver.ChromeOptions()
    return webdriver.Chrome(service=chrome_service, options=chrome_options)


def parse_pushkin(chrome, data):
    url = f'https://www.culture.ru/literature/poems/author-aleksandr-pushkin'
    parse_autor(chrome, data, 'Pushkin', url)


def parse_lermontov(chrome, data):
    url = f'https://www.culture.ru/literature/poems/author-mikhail-lermontov'
    parse_autor(chrome, data, 'Lermontov', url)


def parse_esenin(chrome, data):
    url = f'https://www.culture.ru/literature/poems/author-sergei-esenin'
    parse_autor(chrome, data, 'Esenin', url)


def parse_nekrasov(chrome, data):
    url = f'https://www.culture.ru/literature/poems/author-nikolai-nekrasov'
    parse_autor(chrome, data, 'Nekrasov', url)


def parse_mayakovskii(chrome, data):
    url = f'https://www.culture.ru/literature/poems/author-vladimir-mayakovskii'
    parse_autor(chrome, data, 'Mayakovskii', url)


def parse_akhmatova(chrome, data):
    url = f'https://www.culture.ru/literature/poems/author-anna-akhmatova'
    parse_autor(chrome, data, 'Akhmatova', url)


def parse_autor(chrome, data, autor, url):
    # print(autor)
    for page in range(1, 4):
        # on page 45 poems
        url_with_page = url + f'?page={page}'
        for i in range(1, 41):
            # print(str(i) + autor)
            chrome.get(url_with_page)
            poem = find_poem(chrome, i)
            if poem == 'undefined':
                continue
            row = [autor, poem]
            data.append(row)


def find_poem(driver, i):
    # find first poem_i of all poems
    xpath = f'//*[@id="__next"]/div/main/div/div[4]/div/div/div/div[2]/div/div/div[{i}]/div/div/a'
    poem_url = driver.find_element(By.XPATH, xpath).get_attribute('href')
    return get_poem_text(driver, poem_url)


def get_poem_text(driver, url):
    driver.get(url)
    # find first div of poem
    try:
        xpath = f'//*[@id="__next"]/div/main/div/div[3]/div/div/div/div[3]/div/div/div[1]'
        poem_text = driver.find_element(By.XPATH, xpath).text
        if len(poem_text) <= 20:
            xpath = f'//*[@id="__next"]/div/main/div/div[3]/div/div/div/div[3]/div/div/div[2]'
            poem_text = driver.find_element(By.XPATH, xpath).text
    except Exception:
        print(url)
        poem_text = 'undefined'
    return poem_text


def main():
    parse_poems()
    # df = pd.read_csv('../Data/PoemsDataset.csv')
    # print(df.head())


if __name__ == '__main__':
    main()
