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
    ship_name = scrapy.Field()
    wiki_url = scrapy.Field()


class TimeItem(scrapy.Item):
    # define the fields for your item here like:
    ship_name = scrapy.Field()
    time_label = scrapy.Field()
    audio_url = scrapy.Field()
    voice_line_ja = scrapy.Field()
    voice_line_zh = scrapy.Field()
