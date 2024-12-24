# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KancollebotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ShipItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    href = scrapy.Field()


class TimeItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    time = scrapy.Field()
    time_word_cn = scrapy.Field()
    time_word_jp = scrapy.Field()
    href = scrapy.Field()
