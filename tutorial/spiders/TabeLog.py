# -*- coding: utf-8 -*-
import scrapy


class TabelogSpider(scrapy.Spider):
    name = 'TabeLog'
    allowed_domains = ['a.com']
    start_urls = ['http://a.com/']

    def parse(self, response):
        pass
