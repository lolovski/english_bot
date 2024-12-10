import scrapy
import contextlib

from db.session import get_async_session
from models.dictionary import Word


class WooordhuntSpider(scrapy.Spider):
    name = "wooordhunt"
    allowed_domains = ["wooordhunt.ru"]
    start_urls = ["https://wooordhunt.ru/dic/content/en_ru"]

    def __init__(self, *args, **kwargs):
        super(WooordhuntSpider, self).__init__(*args, **kwargs)
        self.session = contextlib.asynccontextmanager(get_async_session)

    async def parse(self, response):
        parts = response.css('#content').css('a')
        for part in parts:
            link = response.urljoin(part.attrib['href'])
            yield scrapy.Request(link, callback=self.parse_word)


    async def parse_word(self, response):
        words = response.css('#content > div').css('p')
        for word in words:
            link = response.urljoin(word.css('a').attrib['href'])
            english, text = word.css('::text').getall()
            transcription, russian = text.split(' — ')
            async with self.session() as session:
                db_word = Word(
                    english=english,
                    link=link,
                    transcription=transcription,
                    russian=russian
                )
                session.add(db_word)
                await session.commit()

            yield {
                'english': english,
                'link': link,
                'transcription': transcription,
                'russian': russian
            }
