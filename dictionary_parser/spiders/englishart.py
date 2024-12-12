from time import sleep

import scrapy
import contextlib
from scrapy_selenium import SeleniumRequest
from db.session import get_async_session
from models.dictionary import Word
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException



class EnglishartSpider(scrapy.Spider):
    name = "englishart"
    allowed_domains = ["englishart.ru"]
    start_urls = ["https://englishart.ru/angliyskie-slova-na-temu-aksessuary/"]
    custom_settings = {
        'USER_AGENT': "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

    def __init__(self, *args, **kwargs):
        super(EnglishartSpider, self).__init__(*args, **kwargs)
        self.session = contextlib.asynccontextmanager(get_async_session)

    def start_requests(self):
        yield SeleniumRequest(
            url="https://englishart.ru/",
            callback=self.parse,
            wait_time=10,
            wait_until=EC.presence_of_element_located((By.TAG_NAME, 'div'))
        )

    async def parse(self, response):
        try:
            # Ожидание загрузки body

            print(response.text)
            # Проверка наличия ожидаемого контента
            if 'Английские слова' not in response.body.decode('utf-8'):
                self.logger.error("Expected content not found on the page")
                return

        # Парсинг таблицы
            rows = response.css('#example > tbody tr').getall()
            print(rows)
            for row in rows:
                columns = row.css('td::text').getall()
                english = columns[1]
                russian = columns[2]


                yield {
                    'english': english,
                    'russian': russian,
                }

            # Проверка наличия следующей страницы и переход на нее
            current_page = response.css('a.paginate_button.current::text').get()

            if current_page:
                current_page = int(current_page)
                next_page = current_page + 1
                next_page_link = response.css(f'a.paginate_button[data-dt-idx="{next_page}"]::attr(href)').get()
                if next_page_link:
                    yield scrapy.Request(url=response.urljoin(next_page_link), callback=self.parse)
                else:
                    # Если прямой ссылки нет, попробуем использовать JavaScript-вызов
                    yield scrapy.Request(
                        url=response.url,
                        callback=self.parse,
                        dont_filter=True,
                        meta={'next_page': next_page},
                        headers={'X-Requested-With': 'XMLHttpRequest'},
                        method='POST',
                        body=f'action=get_page&page={next_page}'
                    )

        except TimeoutException:
            self.logger.error("Timed out waiting for page to load")
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
