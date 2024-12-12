import time
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import asyncio
from db.session import get_async_session
from models.dictionary import Word
import contextlib
# Установка и инициализация ChromeDriver

driver = webdriver.Chrome()

driver.get('https://englishart.ru/angliyskie-slova-po-temam/')
time.sleep(1)

def get_themes():
    themes = driver.find_elements(by=By.XPATH, value='/html/body/main/div/div/div')
    return themes

def get_categories(theme):
    theme_name = theme.find_element(by=By.CSS_SELECTOR, value='div.grid-item__title').text
    theme_href = theme.find_element(by=By.CSS_SELECTOR, value='a.grid-item__link').get_attribute('href')
    driver.get(theme_href)
    time.sleep(1)
    main = driver.find_element(by=By.XPATH, value='/html/body/main/div')
    categories_names = main.find_elements(by=By.CSS_SELECTOR, value='strong')
    categories_ul = main.find_elements(by=By.CSS_SELECTOR, value='ul.lcp_catlist')
    categories = []
    for i in range(len(categories_names)):
        categories.append([categories_names[i].text, categories_ul[i]])
    return categories, theme_name

def get_under_categories(category):
    category_name = category[0]
    category_ul = category[1]
    under_categories = category_ul.find_elements(by=By.CSS_SELECTOR, value='li > a')
    under_categories_list = [[under_category.get_attribute('href'), under_category.text] for under_category in under_categories]

    return under_categories_list, category_name

def get_words(under_category):
    under_category_href = under_category[0]
    under_category_name = under_category[1]
    driver.get(under_category_href)
    ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(1)
    words_table = driver.find_element(by=By.XPATH, value='//*[@id="example_wrapper"]/div[1]/div[1]/div/table')
    next_page = words_table.find_element(by=By.XPATH, value='//*[@id="example_next"]')
    db_words = []
    while 'disabled' not in words_table.find_element(by=By.XPATH, value='//*[@id="example_next"]').get_attribute('class'):
        words = words_table.find_elements(by=By.CSS_SELECTOR, value='tbody > tr')
        for word in words:
            english = word.find_element(by=By.CSS_SELECTOR, value='td:nth-child(2) > a').text
            russian = word.find_element(by=By.CSS_SELECTOR, value='td:nth-child(3)').text
            transcription = word.find_element(by=By.CSS_SELECTOR, value='td:nth-child(4)').text
            level = word.find_element(by=By.CSS_SELECTOR, value='#td:nth-child(9)').text
            db_words.append([english, russian, transcription, level])
        next_page = driver.find_element(by=By.XPATH, value='//*[@id="example_next"]')
        next_page.click()
        time.sleep(1)

    return db_words, under_category_name

async def main():
    async_session = contextlib.asynccontextmanager(get_async_session)
    themes = get_themes()
    for theme in themes:
        categories, theme_name = get_categories(theme)
        for category in categories:
            under_categories_list, category_name = get_under_categories(category)
            for under_category in under_categories_list:
                db_words, under_category_name = get_words(under_category)
                for word in db_words:
                    async with async_session() as session:
                        db_word = Word(english=word[0], russian=word[1], transcription=word[2])
                        session.add(db_word)
                        await session.commit()


asyncio.run(main())