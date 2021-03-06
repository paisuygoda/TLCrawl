# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TabeLogItem(scrapy.Item):
    num = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
