# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import TabeLogItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class TabeLogSpider(scrapy.Spider):
    name = 'TabeLogSpider'
    allowed_domains = ['https://tabelog.com/']
    start_urls = ['https://tabelog.com/tokyo/']
    custom_settings = {
        "DOWNLOAD_DELAY": 2.0,
    }

    def parse(self, response):

        # 店の情報、店のスコアをリストから抽出。
        link_list = response.xpath('//li//a[@class="list-rst__rst-name-target cpy-rst-name"]/@href').extract()
        name_list = response.xpath('//li//a[@class="list-rst__rst-name-target cpy-rst-name"]/text()').extract()

        for link, name in zip(link_list, name_list):
            # 店ごとに必要な情報をTabelogcrawlItemに格納。
            item = TabeLogItem()
            item['name'] = name
            print(name)
            item['link'] = link
            print(link)

            # 店の緯度経度を取得する為、
            # 詳細ページもクローリングしてTabelogcrawlItemに格納。
            request = scrapy.http.Request(
                link, callback=self.parse_child)
            request.meta["item"] = item
            yield request

        # 次ページ。
        next_page = response.xpath('//link[@rel="next"]/@href')
        if next_page:
            href = next_page.get('href')
            print(href)
            yield scrapy.http.Request(href, callback=self.parse)

    def parse_child(self, response):
        # 店の緯度経度を抽出する。
        print("HAITTERU")
        g = response.xpath('//div//img[@class="js-map-lazyload"]/@data-original').extract()
        g = g.split("center=")
        gg = g[1].split("&markers")
        longitude, latitude = gg[0].split(",")
        item = response.meta["item"]
        item['longitude'] = longitude
        item['latitude'] = latitude
        print(longitude)
        print(latitude)
        return item

    pass
