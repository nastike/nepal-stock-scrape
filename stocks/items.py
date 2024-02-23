# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StocksItem(scrapy.Item):
    symbol = scrapy.Field()
    ltp = scrapy.Field()
    open = scrapy.Field()
    high = scrapy.Field()
    low = scrapy.Field()
    previous_close = scrapy.Field()

    pass


class ShareItem(scrapy.Item):
    name = scrapy.Field()
    symbol = scrapy.Field()
    bonus = scrapy.Field()
    cash = scrapy.Field()
    total = scrapy.Field()
    announcement_date = scrapy.Field()
    book_closure_date = scrapy.Field()
    fiscal_year = scrapy.Field()
    ltp = scrapy.Field()
