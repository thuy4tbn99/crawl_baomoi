# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaomoiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    time = scrapy.Field()
    category = scrapy.Field()
    header = scrapy.Field()
    content = scrapy.Field()
    keyword = scrapy.Field()
