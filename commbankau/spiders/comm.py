import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from commbankau.items import Article


class CommSpider(scrapy.Spider):
    name = 'comm'
    start_urls = ['https://www.commbank.com.au/newsroom.html']

    def parse(self, response):
        links = response.xpath('//h4/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@class="banner-content no-offer"]/p/text()').get()
        if date:
            date = datetime.strptime(date.strip(), '%d %B %Y')
            date = date.strftime('%Y/%m/%d')

        content = response.xpath('//div[@class="cmp-text"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
