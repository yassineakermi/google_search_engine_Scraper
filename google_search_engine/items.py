# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GoogleSearchEngineItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title= scrapy.Field()
    link= scrapy.Field()
    resultType = scrapy.Field()
    keyword=scrapy.Field()
    createdAT = scrapy.Field()
    rank=scrapy.Field()
