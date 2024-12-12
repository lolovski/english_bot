import scrapy
import contextlib

from db.session import get_async_session
from models.dictionary import Word



class TolstyslovarSpider(scrapy.Spider):
    name = "tolstyslovar"
    allowed_domains = ["www.tolstyslovar.com/"]
    start_urls = ["http://www.tolstyslovar.com/"]

    def __init__(self, *args, **kwargs):
        super(TolstyslovarSpider, self).__init__(*args, **kwargs)
        self.session = contextlib.asynccontextmanager(get_async_session)

    async def parse(self, response):
        levels = response.css('body > div.content > div > div.mainside > div.cefrMenu').css('a').getall()
        for level in levels:
            yield scrapy.Request(response.urljoin(level), callback=self.parse_level, level_name=level[:-2])


    async def parse_level(self, response, level_name):
        ...
