# -*- coding: utf-8 -*-
import scrapy
import pytz
from bs4 import BeautifulSoup
from tabelogcrawl.items import TabelogcrawlItem


class TabelogSpider(scrapy.Spider):
    name = 'TabeLogSpider'
    allowed_domains = ['https://tabelog.com/']
    start_urls = ['https://tabelog.com/tokyo/']
    custom_settings = {
        "DOWNLOAD_DELAY": 10.0,
    }

    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        summary_list = soup.find_all("a", class_="cpy-rst-name")

        for summary in zip(summary_list):
            item = TabelogcrawlItem()
            item['name'] = summary.string
            href = summary["href"]
            item['link'] = href

            # 店の緯度経度を取得する為、
            # 詳細ページもクローリングしてTabelogcrawlItemに格納。
            request = scrapy.Request(
                href, callback=self.parse_child)
            request.meta["item"] = item
            yield request

    def parse_child(self, response):
        # 店の緯度経度を抽出する。
        soup = BeautifulSoup(response.body, "html.parser")
        g = soup.find("img", class_="js-map-lazyload")
        longitude, latitude = parse_qs(
            urlparse(g["data-original"]).query)["center"][0].split(",")
        item = response.meta["item"]
        item['longitude'] = longitude
        item['latitude'] = latitude
        return item