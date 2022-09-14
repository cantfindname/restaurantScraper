# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapebackendItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    address = scrapy.Field()
    five_star = scrapy.Field()
    four_star = scrapy.Field()
    three_star = scrapy.Field()
    two_star = scrapy.Field()
    one_star = scrapy.Field()
    pass
